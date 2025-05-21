import os
import httpx
from dotenv import load_dotenv
from typing import List
from typing_extensions import TypedDict
from langchain_core.tools import tool

load_dotenv()

TOKEN_GITHUB = os.getenv("TOKEN_GITHUB")
REPO = os.getenv("GITHUB_REPO")
PR_NUMBER = os.getenv("PR_NUMBER")

HEADERS = {
    "Authorization": f"Bearer {TOKEN_GITHUB}",
    "Accept": "application/vnd.github+json"
}


class Comment(TypedDict):
    """Represents an inline comment to be posted."""
    path: str
    line: int
    body: str

@tool
def fetch_pr_files() -> list:
    """
    Fetch changed files and their patch from the PR.
    Returns a list of dicts: { filename, patch }
    """
    if not REPO or not PR_NUMBER:
        print("Error: GITHUB_REPO or PR_NUMBER not set.")
        return []

    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
    try:
        r = httpx.get(url, headers=HEADERS)
        r.raise_for_status()
        files = r.json()
        return [{"filename": f["filename"], "patch": f.get("patch", "")} for f in files if f.get("patch")]
    except httpx.RequestError as e:
        print(f"Error fetching PR files: {e}")
        return []
    except json.JSONDecodeError:
        print("Error decoding JSON response from GitHub API.")
        return []


@tool
def post_inline_comments(comments: List[Comment]) -> str:
    """
    Post multiple inline comments to a PR as a GitHub review.

    Input example:
    [
      {"path": "file.py", "line": 10, "body": "This could be optimized"},
      {"path": "main.py", "line": 42, "body": "Consider renaming this variable"}
    ]
    """
    if not REPO or not PR_NUMBER:
        return "Error: GITHUB_REPO or PR_NUMBER not set."

    if not comments:
        return "No comments to post."

    review_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/reviews"
    review_payload = {
        "body": "AI Code Review",
        "event": "COMMENT",
        "comments": comments
    }
    try:
        response = httpx.post(review_url, headers=HEADERS, json=review_payload)
        response.raise_for_status() # Raise an exception for bad status codes
        return "Inline comments posted successfully."
    except httpx.RequestError as e:
        return f"Failed to post comments: {e}"
    except json.JSONDecodeError:
        return "Error decoding JSON response from GitHub API when posting comments."