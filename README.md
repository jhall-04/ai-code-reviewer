# AI Code Reviewer

# ✨ Features
🧠 Uses a local LLM (via Ollama) to generate intelligent code review suggestions

- 📥 Receives pull request events via GitHub webhooks

- 🧾 Parses diffs and formats prompts with clear context

- 💬 Posts inline comments and full reviews back to GitHub

- 🔒 No cloud dependency — runs entirely locally or on your serve

Modules:

- app/main.py — FastAPI server to receive GitHub events

- app/github_client.py — GitHub API wrapper

- app/prompts.py — LLM prompt formatter

- app/llm.py — Local LLM interface (e.g. Ollama)

- app/commenter.py — GitHub inline comment/review poster (optional)

# 🚀 Quick Start
1. Clone the repo
```
git clone https://github.com/jhall-04/ai-code-reviewer.git
cd ai-code-reviewer
```
# Docker Setup
2. Setup environment variables
create a .env file:
```
GITHUB_TOKEN=your-token # Github Auth Token
GITHUB_REPO=repo-name   # Username/Repo
NGROK_AUTHTOKEN=ngrok-token # Ngrok Auth Token
LLM_MO
```
3. Run docker container
```
docker compose build
docker compose up
```
# Custom Setup
2. Install dependencies
```
pip install -r requirements.txt
```
3. Setup environment variables
create a .env file:
```
GITHUB_TOKEN=your-token # Github Auth Token
GITHUB_REPO=repo-name   # Username/Repo
NGROK_AUTHTOKEN=ngrok-token # Ngrok Auth Token
LLM_MODEL=desired-model # Local model you want to use
```
4. Start Ollama (Other backends down the road)
```
ollama pull llama3
```
5. Run the server
```
uvicorn app.main:app --reload
```
6. Expose your local server (for Github webhooks)
I use ngrok but you can modify to use what works for you
```
ngrok http 8000
```
7. Create a webhook on your Github repo
- URL: https://your-ngrok-url/webhook
- Content type: application/json
- Events: Pull request

# 🧠 How It Works
- GitHub sends a webhook when a PR is opened/updated

- FastAPI receives the payload and fetches the diff

- The diff is formatted into a prompt and sent to the local LLM

- The LLM returns a review comment

- (Optional) The agent parses the comment and posts it inline using GitHub’s API