"""
Module: exceptions.py
Role: Centralized exception hierarchy for OdooAI.
      Every exception provides both a technical message (for logs)
      and a user_message (safe for display to users or LLMs).
Dependencies: none (pure Python)
"""


class OdooAIError(Exception):
    """
    Base exception for all OdooAI errors.

    Args:
        message: Technical description for logs (may contain internal details).
        user_message: Safe, human-readable message for display to users or LLMs.
                      Defaults to message if not provided.
    """

    def __init__(self, message: str, user_message: str | None = None) -> None:
        super().__init__(message)
        self.user_message: str = user_message or message


# ============================================================
# CONFIGURATION
# ============================================================


class ConfigurationError(OdooAIError):
    """Missing or invalid environment variable or configuration."""


# ============================================================
# ODOO CONNECTION
# ============================================================


class OdooConnectionError(OdooAIError):
    """Network-level failure connecting to the Odoo instance."""


class OdooAuthError(OdooAIError):
    """Authentication to Odoo failed (bad credentials or expired API key)."""


class OdooValidationError(OdooAIError):
    """Odoo returned a validation error for the requested operation."""


class OdooRecordNotFoundError(OdooAIError):
    """The requested Odoo record does not exist or is not accessible."""


# ============================================================
# SECURITY
# ============================================================


class BlockedModelError(OdooAIError):
    """The model is permanently blocked and can never be exposed."""


class BlockedMethodError(OdooAIError):
    """The method is permanently blocked and can never be called."""


class SecurityError(OdooAIError):
    """Anonymization, encryption, or audit failure."""


# ============================================================
# LLM
# ============================================================


class LLMProviderError(OdooAIError):
    """LLM API call failed (network, auth, or model error)."""


class LLMRateLimitError(OdooAIError):
    """LLM provider rate limit reached. Retry after backoff."""
