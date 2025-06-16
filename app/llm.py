from dotenv import load_dotenv
import requests
import json
import re
import os

load_dotenv()

OLLAMA_URL = "http://localhost:11434/api/generate"
LLM = os.getenv("LLM_MODEL", "llama3")

def run_local_llm(prompt: str, model: str = LLM) -> str:
    response = requests.post(OLLAMA_URL, json={
        "model": model,
        "prompt": prompt,
        "stream": False
    })

    response.raise_for_status()
    answer = response.json()["response"]
    print(f"LLM Response: {answer}")
    print("---------------------")
    match = re.search(r"({.*[.*].*})", answer, re.DOTALL)
    if match:
        return json.loads(match.group(1))
    else:
        raise ValueError("Response does not contain valid JSON format.")