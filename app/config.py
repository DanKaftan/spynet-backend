"""Configuration settings for the application."""
import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Supabase configuration
    supabase_url: str
    supabase_key: str  # Service role key (for backend)
    
    # JWT configuration
    jwt_secret: Optional[str] = None
    jwt_algorithm: str = "HS256"
    
    # CORS configuration
    cors_origins: list = [
        "http://localhost:3000",
        "http://localhost:8080",
        "https://your-domain.com"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
