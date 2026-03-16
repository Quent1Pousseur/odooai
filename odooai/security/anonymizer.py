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
    Mask an email address: j***@c***.com.

    Both local part and domain name are masked to prevent company identification.

    Args:
        email: Raw email string.

    Returns:
        Masked email or the original string if not a valid email format.
    """
    if "@" not in email:
        return email
    local, domain = email.rsplit("@", 1)
    masked_local = f"{local[0]}***" if len(local) > 1 else "*"
    # Mask domain name but keep TLD (.com, .fr, etc.)
    domain_parts = domain.rsplit(".", 1)
    if len(domain_parts) == 2:
        domain_name, tld = domain_parts
        masked_domain = f"{domain_name[0]}***.{tld}" if domain_name else f"***.{tld}"
    else:
        masked_domain = f"{domain[0]}***" if domain else "***"
    return f"{masked_local}@{masked_domain}"


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


# ──────────────────────────────────────────────────────────────
# Field-name-based anonymization rules for SENSITIVE models
# ──────────────────────────────────────────────────────────────

# Patterns: if field name contains any of these substrings, apply the method.
_AMOUNT_PATTERNS = ("amount", "price", "cost", "total", "salary", "wage", "balance")
_EMAIL_PATTERNS = ("email",)
_PHONE_PATTERNS = ("phone", "mobile", "fax")
_NAME_PATTERNS_HR = ("name",)  # Only on HR models


def anonymize_field_value(
    field_name: str,
    value: object,
    model: str = "",
) -> object:
    """
    Anonymize a single field value based on field name patterns.

    Args:
        field_name: Odoo field name.
        value: Raw field value.
        model: Odoo model name (used for HR-specific rules).

    Returns:
        Anonymized value, or original if no rule matches.
    """
    lower = field_name.lower()

    if any(p in lower for p in _AMOUNT_PATTERNS):
        if isinstance(value, (int, float)):
            return round_amount(float(value))
        return value

    if any(p in lower for p in _EMAIL_PATTERNS):
        if isinstance(value, str):
            return mask_email(value)
        return value

    if any(p in lower for p in _PHONE_PATTERNS):
        if isinstance(value, str):
            return mask_phone(value)
        return value

    # Mask names on ALL SENSITIVE models (prevents prompt injection via names)
    sensitive_name_prefixes = ("hr.", "res.partner", "account.", "mail.message")
    if any(model.startswith(p) for p in sensitive_name_prefixes) and any(
        p in lower for p in _NAME_PATTERNS_HR
    ):
        if isinstance(value, str):
            return mask_name(value)
        return value

    return value


def anonymize_record(
    record: dict[str, object],
    model: str,
) -> dict[str, object]:
    """
    Anonymize all sensitive fields in a single Odoo record.

    Args:
        record: Raw Odoo record dict.
        model: Odoo model name.

    Returns:
        New dict with sensitive fields anonymized.
    """
    return {field: anonymize_field_value(field, value, model) for field, value in record.items()}
