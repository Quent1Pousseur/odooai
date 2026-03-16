"""
Module: domain/value_objects/sanitized_response.py
Role: Immutable container for Odoo data after security filtering and anonymization.
Dependencies: none (pure Python)
"""

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class SanitizedResponse:
    """Records that have passed through the Security Guardian pipeline."""

    model: str
    records: tuple[dict[str, Any], ...] = field(default_factory=tuple)
    fields_returned: tuple[str, ...] = field(default_factory=tuple)
    record_count: int = 0
    was_anonymized: bool = False
