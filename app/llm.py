import requests
import json
import re

OLLAMA_URL = "http://localhost:11434/api/generate"

def run_local_llm(prompt: str, model: str = "llama3") -> str:
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