#!/bin/bash

# Authenticate ngrok
ngrok config add-authtoken "$NGROK_AUTHTOKEN"

# Start ngrok in the background
ngrok http 8000 --log=stdout > ngrok.log &
NGROK_PID=$!

# Wait for ngrok API to be ready (up to 10 seconds)
for i in {1..30}; do
    NGROK_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')
    if [ -n "$NGROK_URL" ]; then
        echo "Public ngrok URL: $NGROK_URL"
        break
    fi
    echo "Waiting for ngrok tunnel... ($i)"
    sleep 1
done

if [ -z "$NGROK_URL" ]; then
    echo "⚠️  ngrok tunnel did not appear after 10 seconds."
    cat ngrok.log
    kill $NGROK_PID
    exit 1
fi

# GitHub API base
WEBHOOK_API="https://api.github.com/repos/$GITHUB_REPO/hooks"
HOOK_PATH="$NGROK_URL/webhook"

# Fetch all webhooks
HOOKS=$(curl -s -H "Authorization: token $GITHUB_TOKEN" -H "Accept: application/vnd.github.v3+json" "$WEBHOOK_API")

# Look for the first webhook with the same "content_type" and endpoint path (e.g. ends with /webhook)
EXISTING_HOOK_ID=$(echo "$HOOKS" | jq -r ".[] | select(.config.url | endswith(\"/webhook\")) | .id" | head -n 1)

if [ -n "$EXISTING_HOOK_ID" ]; then
  echo "Updating existing webhook ID $EXISTING_HOOK_ID to point to $HOOK_PATH"
  curl -s -X PATCH "$WEBHOOK_API/$EXISTING_HOOK_ID" \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    -d @- <<EOF
{
  "config": {
    "url": "$HOOK_PATH",
    "content_type": "json",
    "insecure_ssl": "0"
  }
}
EOF
else
  echo "Creating new webhook..."
  curl -s -X POST "$WEBHOOK_API" \
    -H "Authorization: token $GITHUB_TOKEN" \
    -H "Accept: application/vnd.github.v3+json" \
    -d @- <<EOF
{
  "name": "web",
  "active": true,
  "events": ["pull_request"],
  "config": {
    "url": "$HOOK_PATH",
    "content_type": "json",
    "insecure_ssl": "0"
  }
}
EOF
fi

# You can now dynamically register the webhook using this URL, or email it to yourself

# Start FastAPI server
uvicorn app.main:app --host 0.0.0.0 --port 8000