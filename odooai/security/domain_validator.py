"""
Module: security/domain_validator.py
Role: Validate Odoo domain filters to prevent injection attacks.
      Rejects malformed domains, forbidden operators, and suspicious field names.
      ZERO LLM dependency — pure deterministic logic.
Dependencies: odooai.exceptions
"""

from __future__ import annotations

from typing import Any

from odooai.exceptions import DomainInjectionError

# Operators allowed in Odoo domain filters.
_VALID_OPERATORS = frozenset(
    {
        "=",
        "!=",
        ">",
        ">=",
        "<",
        "<=",
        "like",
        "ilike",
        "not like",
        "not ilike",
        "in",
        "not in",
        "child_of",
        "parent_of",
        "=like",
        "=ilike",
    }
)

# Logical connectors in Odoo polish-notation domains.
_LOGICAL_OPERATORS = frozenset({"&", "|", "!"})

# Field name prefixes that indicate private/internal methods — never allowed.
_FORBIDDEN_FIELD_PREFIXES = ("_", "sudo", "with_env", "with_context", "mapped")

# Suspicious patterns in string values that may indicate SQL injection attempts.
_SUSPICIOUS_PATTERNS = ("--", ";", "/*", "*/", "xp_", "exec(", "drop ", "union ")


def validate_domain(domain: list[Any]) -> None:
    """
    Validate an Odoo domain filter for safety.

    Checks:
    - Overall structure (list of tuples/lists or logical operators)
    - Valid operators only
    - No private/internal field names
    - No suspicious SQL patterns in string values

    Args:
        domain: Odoo domain filter (e.g. [('state', '=', 'draft')]).

    Raises:
        DomainInjectionError: If the domain is malformed or suspicious.
    """
    if not isinstance(domain, list):
        raise DomainInjectionError(
            f"Domain must be a list, got {type(domain).__name__}",
            user_message="Invalid search filter format.",
        )

    for element in domain:
        if isinstance(element, str):
            _validate_logical_operator(element)
        elif isinstance(element, (list, tuple)):
            _validate_condition(element)
        else:
            raise DomainInjectionError(
                f"Domain element must be list/tuple or string, got {type(element).__name__}",
                user_message="Invalid search filter element.",
            )


def _validate_logical_operator(op: str) -> None:
    """Validate a logical operator ('&', '|', '!')."""
    if op not in _LOGICAL_OPERATORS:
        raise DomainInjectionError(
            f"Invalid logical operator: {op!r}",
            user_message=f"Invalid search filter operator: {op!r}.",
        )


def _validate_condition(condition: list[Any] | tuple[Any, ...]) -> None:
    """Validate a single domain condition [field, operator, value]."""
    if len(condition) != 3:
        raise DomainInjectionError(
            f"Domain condition must have 3 elements, got {len(condition)}",
            user_message="Invalid search filter: each condition must be [field, operator, value].",
        )

    field, operator, value = condition

    if not isinstance(field, str):
        raise DomainInjectionError(
            f"Field name must be a string, got {type(field).__name__}",
            user_message="Invalid search filter: field name must be text.",
        )

    if not isinstance(operator, str):
        raise DomainInjectionError(
            f"Operator must be a string, got {type(operator).__name__}",
            user_message="Invalid search filter: operator must be text.",
        )

    # Check forbidden field prefixes
    for prefix in _FORBIDDEN_FIELD_PREFIXES:
        if field.startswith(prefix):
            raise DomainInjectionError(
                f"Forbidden field name prefix: {field!r}",
                user_message=f"Field '{field}' is not allowed in search filters.",
            )

    # Check valid operator
    if operator not in _VALID_OPERATORS:
        raise DomainInjectionError(
            f"Invalid operator: {operator!r}",
            user_message=f"Operator '{operator}' is not allowed in search filters.",
        )

    # Check for suspicious SQL patterns in string values
    _check_suspicious_value(value)


def _check_suspicious_value(value: Any) -> None:
    """Check a domain value for SQL injection patterns."""
    if isinstance(value, str):
        lower = value.lower()
        for pattern in _SUSPICIOUS_PATTERNS:
            if pattern in lower:
                raise DomainInjectionError(
                    f"Suspicious pattern in domain value: {pattern!r}",
                    user_message="Search filter value contains invalid characters.",
                )
    elif isinstance(value, (list, tuple)):
        for item in value:
            _check_suspicious_value(item)
