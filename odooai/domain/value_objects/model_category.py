"""
Module: domain/value_objects/model_category.py
Role: Classify Odoo models into security categories (blocked/sensitive/standard/open).
Dependencies: none (pure Python)
"""

from enum import StrEnum
from typing import ClassVar


class ModelCategory(StrEnum):
    """
    Security classification for Odoo models.

    BLOCKED:   Never exposed (security-critical: ir.rule, res.users, etc.)
    SENSITIVE: Financial / HR data — subject to anonymization
    STANDARD:  Normal business models — default handling
    OPEN:      Reference data (products, currencies) — no restrictions
    """

    BLOCKED = "blocked"
    SENSITIVE = "sensitive"
    STANDARD = "standard"
    OPEN = "open"


class ModelClassifier:
    """
    Stateless classifier that maps any Odoo model name to a ModelCategory.

    Classification priority:
      1. _BLOCKED set (exact match) — NEVER overridable
      2. Explicit overrides (loaded at startup)
      3. _SENSITIVE set (exact match)
      4. _SENSITIVE_PREFIXES (prefix match)
      5. _OPEN set (exact match)
      6. Default -> STANDARD
    """

    _BLOCKED: frozenset[str] = frozenset(
        {
            "ir.rule",
            "ir.model.access",
            "res.users",
            "res.groups",
            "ir.config_parameter",
            "ir.cron",
            "ir.mail_server",
        }
    )

    _SENSITIVE: frozenset[str] = frozenset(
        {
            "account.move",
            "account.payment",
            "account.bank.statement",
            "hr.payslip",
            "hr.contract",
            "hr.employee",
            "res.partner",
            "mail.message",
            "base.automation",
            "ir.actions.server",
            "ir.module.module",
            "ir.ui.view",
        }
    )

    _SENSITIVE_PREFIXES: tuple[str, ...] = ("account.", "hr.")

    _OPEN: frozenset[str] = frozenset(
        {
            "product.product",
            "product.category",
            "product.template",
            "res.country",
            "res.currency",
            "uom.uom",
            "res.lang",
            "res.country.state",
        }
    )

    _overrides: ClassVar[dict[str, ModelCategory]] = {}

    @classmethod
    def classify(cls, model: str) -> ModelCategory:
        """
        Classify an Odoo model into a security category.

        Args:
            model: Odoo technical model name (e.g. 'account.move').

        Returns:
            The ModelCategory for this model.
        """
        if model in cls._BLOCKED:
            return ModelCategory.BLOCKED
        if model in cls._overrides:
            return cls._overrides[model]
        if model in cls._SENSITIVE:
            return ModelCategory.SENSITIVE
        if any(model.startswith(p) for p in cls._SENSITIVE_PREFIXES):
            return ModelCategory.SENSITIVE
        if model in cls._OPEN:
            return ModelCategory.OPEN
        return ModelCategory.STANDARD

    @classmethod
    def load_overrides(cls, overrides: list[tuple[str, ModelCategory]]) -> None:
        """
        Load model category overrides (e.g. from DB at startup).

        Overrides cannot promote BLOCKED models — those are always blocked.

        Args:
            overrides: List of (model_name, category) tuples.
        """
        cls._overrides = {
            model: category for model, category in overrides if model not in cls._BLOCKED
        }

    @classmethod
    def clear_overrides(cls) -> None:
        """Remove all overrides (useful for testing)."""
        cls._overrides = {}
