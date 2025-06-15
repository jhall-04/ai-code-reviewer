from github import Github
import os
from dotenv import load_dotenv

load_dotenv()

def list_pull_requests():
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO")
    if not token:
        return {"error": "GITHUB_TOKEN not set"}
    if not repo:
        return {"error": "GITHUB_REPO not set"}
    
    g = Github(token)
    repo = g.get_repo(repo)  # Change this to your test repo
    pulls = repo.get_pulls(state='open', sort='created')
    
    return [{"title": pr.title, "number": pr.number} for pr in pulls]

async def handle_pull_request_event(pr):
    token = os.getenv("GITHUB_TOKEN")
    repo = os.getenv("GITHUB_REPO")
    if not token:
        return {"error": "GITHUB_TOKEN not set"}
    if not repo:
        return {"error": "GITHUB_REPO not set"}
    g = Github(token)
    repo = g.get_repo(repo)  # Change this to your test repo
    pull = repo.get_pull(pr['number'])

    if pull:
        files = pull.get_files()

        diffs = []

        for file in files:
            if file.filename.endswith('.py'):
                diffs.append({
                    "filename": file.filename,
                    "status": file.status,
                    "patch": file.patch
                })
        pull.create_issue_comment("Thank you for your contribution! We will review it soon.")
        return {"diffs": diffs}
    else:
        return {"error": f"Pull request #{pr['number']} not found."}

def comment_on_line(pr_num, response):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise ValueError("GITHUB_TOKEN not set")
    g = Github(token)
    repo = g.get_repo(os.getenv("GITHUB_REPO"))
    pr = repo.get_pull(pr_num)
    comments = response.get("comments", [])
    summary = response.get("summary", "AI Review Comment")
    lines = []
    for comment in comments:
        line = {
            "path": comment.get("filename"),
            "position": int(comment.get("line").split('-')[0]),
            "body": comment.get("comment")
        }
        lines.append(line)
    pr.create_review(
        body=summary,
        event="COMMENT",
        comments=lines
    )