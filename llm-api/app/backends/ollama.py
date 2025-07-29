import httpx
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
    
    async def generate(self, prompt: str, **kwargs) -> str:
        print(f"[OLLAMA] (async) Generating with model: {self.model}, prompt: {prompt}")
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
            print(f"[OLLAMA] (async) Sending request to {self.generate_url} with payload: {payload}")
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.generate_url, json=payload)
            print(f"[OLLAMA] (async) Response status: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            print(f"[OLLAMA] (async) Response JSON: {data}")
            result = data.get("response", "")
            if not result:
                print(f"[OLLAMA] (async) Empty response from Ollama for model: {model}")
                raise BackendError(f"Empty response from Ollama for model: {model}")
            print(f"[OLLAMA] (async) Generated result: {result}")
            return result
        except httpx.TimeoutException:
            print(f"[OLLAMA] (async) Ollama request timed out after {self.timeout}s")
            raise BackendTimeoutError(f"Ollama request timed out after {self.timeout}s")
        except httpx.RequestError as e:
            print(f"[OLLAMA] (async) Ollama request failed: {e}")
            raise BackendError(f"Ollama request failed: {e}")
        except Exception as e:
            print(f"[OLLAMA] (async) Unexpected error: {e}")
            raise BackendError(f"Unexpected error with Ollama: {e}")
    
    async def is_available(self) -> bool:
        try:
            print(f"[OLLAMA] (async) Checking availability at {self.base_url}/api/tags")
            async with httpx.AsyncClient(timeout=5) as client:
                response = await client.get(f"{self.base_url}/api/tags")
            print(f"[OLLAMA] (async) Availability status: {response.status_code}")
            return response.status_code == 200
        except Exception as e:
            print(f"[OLLAMA] (async) Availability check failed: {e}")
            return False 