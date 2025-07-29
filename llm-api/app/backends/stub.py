from .base import LLMBackend

class StubBackend(LLMBackend):
    """Stub backend for testing and fallback scenarios."""
    
    def __init__(self):
        super().__init__("stub")
    
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a stub response for the given prompt.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional parameters (ignored)
            
        Returns:
            A stub response text
        """
        self.logger.debug(f"Generating stub response for prompt: {prompt[:50]}...")
        return f"This is a dummy response to: {prompt}"
    
    def is_available(self) -> bool:
        """Stub backend is always available."""
        return True 