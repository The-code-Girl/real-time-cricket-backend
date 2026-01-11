# 👉 Why?

# Centralized config

# Easy env-based switching

# Production-safe

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Cricket Live Platform"
    ENV: str = "dev"

    # Security
    JWT_SECRET_KEY: str = "change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRY_MINUTES: int = 60

    class Config:
        env_file = ".env"

settings = Settings()

