from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "SnakeOS API"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "API for monitoring system resources using psutil"

    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = ["*"]

    # Database Settings
    POSTGRES_SERVER: str = "localhost"  # Using service name from docker-compose
    POSTGRES_USER: str = "snakeos"
    POSTGRES_PASSWORD: str = "snakeos"
    POSTGRES_DB: str = "snakeos"
    POSTGRES_PORT: str = "5432"
    DB_URL: str = (
        f"postgres://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    # JWT Settings
    SECRET_KEY: str = "your-secret-key-here"  # Change this in production
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALGORITHM: str = "HS256"

    # Optional Redis Settings
    REDIS_HOST: Optional[str] = None
    REDIS_PORT: Optional[int] = None
    REDIS_PASSWORD: Optional[str] = None
    REDIS_DB: Optional[int] = 0

    class Config:
        case_sensitive = True
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    This function is cached to avoid reading the .env file on every request.
    """
    return Settings()


# Create a settings instance
settings = get_settings()
