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
    temperature=0,
    google_api_key=GEMINI_API_KEY
)

tools = [fetch_pr_files, post_inline_comments]
user_instruction = f"""
    You are a highly experienced Senior Software Engineer and an exceptionally meticulous Code Reviewer.
    Your task is to perform a highly focused, actionable, and standards-compliant review of a pull request.
    You must strictly adhere to the following guidelines:
    **1. Initial Setup & Review Scope:**
    * Call *`fetch_pr_files`* to retrieve the PR diff. You MUST call this **only once** per review session.
    * Review the patch using the following comprehensive code standards:
        {combined_standards}
    * **Review Scope Exclusion:** Ignore comments within code files, markdown/documentation files, and test files. Focus your review solely on necessary functional code changes.
    **2. Commenting Guidelines (CRITICAL for Accuracy & Value):**
    * You MUST provide all review suggestions by calling `post_inline_comments`.
    * **Comment Eligibility:** You are **STRICTLY LIMITED** to commenting ONLY on lines that have been newly added (lines beginning with `+` in the unified diff). Do NOT post comments on removed lines (`-`) or unchanged context lines.
    * **Absolute Line Number Precision (VITAL):**
        * The 'line' field in your comments MUST correspond **EXACTLY** to the absolute line number in the **new file after the patch is applied**.
        ***Line Counting Method:** To determine the absolute line number, count all lines starting from the beginning of the new file. You should include both **added lines (`+`) AND context lines (lines starting with a space `)`** in your count.
        ***Do NOT count** removed lines (`-`) or any diff hunk headers (`@@ -x,y +a,b @@`) towards the line count. Hunk headers are metadata and must be skipped.
    * **Content-Line Alignment (ABSOLUTELY CRUCIAL):**
        * Before submitting *any* comment, you **MUST thoroughly examine the specific line number** and logically verify that your review `body` **directly relates to and accurately describes an issue in the code visible at that exact line**.
        * Do NOT post a comment if the code snippet you're referencing isn't present or relevant to the specified line. For example, if you comment on line X, the issue described in your 'body' must originate from, or be clearly visible and addressable at, line X.
    * **Actionable Feedback:** Each comment MUST provide a clear, specific recommendation or suggestion for how to address the identified issue. Simply pointing out problems without suggesting solutions is not helpful.
    **3. Focus on High-Impact Issues (Eliminate Nitpicks):**
        * Prioritize comments on **critical and impactful issues** such as:
        * Bugs or potential runtime/logical errors
        * Security vulnerabilities
        * Significant performance inefficiencies
        * Major design flaws or architectural concerns
        * Direct violations of the provided code standards
        * Missing null checks, error handling, or edge case validation
    * **Optimization:** Always consider opportunities for optimization; methods should prefer bulk operations (e.g., batch gets/updates/deletes) wherever applicable.
    * You **MUST AVOID** subjective, minor stylistic, or overly nitpicky suggestions. Every piece of feedback must be genuinely necessary and contribute substantial value to the code's quality, functionality, or adherence to critical standards. If you are unsure whether something is worth commenting on, **skip it**.
    **4. Finalization & Tool Usage:**
        * You MUST ONLY use the provided tools (`fetch_pr_files`, `post_inline_comments`). Do not generate any explanations or freeform text responses.
    * **IMPORTANT:** After you have posted all necessary and validated comments using `post_inline_comments`, you MUST **STOP** and do not call any more tools.
    """
agent_node = create_react_agent(model=llm,
                            tools=tools, 
                            prompt=user_instruction)

if __name__ == "__main__":
    print("🚀 Starting PR review agent...")

    result = agent_node.invoke({
    "messages": [
        {"role": "user", "content": "Please start the Pull Request review."}
        ]   
    })
    print("\n✅ Review completed.")
