"""
Module: knowledge/schemas/constraints.py
Role: Schemas for SQL and Python constraints.
Dependencies: pydantic
"""

from pydantic import BaseModel


class SqlConstraint(BaseModel, frozen=True):
    """SQL constraint defined in _sql_constraints."""

    name: str  # Constraint name
    sql: str  # SQL expression
    message: str  # Error message


class PythonConstraint(BaseModel, frozen=True):
    """Python constraint defined via @api.constrains."""

    method_name: str
    fields: list[str]  # Fields watched by @api.constrains
    docstring: str = ""


class OnchangeMethod(BaseModel, frozen=True):
    """Method decorated with @api.onchange."""

    method_name: str
    fields: list[str]  # Fields that trigger onchange
    docstring: str = ""
