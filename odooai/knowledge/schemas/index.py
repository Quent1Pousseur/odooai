"""
Module: knowledge/schemas/index.py
Role: Schemas for Knowledge Graph version-level index.
Dependencies: pydantic
"""

from pydantic import BaseModel

from odooai.knowledge.schemas.actions import ActionMethod
from odooai.knowledge.schemas.constraints import OnchangeMethod, PythonConstraint, SqlConstraint
from odooai.knowledge.schemas.manifest import ModuleManifest
from odooai.knowledge.schemas.menus import MenuItem
from odooai.knowledge.schemas.models import ModelDefinition
from odooai.knowledge.schemas.security import AccessRight, RecordRule, SecurityGroup
from odooai.knowledge.schemas.views import ViewDefinition


class ModuleKnowledgeGraph(BaseModel, frozen=True):
    """Complete Knowledge Graph for a single Odoo module."""

    manifest: ModuleManifest
    models: list[ModelDefinition] = []
    sql_constraints: list[SqlConstraint] = []
    python_constraints: list[PythonConstraint] = []
    onchange_methods: list[OnchangeMethod] = []
    action_methods: list[ActionMethod] = []
    access_rights: list[AccessRight] = []
    record_rules: list[RecordRule] = []
    security_groups: list[SecurityGroup] = []
    views: list[ViewDefinition] = []
    menus: list[MenuItem] = []


class ModuleEntry(BaseModel, frozen=True):
    """Entry in the version-level index."""

    technical_name: str
    path: str
    analyzed_at: str  # ISO datetime
    model_count: int = 0
    field_count: int = 0
    success: bool = True
    error: str = ""  # Error message if parsing failed (best-effort)


class KnowledgeIndex(BaseModel, frozen=True):
    """Version-level index of all analyzed modules."""

    odoo_version: str
    generated_at: str  # ISO datetime
    modules: list[ModuleEntry] = []
    total_models: int = 0
    total_fields: int = 0
