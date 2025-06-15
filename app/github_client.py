from github import Github
import os
from dotenv import load_dotenv

load_dotenv()

def list_pull_requests():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        return {"error": "GITHUB_TOKEN not set"}
    
    g = Github(token)
    repo = g.get_repo("jhall-04/assistant")  # Change this to your test repo
    pulls = repo.get_pulls(state='open', sort='created')
    
    return [{"title": pr.title, "number": pr.number} for pr in pulls]