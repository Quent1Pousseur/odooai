"""
Module: knowledge/schemas/actions.py
Role: Schemas for Odoo action methods (buttons, workflows).
Dependencies: pydantic
"""

from pydantic import BaseModel


class ActionMethod(BaseModel, frozen=True):
    """Action method on a model (button, workflow step)."""

    name: str  # Method name (e.g. 'action_confirm')
    model: str  # Model it belongs to
    docstring: str = ""
    decorators: list[str] = []  # e.g. ['api.depends', 'api.model']
    returns: str = ""  # Return type hint if available
