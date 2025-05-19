import os
import httpx
from agents import function_tool

TOKEN_GITHUB = os.getenv("TOKEN_GITHUB")
REPO = os.getenv("GITHUB_REPO")
PR_NUMBER = os.getenv("PR_NUMBER")

HEADERS = {
    "Authorization": f"Bearer {TOKEN_GITHUB}",
    "Accept": "application/vnd.github+json"
}

@function_tool
def fetch_pr_files() -> list:
    """
    Fetch changed files and their patch from the PR.
    Returns a list of dicts: { filename, patch }
    """
    url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/files"
    r = httpx.get(url, headers=HEADERS)
    files = r.json()
    return [{"filename": f["filename"], "patch": f.get("patch", "")} for f in files if f.get("patch")]

@function_tool
def post_inline_comments(comments: list) -> str:
    """
    Post multiple inline comments to a PR as a GitHub review.

    Input example:
    [
      {"path": "file.py", "line": 10, "body": "This could be optimized"},
      {"path": "main.py", "line": 42, "body": "Consider renaming this variable"}
    ]
    """
    review_url = f"https://api.github.com/repos/{REPO}/pulls/{PR_NUMBER}/reviews"
    review_payload = {
        "body": "AI Code Review",
        "event": "COMMENT",
        "comments": comments
    }
    response = httpx.post(review_url, headers=HEADERS, json=review_payload)
    if response.status_code == 200:
        return "Inline comments posted."
    else:
        return f"Failed to post comments: {response.text}"
