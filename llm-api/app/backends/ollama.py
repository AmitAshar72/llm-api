import requests
from typing import Optional
from .base import LLMBackend, BackendError, BackendTimeoutError
from ..config import settings

class OllamaBackend(LLMBackend):
    """Ollama backend for local LLM inference."""
    
    def __init__(self):
        super().__init__("ollama")
        self.model = settings.ollama_model
        self.base_url = settings.ollama_url
        self.generate_url = f"{self.base_url}/api/generate"
        self.timeout = 30
    
    def generate(self, prompt: str, **kwargs) -> str:
        print(f"[OLLAMA] Generating with model: {self.model}, prompt: {prompt}")
        model = kwargs.get('model', self.model)
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False
        }
        if 'temperature' in kwargs:
            payload['temperature'] = kwargs['temperature']
        if 'top_p' in kwargs:
            payload['top_p'] = kwargs['top_p']
        try:
            print(f"[OLLAMA] Sending request to {self.generate_url} with payload: {payload}")
            response = requests.post(
                self.generate_url,
                json=payload,
                timeout=self.timeout
            )
            print(f"[OLLAMA] Response status: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            print(f"[OLLAMA] Response JSON: {data}")
            result = data.get("response", "")
            if not result:
                print(f"[OLLAMA] Empty response from Ollama for model: {model}")
                raise BackendError(f"Empty response from Ollama for model: {model}")
            print(f"[OLLAMA] Generated result: {result}")
            return result
        except requests.exceptions.Timeout:
            print(f"[OLLAMA] Ollama request timed out after {self.timeout}s")
            raise BackendTimeoutError(f"Ollama request timed out after {self.timeout}s")
        except requests.exceptions.ConnectionError:
            print("[OLLAMA] Cannot connect to Ollama. Is it running?")
            raise BackendError("Cannot connect to Ollama. Is it running?")
        except requests.exceptions.RequestException as e:
            print(f"[OLLAMA] Ollama request failed: {e}")
            raise BackendError(f"Ollama request failed: {e}")
        except Exception as e:
            print(f"[OLLAMA] Unexpected error: {e}")
            raise BackendError(f"Unexpected error with Ollama: {e}")
    
    def is_available(self) -> bool:
        try:
            print(f"[OLLAMA] Checking availability at {self.base_url}/api/tags")
            response = requests.get(f"{self.base_url}/api/tags", timeout=5)
            print(f"[OLLAMA] Availability status: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"[OLLAMA] Availability check failed: {e}")
            return False 