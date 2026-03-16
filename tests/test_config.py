"""Tests for Settings validation and properties."""

import pytest

from odooai.config import Settings
from odooai.exceptions import ConfigurationError


class TestSettingsProperties:
    """Test Settings properties."""

    def test_is_production(self) -> None:
        s = Settings(environment="production")
        assert s.is_production is True
        assert s.is_development is False

    def test_is_development(self) -> None:
        s = Settings(environment="development")
        assert s.is_development is True
        assert s.is_production is False


class TestProductionValidation:
    """Test fail-fast validation for production."""

    def test_default_secret_key_rejected(self) -> None:
        s = Settings(environment="production")
        with pytest.raises(ConfigurationError, match="SECRET_KEY"):
            s.validate_production()

    def test_short_secret_key_rejected(self) -> None:
        s = Settings(environment="production", secret_key="short")
        with pytest.raises(ConfigurationError, match="SECRET_KEY"):
            s.validate_production()

    def test_missing_crypto_key_rejected(self) -> None:
        s = Settings(
            environment="production",
            secret_key="a" * 32,
            anthropic_api_key="sk-ant-123",
            database_url="postgresql+asyncpg://user:pass@localhost/odooai",
        )
        with pytest.raises(ConfigurationError, match="ODOO_CRYPTO_KEY"):
            s.validate_production()

    def test_sqlite_in_production_rejected(self) -> None:
        s = Settings(
            environment="production",
            secret_key="a" * 32,
            odoo_crypto_key="key123",
            anthropic_api_key="sk-ant-123",
            database_url="sqlite:///odooai.db",
        )
        with pytest.raises(ConfigurationError, match="PostgreSQL"):
            s.validate_production()

    def test_valid_production_config(self) -> None:
        s = Settings(
            environment="production",
            secret_key="a" * 32,
            odoo_crypto_key="key123",
            anthropic_api_key="sk-ant-123",
            database_url="postgresql+asyncpg://user:pass@localhost/odooai",
        )
        s.validate_production()  # Should not raise

    def test_development_skips_validation(self) -> None:
        s = Settings(environment="development")
        # validate_production would fail, but in dev we don't call it
        assert s.is_development is True
