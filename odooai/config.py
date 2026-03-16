"""
Module: config.py
Role: Application settings loaded from environment variables.
      Includes fail-fast validation for production deployments.
Dependencies: pydantic-settings
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict

from odooai.exceptions import ConfigurationError


class Settings(BaseSettings):
    """Application configuration from environment variables."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    # Application
    environment: str = "development"
    app_name: str = "odooai"
    log_level: str = "INFO"

    # Database
    database_url: str = "sqlite+aiosqlite:///odooai.db"

    # Cache
    redis_url: str = "redis://localhost:6379/0"

    # Security
    secret_key: str = "change_me_in_production_must_be_at_least_32_chars"
    odoo_crypto_key: str = ""
    odoo_crypto_key_previous: str = ""

    # Odoo
    odoo_url: str = ""
    odoo_db: str = ""

    # LLM
    anthropic_api_key: str = ""

    # Monitoring
    sentry_dsn: str = ""

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"

    def validate_production(self) -> None:
        """
        Fail-fast validation for production deployments.

        Raises ConfigurationError if critical settings are missing or insecure.
        Must be called at startup in production.
        """
        errors: list[str] = []

        if self.secret_key == "change_me_in_production_must_be_at_least_32_chars":
            errors.append("SECRET_KEY must be changed from default")
        if len(self.secret_key) < 32:
            errors.append("SECRET_KEY must be at least 32 characters")
        if not self.odoo_crypto_key:
            errors.append("ODOO_CRYPTO_KEY is required")
        if not self.anthropic_api_key:
            errors.append("ANTHROPIC_API_KEY is required")
        if "sqlite" in self.database_url:
            errors.append("DATABASE_URL must use PostgreSQL in production")
        if self.odoo_url and not self.odoo_url.startswith("https://"):
            errors.append("ODOO_URL must use HTTPS in production")

        if errors:
            detail = "; ".join(errors)
            raise ConfigurationError(
                f"Production configuration errors: {detail}",
                user_message="Server configuration is incomplete. Contact the administrator.",
            )


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings."""
    return Settings()
