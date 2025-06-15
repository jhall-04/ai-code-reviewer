from fastapi import FastAPI, Request
from app.github_client import list_pull_requests, handle_pull_request_event, comment_on_line
from app.prompts import format_diff_prompt
from app.llm import run_local_llm

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AI Code Reviewer Agent Running"}

@app.get("/pulls")
def get_pulls():
    return list_pull_requests()

@app.post("/webhook")
async def github_webhook(request: Request):
    payload = await request.json()
    event = request.headers.get("X-GitHub-Event")

    if event == "pull_request":
        action = payload.get("action")
        pr = payload.get("pull_request", {})
        if action in ["opened", "synchronize", "reopened"]:
            diffs = await handle_pull_request_event(pr)
            if "error" in diffs:
                print(f"Error processing pull request: {diffs['error']}")
                return {"status": "error"}
            for diff in diffs.get("diffs", []):
                prompt  = format_diff_prompt(
                    filename=diff["filename"],
                    status=diff["status"],
                    patch=diff["patch"]
                )
                print(f"\nPrompt:\n{prompt}")
                response = run_local_llm(prompt)
                comment_on_line(
                    pr_num=pr["number"],
                    response=response
                )
                print(f"\nReview:\n{response}")
    return {"status": "ok"}
            