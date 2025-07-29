from pydantic_settings import BaseSettings
from typing import Optional
from enum import Enum

class BackendType(str, Enum):
    OLLAMA = "ollama"
    HUGGINGFACE = "huggingface"
    OPENAI = "openai"
    CLAUDE = "claude"
    STUB = "stub"

class HuggingFaceMode(str, Enum):
    LOCAL = "local"
    CLOUD = "cloud"

class Settings(BaseSettings):
    # Backend selection
    llm_backend: BackendType = BackendType.OLLAMA
    
    # Ollama configuration
    ollama_model: str = "llama2"
    ollama_url: str = "http://localhost:11434"
    
    # HuggingFace configuration
    hf_mode: Optional[HuggingFaceMode] = None
    hf_model: Optional[str] = None
    hf_api_key: Optional[str] = None
    
    # OpenAI configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-3.5-turbo"
    
    # Claude configuration
    claude_api_key: Optional[str] = None
    claude_model: str = "claude-3-sonnet-20240229"
    
    # Logging configuration
    log_file: str = "logs/log.jsonl"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

# Global settings instance
settings = Settings() 