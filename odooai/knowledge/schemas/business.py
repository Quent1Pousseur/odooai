"""
Module: knowledge/schemas/business.py
Role: Business intelligence structures extracted from KG WITHOUT LLM.
      Pure Python reverse engineering of Odoo business logic.
Dependencies: pydantic
"""

from __future__ import annotations

from pydantic import BaseModel


class StateTransition(BaseModel, frozen=True):
    """A state transition inferred from action methods."""

    from_state: str  # Inferred source state (or "*" if unknown)
    to_state: str  # Inferred target state
    method: str  # action_confirm, action_cancel, etc.
    model: str  # sale.order, stock.picking, etc.


class BusinessWorkflow(BaseModel, frozen=True):
    """A workflow extracted from state fields + action methods."""

    model: str  # sale.order
    states: list[str]  # [draft, sent, sale, done, cancel]
    transitions: list[StateTransition] = []
    timeline_fields: list[str] = []  # date_order, commitment_date, etc.
    description: str = ""  # Auto-generated description


class ModelRelation(BaseModel, frozen=True):
    """A relationship between two models."""

    source: str  # sale.order
    target: str  # res.partner
    field: str  # partner_id
    type: str  # many2one, one2many, many2many
    required: bool = False


class DependencyGraph(BaseModel, frozen=True):
    """Graph of model dependencies for a domain."""

    relations: list[ModelRelation] = []
    extensions: list[str] = []  # Models extended via _inherit
    computed_fields: dict[str, list[str]] = {}  # model → [computed field names]


class FieldIntent(BaseModel, frozen=True):
    """A field classified by business intent."""

    name: str
    model: str
    type: str
    intent: str  # finance, timeline, workflow, relation, audit, automation, security, critical


class AutoQAPair(BaseModel, frozen=True):
    """A Q&A pair auto-generated from KG (0 LLM tokens)."""

    question: str
    model: str
    domain_filter: str  # e.g. "[('state','=','draft')]"
    fields: list[str]  # Fields to fetch
    method: str = "search_read"  # search_read, search_count, read_group
    groupby: str = ""  # For read_group


class BusinessSummary(BaseModel, frozen=True):
    """Complete business intelligence for a domain — extracted without LLM."""

    domain_id: str
    workflows: list[BusinessWorkflow] = []
    dependency_graph: DependencyGraph = DependencyGraph()
    field_intents: list[FieldIntent] = []
    auto_qa: list[AutoQAPair] = []
