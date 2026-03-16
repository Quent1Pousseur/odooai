"""
Module: config.py
Role: Application settings loaded from environment variables.
Dependencies: pydantic-settings
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    environment: str = "development"
    app_name: str = "odooai"

    database_url: str = "sqlite+aiosqlite:///odooai.db"
    redis_url: str = "redis://localhost:6379/0"

    secret_key: str = "change_me_in_production_must_be_at_least_32_chars"
    anthropic_api_key: str = ""


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
