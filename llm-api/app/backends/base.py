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
    async def generate(self, prompt: str, **kwargs) -> str:
        pass
    
    @abstractmethod
    async def is_available(self) -> bool:
        pass

class BackendError(Exception):
    """Base exception for backend errors."""
    pass

class BackendNotAvailableError(BackendError):
    """Raised when a backend is not available."""
    pass

class BackendTimeoutError(BackendError):
    """Raised when a backend request times out."""
    pass 