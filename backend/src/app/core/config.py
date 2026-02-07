import os
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database Configuration (PostgreSQL / Neon)
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://neondb_owner:npg_v7JqWkVLAs1X@ep-cold-voice-aipz64az-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require",
    )
    DATABASE_URL_ASYNC: str = os.getenv("DATABASE_URL_ASYNC", "")
    
    # Authentication & Security
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "change-me-at-runtime")
    JWT_SECRET: str = os.getenv("JWT_SECRET", "change-me-at-runtime")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # OpenRouter Configuration (AI Chatbot)
    OPENROUTER_API_KEY: str = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL: str = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    OPENROUTER_BASE_URL: str = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
    
    # MCP Server Configuration (Phase III)
    MCP_SERVER_PORT: int = int(os.getenv("MCP_SERVER_PORT", "8001"))
    
    # Development Settings
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # CORS Settings
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://localhost:3000",
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
