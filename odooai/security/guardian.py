"""
Module: security/guardian.py
Role: Security Guardian — gate that classifies models and rejects BLOCKED access.
      ZERO LLM dependency, pure deterministic logic.
      Full implementation (anonymization pipeline, field filtering) in ODAI-SEC-001.
Dependencies: services/model_classifier, domain/value_objects/model_category
"""

from odooai.domain.value_objects.model_category import ModelCategory
from odooai.services.model_classifier import check_model_access


def guard_model_access(model: str) -> ModelCategory:
    """
    Check if a model can be accessed. Raises BlockedModelError if blocked.

    This is the entry point for all Odoo data access requests.

    Args:
        model: Odoo technical model name.

    Returns:
        The ModelCategory (SENSITIVE, STANDARD, or OPEN).

    Raises:
        BlockedModelError: If the model is permanently blocked.
    """
    return check_model_access(model)
