import os
import re
import json
from dotenv import load_dotenv
from typing import List, Dict, Any
from typing_extensions import TypedDict
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from langchain_core.tools import tool as langchain_tool 
from langchain_core.runnables import Runnable
from langgraph.graph import StateGraph, END
from tools import fetch_pr_files, post_inline_comments,Comment

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=GEMINI_API_KEY,
    temperature=0.1
)

llm_tools = [post_inline_comments]
llm_with_tools = llm.bind_tools(llm_tools)

class GraphState(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        files: List of dictionaries containing filename and patch.
        comments: List of dictionaries containing path, line, and body for comments.
        error: Any error message encountered during the process.
    """
    files: List[Dict[str, str]]
    comments: List[Comment] # Use the Comment type imported from tools
    error: str

def fetch_files_node(state: GraphState) -> Dict[str, Any]:
    """
    Node to fetch PR files using the fetch_pr_files tool.
    """
    print("---Fetching PR files---")
    try:
        files = fetch_pr_files.invoke({})
        if not files:
            print("Failed to fetch PR files or no patch files found.")
            return {"files": [], "error": "Failed to fetch PR files or no patch files found."}
        print(f"Fetched {len(files)} files with patches.")
        return {"files": files, "error": ""} # Update state with fetched files
    except Exception as e:
        print(f"Error in fetch_files_node: {e}")
        return {"files": [], "error": f"Error fetching files: {e}"}


def review_code_node(state: GraphState) -> Dict[str, Any]:
    """
    Node to review the fetched code patches using the Gemini model
    and generate comments in the required format by implicitly using the tool schema.
    """
    print("---Reviewing code and generating comments---")
    files = state.get("files", [])
    if not files:
        print("No files to review.")
        return {"comments": [], "error": state.get("error", "No files to review.")}
    try:
        with open("clean_code_standards.md", "r", encoding="utf-8") as f:
            clean_code_standards = f.read()
    except Exception:
        clean_code_standards = ""

    try:
        with open("angular_code_standards.md", "r", encoding="utf-8") as f:
            angular_code_standards = f.read()
    except Exception:
        angular_code_standards = ""

    try:
        with open("csharp_code_standards.md", "r", encoding="utf-8") as f:
            csharp_code_standards = f.read()
    except Exception:
        csharp_code_standards = ""

    prompt_content = f"""
    You are a senior software engineer and an expert code reviewer.
    Your team follows these code standards (enforced strictly in every review):
    For clean code standards - {clean_code_standards}, for angular code - {angular_code_standards}, for C# code - {csharp_code_standards}
    Analyze the provided PR patch data and suggest specific, actionable improvements.
    Focus on important issues like potential bugs, performance problems, security vulnerabilities,
    design flaws, and significant code smells. Avoid nitpicks.
    Keep optimization in mind and methods should always be trying to get, update or delete in bulk wherever possible.
    For each comment you generate, provide the filename, the exact line number the comment applies to
    within the patch, and the comment body. The line number should correspond to the line in the *new* file
    after the changes.

    Your response MUST be a JSON array of comment objects, exactly matching the structure required by the `post_inline_comments` tool.
    Do NOT include any other text or formatting outside the JSON array.

    Here is the PR patch data:
    """
    for file_data in files:
        prompt_content += f"\n\n--- File: {file_data['filename']} ---\n"
        prompt_content += file_data['patch']

    messages = [
        HumanMessage(content=prompt_content)
    ]
    try:
        response = llm_with_tools.invoke(messages)
        print("Raw model response content:", response.content)
        content = response.content.strip()
        content = re.sub(r"^```json|^```|```$", "", content, flags=re.MULTILINE).strip()
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as e:
            print(f"Error parsing model response as JSON: {e}")
            return {"comments": [], "error": "Model response is not valid JSON."}
        valid_comments = []
        for comment in parsed:
            if isinstance(comment, dict) and 'path' in comment and 'line' in comment and 'body' in comment:
                if isinstance(comment['line'], int):
                    valid_comments.append(comment)
                else:
                    print(f"Skipping comment with invalid line type: {comment}")
            else:
                print(f"Skipping invalid comment format: {comment}")

        print(f"Generated {len(valid_comments)} valid comments.")
        return {"comments": valid_comments, "error": ""}

    except Exception as e:
        print(f"Error during code review with Gemini model: {e}")
        return {"comments": [], "error": f"Error during code review: {e}"}


def post_comments_node(state: GraphState) -> Dict[str, Any]:
    """
    Node to post the generated comments using the post_inline_comments tool.
    """
    print("---Posting comments to GitHub---")
    comments = state.get("comments", [])
    if not comments:
        print("No comments to post.")
        return {"error": ""}

    try:
        result = post_inline_comments.invoke({"comments": comments})
        print(f"Posting result: {result}")
        return {"error": result if "Failed" in result else ""}
    except Exception as e:
        print(f"Error in post_comments_node: {e}")
        return {"error": f"Error posting comments: {e}"}

workflow = StateGraph(GraphState)

workflow.add_node("fetch_files", fetch_files_node)
workflow.add_node("review_code", review_code_node)
workflow.add_node("post_comments", post_comments_node)
workflow.set_entry_point("fetch_files")
workflow.add_edge("fetch_files", "review_code")

workflow.add_conditional_edges(
    "review_code",
    lambda state: "post_comments" if state.get("comments") and not state.get("error") else END,
    {"post_comments": "post_comments", END: END}
)

workflow.add_edge("post_comments", END)

app = workflow.compile()

if __name__ == "__main__":
    print("Starting LangGraph Code Review Workflow...")

    initial_state: GraphState = {"files": [], "comments": [], "error": ""}

    final_state = app.invoke(initial_state)

    print("\n--- Workflow Finished ---")
    print("Final State:")
    print(final_state)

    if final_state.get("error"):
        print(f"\nWorkflow completed with error: {final_state['error']}")
    elif final_state.get("comments"):
        print(f"\nSuccessfully processed and potentially posted {len(final_state['comments'])} comments.")
    else:
         print("\nWorkflow completed without generating or posting comments.")

