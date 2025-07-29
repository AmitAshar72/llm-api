from typing import Optional
from .base import LLMBackend, BackendError
from .ollama import OllamaBackend
from .stub import StubBackend
from ..config import settings, BackendType

class BackendFactory:
    """Factory for creating LLM backend instances."""
    
    _backends = {}
    
    @classmethod
    def get_backend(cls, backend_type: Optional[BackendType] = None) -> LLMBackend:
        """
        Get a backend instance for the specified type.
        
        Args:
            backend_type: The type of backend to create. If None, uses settings.llm_backend
            
        Returns:
            An LLMBackend instance
            
        Raises:
            BackendError: If the backend type is not supported
        """
        if backend_type is None:
            backend_type = settings.llm_backend
        
        # Return cached instance if available
        if backend_type in cls._backends:
            return cls._backends[backend_type]
        
        # Create new instance
        backend = cls._create_backend(backend_type)
        cls._backends[backend_type] = backend
        return backend
    
    @classmethod
    def _create_backend(cls, backend_type: BackendType) -> LLMBackend:
        """Create a new backend instance."""
        if backend_type == BackendType.OLLAMA:
            return OllamaBackend()
        elif backend_type == BackendType.STUB:
            return StubBackend()
        elif backend_type == BackendType.HUGGINGFACE:
            # TODO: Implement HuggingFace backend
            raise BackendError("HuggingFace backend not implemented yet")
        elif backend_type == BackendType.OPENAI:
            # TODO: Implement OpenAI backend
            raise BackendError("OpenAI backend not implemented yet")
        elif backend_type == BackendType.CLAUDE:
            # TODO: Implement Claude backend
            raise BackendError("Claude backend not implemented yet")
        else:
            raise BackendError(f"Unsupported backend type: {backend_type}")
    
    @classmethod
    def clear_cache(cls):
        """Clear the backend cache."""
        cls._backends.clear() 