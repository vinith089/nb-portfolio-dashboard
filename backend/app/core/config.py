"""
Configuration settings for the Portfolio Monitoring Dashboard API
"""
import secrets
from typing import List, Optional, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8",
        case_sensitive=True
    )
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PROJECT_NAME: str = "Portfolio Monitoring Dashboard"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Security
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1", "0.0.0.0"]
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",  # Next.js dev server
        "http://localhost:8080",  # Alternative frontend port
        "http://127.0.0.1:3000",
    ]
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    # Database Configuration
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_USER: str = "portfolio_user"
    POSTGRES_PASSWORD: str = "portfolio_pass"
    POSTGRES_DB: str = "portfolio_db"
    POSTGRES_PORT: str = "5432"
    DATABASE_URL: Optional[str] = None
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values) -> str:
        if isinstance(v, str):
            return v
        
        # Build database URL from components
        return (
            f"postgresql+asyncpg://"
            f"{values.data.get('POSTGRES_USER')}:"
            f"{values.data.get('POSTGRES_PASSWORD')}@"
            f"{values.data.get('POSTGRES_SERVER')}:"
            f"{values.data.get('POSTGRES_PORT', '5432')}/"
            f"{values.data.get('POSTGRES_DB')}"
        )
    
    # External API Configuration
    STOCK_API_KEY: str = ""
    STOCK_API_URL: str = "https://www.alphavantage.co/query"
    STOCK_API_RATE_LIMIT: int = 5  # requests per minute
    
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Application Limits
    MAX_FUNDS_PER_USER: int = 100
    MAX_HOLDINGS_PER_FUND: int = 500
    CACHE_TTL: int = 300  # 5 minutes
    
    # Performance Settings
    DB_POOL_SIZE: int = 20
    DB_MAX_OVERFLOW: int = 30
    DB_POOL_TIMEOUT: int = 30


# Global settings instance
settings = Settings()