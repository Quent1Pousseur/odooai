"""
Module: services/model_classifier.py
Role: Service wrapper around ModelClassifier for use in the application layer.
Dependencies: domain/value_objects/model_category
"""

from odooai.domain.value_objects.model_category import ModelCategory, ModelClassifier
from odooai.exceptions import BlockedModelError


def check_model_access(model: str) -> ModelCategory:
    """
    Classify a model and reject BLOCKED ones.

    Args:
        model: Odoo technical model name.

    Returns:
        The ModelCategory if access is allowed.

    Raises:
        BlockedModelError: If the model is in the BLOCKED set.
    """
    category = ModelClassifier.classify(model)
    if category == ModelCategory.BLOCKED:
        raise BlockedModelError(
            message=f"Model {model} is in BLOCKED set",
            user_message=f"Model '{model}' is permanently blocked for security reasons.",
        )
    return category
