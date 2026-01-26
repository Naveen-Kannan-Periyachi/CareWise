"""
LLM interface using Ollama for local inference.
"""

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.1:8b"


def call_llm(prompt: str) -> str:
    """Call the local Ollama LLM with a prompt."""
    response = requests.post(
        OLLAMA_URL,
        json={"model": MODEL, "prompt": prompt, "stream": False},
        timeout=60
    )
    response.raise_for_status()
    return response.json()["response"]
