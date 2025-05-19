
import os
from dotenv import load_dotenv
from agents import Agent, Runner
from tools import fetch_pr_files, post_inline_comments

load_dotenv()

def run_code_review():
    """Run the code review process using the OpenAI Agents SDK"""
    
    # Create the agent with the tools from tools.py
    code_reviewer = Agent(
        name="InlineCodeReviewer",
        instructions="""
        You're a senior software engineer and an expert code reviewer. Analyze the PR patch and suggest specific improvements.
        Reply in this exact JSON format:
        [
          { "path": "<filename>", "line": <line_number>, "body": "<review comment>" }
        ]
        Only comment on important issues — avoid nitpicks.
        """,
        tools=[fetch_pr_files, post_inline_comments],
        model="gpt-4-turbo"
    )
    
    # Run the agent synchronously
    result = Runner.run_sync(
        code_reviewer, 
        """
        Use fetch_pr_files to get the PR diff.
        Then call post_inline_comments with specific comments using filename, line number, and text.
        """
    )
    
    # Print the final output
    print(result.final_output)
    
    # Optionally, to see the entire execution trace including all tool calls
    # import json
    # print("\nExecution trace:", json.dumps(result.trace, indent=2))

if __name__ == "__main__":
    run_code_review()