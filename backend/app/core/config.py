# 👉 Why?

# Centralized config

# Easy env-based switching

# Production-safe

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # App settings
    APP_NAME: str = "Cricket Live Platform"
    ENV: str = "dev"

    # Security settings
    JWT_SECRET_KEY: str 
    JWT_ALGORITHM: str 
    JWT_EXPIRY_MINUTES: int

    # Database settings
    DATABASE_URL: str  # Database URL

    # Redis settings
    REDIS_HOST: str
    REDIS_PORT: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Instantiate settings to access env variables
settings = Settings()



