from fastapi import FastAPI
from app.github_client import list_pull_requests

app = FastAPI()

@app.get("/")
def root():
    return {"message": "AI Code Reviewer Agent Running"}

@app.get("/pulls")
def get_pulls():
    return list_pull_requests()