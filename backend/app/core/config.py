"""Core configuration settings for the Philosophy Chat backend."""

import os
from typing import List, Optional

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "Philosophy Chat API"
    version: str = "0.1.0"
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database
    database_url: str
    test_database_url: Optional[str] = None
    
    # Authentication
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # AI APIs
    openai_api_key: str
    anthropic_api_key: Optional[str] = None
    hf_token: Optional[str] = None
    
    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Redis (optional)
    redis_url: Optional[str] = None
    
    # Logging
    log_level: str = "INFO"
    
    # NLP Settings
    spacy_model: str = "en_core_web_lg"
    max_context_length: int = 10
    philosophical_depth_threshold: float = 0.6
    concept_extraction_threshold: float = 0.7
    
    # Performance
    max_concurrent_requests: int = 100
    request_timeout: float = 30.0
    ai_response_timeout: float = 25.0
    
    @validator("cors_origins", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        """Parse CORS origins from environment variable."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @validator("database_url", pre=True)
    def assemble_db_connection(cls, v: Optional[str]) -> str:
        """Ensure database URL is provided."""
        if not v:
            raise ValueError("DATABASE_URL must be provided")
        return v
    
    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()