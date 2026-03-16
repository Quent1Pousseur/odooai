"""
Module: knowledge/schemas/models.py
Role: Schemas for Odoo model and field definitions.
Dependencies: pydantic
"""

from pydantic import BaseModel


class FieldDefinition(BaseModel, frozen=True):
    """Single field extracted from an Odoo model."""

    name: str
    type: str  # char, integer, many2one, selection, etc.
    string: str = ""  # Human-readable label
    required: bool = False
    readonly: bool = False
    store: bool = True  # False by default for computed without store=True
    compute: str | None = None  # Compute method name
    depends: list[str] = []  # @api.depends fields
    related: str | None = None  # Related field path (e.g. 'partner_id.name')
    relation: str | None = None  # Target model for relational fields
    selection: list[list[str]] | str = []  # [(key, label)] or method name
    default: str | None = None  # Default value expression
    help: str = ""  # Help text
    comodel_name: str | None = None  # Alias for relation (Odoo convention)
    inverse_name: str | None = None  # For One2many fields


class ModelDefinition(BaseModel, frozen=True):
    """Single Odoo model extracted from source code."""

    name: str  # Technical name (e.g. 'sale.order')
    description: str = ""  # _description
    inherit: list[str] = []  # _inherit (extension)
    inherits: dict[str, str] = {}  # _inherits (delegation: {parent_model: fk_field})
    is_transient: bool = False  # TransientModel (wizard)
    is_abstract: bool = False  # AbstractModel (mixin)
    is_extension: bool = False  # _inherit without _name (extending existing model)
    fields: dict[str, FieldDefinition] = {}
    order: str = ""  # _order
    rec_name: str = ""  # _rec_name
    table: str = ""  # _table (if custom)
