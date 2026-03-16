# OdooAI — Contributing Guidelines

## Language Rules

### Code : ENGLISH ONLY
- All variable names, function names, class names : English
- All comments : English
- All commit messages : English
- All spec documents : English
- All PR descriptions : English

### Governance docs : FRENCH
- Project docs (MANIFESTO, WORKFLOW, etc.) : French (primary market language)
- Agent profiles : French
- Meeting notes : French
- These may be translated to English later for international team members

```python
# GOOD
def calculate_token_cost(model: str, tokens_in: int, tokens_out: int) -> float:
    """Calculate the cost in dollars for a given LLM request."""
    ...

# BAD
def calculer_cout_token(modele: str, tokens_entree: int, tokens_sortie: int) -> float:
    """Calcule le cout en dollars pour une requete LLM."""
    ...
```

### User-facing content : Multilingual
- UI text, emails, documentation for users → managed by i18n Lead
- Default language : French first (primary market), English second
- All user-facing strings must go through the i18n framework (never hardcoded)

## Code Standards

### Python (Backend)
```
Python version    : 3.11+
Formatter         : ruff format
Linter            : ruff check
Type checker      : mypy --strict
Line length       : 100 characters max
File length       : 300 lines max (split if longer)
Function length   : 50 lines max
```

### Naming Conventions
```
Files             : snake_case.py
Classes           : PascalCase
Functions         : snake_case
Variables         : snake_case
Constants         : UPPER_SNAKE_CASE
Private           : _leading_underscore
Type aliases      : PascalCase
Enums             : PascalCase (members: UPPER_SNAKE_CASE)
```

### Type Hints
```python
# MANDATORY on all public functions
def search_read(
    self,
    api_key: str,
    model: str,
    domain: list,
    fields: list[str],
    limit: int = 10,
) -> list[dict[str, Any]]:
    ...

# Any is allowed ONLY for dynamic Odoo responses
# All value objects : frozen dataclasses with type hints
```

### Comments

Every file MUST start with a module docstring :
```python
"""
Module: services/field_scorer.py
Role: Score and select the most useful Odoo fields for LLM consumption.
Dependencies: none (pure Python)
"""
```

Every public class and function MUST have a docstring :
```python
def select_top_fields(fields_meta: dict[str, dict], top_n: int = 15) -> list[str]:
    """
    Select the top N most useful fields from an Odoo model's fields_get() result.

    Always includes 'id'. Excludes binary, html, o2m, m2m, and noise fields.

    Args:
        fields_meta: Full fields_get() result from Odoo.
        top_n: Maximum number of fields to return.

    Returns:
        List of field names, sorted by descending score, capped at top_n.
    """
```

Inline comments : ONLY when the logic is not self-evident :
```python
# GOOD — explains WHY, not WHAT
# Odoo returns many2one as [id, display_name] tuples — normalize to dict
if isinstance(value, (list, tuple)) and len(value) == 2:
    return {"id": value[0], "name": value[1]}

# BAD — states the obvious
# Check if value is a list
if isinstance(value, list):
```

### Imports
```python
# Order: stdlib → third-party → local
# Always absolute imports, never relative
# Group with blank lines between groups

import os
from dataclasses import dataclass
from enum import StrEnum

import httpx
import structlog

from odooai.config import get_settings
from odooai.domain.value_objects.model_category import ModelCategory
```

### Error Handling
```python
# ALWAYS use typed exceptions from exceptions.py
# ALWAYS provide user_message (safe for LLM display)
raise BlockedModelError(
    message=f"Model {model} is in BLOCKED set",
    user_message=f"Model '{model}' is permanently blocked for security reasons.",
)

# NEVER catch bare Exception unless re-raising
# NEVER swallow errors silently
```

### Data Immutability
```python
# Value objects : ALWAYS frozen
@dataclass(frozen=True)
class ResolvedPolicy:
    deny_access: bool = False
    allowed_fields: tuple[str, ...] = ()
    ...

# NEVER use mutable default arguments
# NEVER modify a frozen object (use object.__setattr__ only in __post_init__)
```

## Frontend Standards (TypeScript)
```
Framework         : Next.js 14+ (App Router)
Language          : TypeScript (strict mode)
Formatter         : Prettier
Linter            : ESLint
Styling           : Tailwind CSS
Components        : Shadcn/ui
Tests             : Vitest + Testing Library
```

## CI Enforcement

All standards are enforced automatically in CI. A PR CANNOT be merged if :
- [ ] ruff lint fails
- [ ] mypy fails
- [ ] Tests fail
- [ ] ESLint/Prettier fail (frontend)
- [ ] Commit message format is wrong
- [ ] No spec ID in commit
- [ ] File > 300 lines without justification
