from .base import LLMBackend

class StubBackend(LLMBackend):
    """Stub backend for testing and fallback scenarios."""
    
    def __init__(self):
        super().__init__("stub")
    
    async def generate(self, prompt: str, **kwargs) -> str:
        print(f"[STUB] (async) Generating stub response for prompt: {prompt[:50]}...")
        return f"This is a dummy response to: {prompt}"
    
    async def is_available(self) -> bool:
        return True 