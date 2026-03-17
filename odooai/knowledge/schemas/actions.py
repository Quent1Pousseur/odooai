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


class MethodEffect(BaseModel, frozen=True):
    """An effect detected in a method body."""

    type: str  # state_change, create, write, unlink, env_ref
    target_model: str = ""
    field: str = ""
    value: str = ""
    via_method: str = ""


class MethodActionFlow(BaseModel, frozen=True):
    """Analysis of a method's effects — what it DOES."""

    method_name: str
    model: str
    effects: list[MethodEffect] = []
    calls: list[str] = []  # Internal methods called
    env_refs: list[str] = []  # self.env['model'] references
