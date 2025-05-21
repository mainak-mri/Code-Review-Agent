import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import MessageGraph
from langgraph.prebuilt import create_react_agent
from tools import fetch_pr_files, post_inline_comments

def load_standards(file_name: str) -> str:
    try:
        with open(file_name, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return ""

clean_code = load_standards("clean_code_standards.md")
angular_code = load_standards("angular_code_standards.md")
csharp_code = load_standards("csharp_code_standards.md")
combined_standards = f"{clean_code}\n\n{angular_code}\n\n{csharp_code}"

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    temperature=0.1,
    google_api_key=GEMINI_API_KEY
)

tools = [fetch_pr_files, post_inline_comments]
agent_node = create_react_agent(model=llm, tools=tools)

if __name__ == "__main__":
    print("🚀 Starting PR review agent...")

    user_instruction = f"""
        You are a senior software engineer and an expert code reviewer.

        You must:
        1. Call `fetch_pr_files` to get the PR diff.
        2. Review the patch using the following code standards:
        {combined_standards}
        3. Call `post_inline_comments` with actionable review suggestions. Make sure the line number matches with the code review you are doing. It should not be such that you are referrring to a method and that method doesn't exist in the line number.
        4. Analyze the provided PR patch data and suggest specific, actionable improvements.
        5. ONLY comment on added lines (those that begin with `+` in unified diff).
        6. Focus on important issues like potential bugs, performance problems, security vulnerabilities, design flaws, spelling errors and significant code smells. Avoid nitpicks.
        7. Keep optimization in mind and methods should always be trying to get, update or delete in bulk wherever possible.
        8. The line number should correspond to the line in the *new* file
        after the changes. Do not comment on removed lines (`-`) or unchanged lines.
        9. Do NOT add nitpicks — focus on actual issues.
        Only use the provided tools. Do not reply with plain text explanations.
        10. When suggesting comments, ensure the "line" field refers to the line number in the new file after the patch is applied. Do not use line numbers from the diff header or the old file.
        11. IMPORTANT: After you have posted all necessary comments using post_inline_comments, STOP and do not call any more tools.
        You must only call fetch_pr_files once per review session.
        12. Ignore Comments and doc files. Review only necessary codes and not all the files necessarily.
        """

    result = agent_node.invoke({
    "messages": [
        {"role": "user", "content": user_instruction}
        ]   
    })
    print("\n✅ Review completed.")
