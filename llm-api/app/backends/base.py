from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)

class LLMBackend(ABC):
    """Abstract base class for LLM backends."""
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logging.getLogger(f"{__name__}.{name}")
    
    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> str:
        """
        Generate a response for the given prompt.
        
        Args:
            prompt: The input prompt
            **kwargs: Additional parameters specific to the backend
            
        Returns:
            The generated response text
            
        Raises:
            BackendError: If the backend fails to generate a response
        """
        pass
    
    def is_available(self) -> bool:
        """
        Check if the backend is available and ready to use.
        
        Returns:
            True if the backend is available, False otherwise
        """
        try:
            # Try a simple test generation
            test_response = self.generate("test")
            return bool(test_response and test_response.strip())
        except Exception as e:
            self.logger.warning(f"Backend {self.name} is not available: {e}")
            return False

class BackendError(Exception):
    """Base exception for backend errors."""
    pass

class BackendNotAvailableError(BackendError):
    """Raised when a backend is not available."""
    pass

class BackendTimeoutError(BackendError):
    """Raised when a backend request times out."""
    pass 