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

🚀 Quick Start
1. Clone the repo
2. Install dependencies
3. Setup environment variables
4. Start Ollama
5. Run the server
6. Expose your local server (for Github webhooks)
7. Create a webhook on your Github repo

🧠 How It Works
- GitHub sends a webhook when a PR is opened/updated

- FastAPI receives the payload and fetches the diff

- The diff is formatted into a prompt and sent to the local LLM

- The LLM returns a review comment

- (Optional) The agent parses the comment and posts it inline using GitHub’s API