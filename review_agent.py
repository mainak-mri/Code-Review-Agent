import os
from dotenv import load_dotenv
from openai import AssistantAgent, OpenAI
from tools import fetch_pr_files, post_inline_comments

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
agent = AssistantAgent(
    client=client,
    name="InlineCodeReviewer",
    instructions="""
You're a senior software enginner and an expert code reviewer. Analyze the PR patch and suggest specific improvements.
Reply in this exact JSON format:
[
  { "path": "<filename>", "line": <line_number>, "body": "<review comment>" }
]
Only comment on important issues — avoid nitpicks.
""",
    tools=[fetch_pr_files, post_inline_comments],
    model="gpt-4-turbo"
)

response = agent.run("""
Use `fetch_pr_files` to get the PR diff.
Then call `post_inline_comments` with specific comments using filename, line number, and text.
""")
print(response)
