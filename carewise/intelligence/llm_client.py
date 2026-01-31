"""LLM interface using Ollama for local inference"""

import requests
from config.settings import OLLAMA_URL, LLM_MODEL, LLM_TIMEOUT


def call_llm(prompt: str) -> str:
    """Call the local Ollama LLM with a prompt."""
    try:
        response = requests.post(
            OLLAMA_URL,
            json={"model": LLM_MODEL, "prompt": prompt, "stream": False},
            timeout=LLM_TIMEOUT
        )
        response.raise_for_status()
        return response.json()["response"]
    except requests.exceptions.ConnectionError:
        raise RuntimeError(
            f"Cannot connect to Ollama at {OLLAMA_URL}. "
            "Please ensure Ollama is running with: ollama serve"
        )
    except requests.exceptions.HTTPError as e:
        error_detail = ""
        try:
            error_detail = response.json().get("error", "")
        except:
            pass
        raise RuntimeError(
            f"Ollama API error: {e}. "
            f"Detail: {error_detail}. "
            f"Make sure model '{LLM_MODEL}' is installed with: ollama pull {LLM_MODEL}"
        )
