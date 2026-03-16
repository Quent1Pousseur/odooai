"""
Module: security/anonymizer.py
Role: Field-level anonymization for sensitive Odoo data before LLM exposure.
      Pure logic, ZERO LLM dependency.
Dependencies: none (pure Python)
"""

from __future__ import annotations

import math
import re


def mask_email(email: str) -> str:
    """
    Mask an email address: j***@domain.com.

    Args:
        email: Raw email string.

    Returns:
        Masked email or the original string if not a valid email format.
    """
    if "@" not in email:
        return email
    local, domain = email.rsplit("@", 1)
    if len(local) <= 1:
        return f"*@{domain}"
    return f"{local[0]}***@{domain}"


def mask_name(name: str) -> str:
    """
    Mask a person's name: J*** D***.

    Args:
        name: Raw name string.

    Returns:
        Masked name with only first letter of each word visible.
    """
    if not name:
        return name
    parts = name.split()
    masked = []
    for part in parts:
        if len(part) <= 1:
            masked.append(part)
        else:
            masked.append(f"{part[0]}***")
    return " ".join(masked)


def round_amount(amount: float, precision: int = 100) -> float:
    """
    Round a monetary amount to the nearest precision (default: nearest 100).

    45780.50 -> 45800.0

    Args:
        amount: Raw monetary value.
        precision: Rounding precision (default 100).

    Returns:
        Rounded amount.
    """
    return float(math.ceil(amount / precision) * precision)


def mask_phone(phone: str) -> str:
    """
    Mask a phone number, keeping only the last 2 digits.

    Args:
        phone: Raw phone string.

    Returns:
        Masked phone: ***XX.
    """
    digits = re.sub(r"[^\d]", "", phone)
    if len(digits) <= 2:
        return "***"
    return f"***{digits[-2:]}"


def redact(_value: object) -> str:
    """
    Completely redact a value (for confidential fields).

    Returns:
        The string '[REDACTED]'.
    """
    return "[REDACTED]"
