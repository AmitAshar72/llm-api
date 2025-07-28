import os
import requests

def generate_response(prompt: str) -> str:
    model = os.getenv("OLLAMA_MODEL", "llama2")
    ollama_url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt
    }
    try:
        response = requests.post(ollama_url, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        # Ollama returns streaming responses, but for /api/generate, 'response' key is present
        return data.get("response") or data.get("message") or f"[Ollama] No response for: {prompt}"
    except Exception:
        # Fallback to stub
        return f"This is a dummy response to: {prompt}" 