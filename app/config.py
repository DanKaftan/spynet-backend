"""Configuration settings for the application."""
import os
from typing import Optional, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Supabase configuration
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None  # Service role key (for backend)
    
    # JWT configuration
    jwt_secret: Optional[str] = None
    jwt_algorithm: str = "HS256"
    
    # CORS configuration - can be comma-separated string or list
    # Using wildcard to allow all origins for testing (adjust for production)
    cors_origins: Union[str, list] = "*"
    
    @field_validator('cors_origins', mode='before')
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            # Split comma-separated string and strip whitespace
            return [origin.strip() for origin in v.split(',') if origin.strip()]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
