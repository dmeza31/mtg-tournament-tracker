"""Configuration management for the application."""
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str = "postgresql://postgres:postgres@localhost:5432/mtg_tournaments"
    
    # Server
    server_host: str = "0.0.0.0"
    server_port: int = 8000
    
    # CORS
    cors_origins: str = "http://localhost:3000,http://localhost:8080"
    
    # Application
    app_name: str = "MTG Tournament Tracker API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
