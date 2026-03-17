"""
Module: knowledge/business_extractor.py
Role: Reverse engineer business logic from Knowledge Graphs.
      Pure Python — ZERO LLM tokens. Extracts workflows, dependencies,
      field intents, and auto-generates Q&A pairs.
Dependencies: knowledge schemas
"""

from __future__ import annotations

import re

import structlog

from odooai.knowledge.schemas.business import (
    AutoQAPair,
    BusinessSummary,
    BusinessWorkflow,
    DependencyGraph,
    FieldIntent,
    ModelRelation,
    StateTransition,
)
from odooai.knowledge.schemas.index import ModuleKnowledgeGraph

logger = structlog.get_logger(__name__)

# Heuristic mapping: action method name → likely target state
_ACTION_STATE_MAP: dict[str, str] = {
    "action_confirm": "sale",
    "action_validate": "validated",
    "action_approve": "approved",
    "action_done": "done",
    "action_cancel": "cancel",
    "action_draft": "draft",
    "action_reset": "draft",
    "action_send": "sent",
    "action_post": "posted",
    "action_open": "open",
    "action_close": "close",
    "action_lock": "locked",
    "action_unlock": "draft",
    "button_confirm": "confirmed",
    "button_validate": "validated",
    "button_approve": "approved",
    "button_done": "done",
    "button_cancel": "cancel",
    "button_draft": "draft",
}

# Field name patterns → business intent
_INTENT_PATTERNS: list[tuple[str, str]] = [
    (r"^amount_|^price_|^margin|^cost_|^total", "finance"),
    (r"^date_|_date$|^scheduled_|^deadline|^commitment", "timeline"),
    (r"^state$|^stage_id$", "workflow"),
    (r"^partner_|^customer_|^vendor_|^supplier_", "relation"),
    (r"^tracking|^message_|^activity_", "audit"),
    (r"^compute|^_compute", "automation"),
    (r"^currency_|^company_", "multi-entity"),
    (r"^user_id$|^team_id$|^responsible", "assignment"),
]


def extract_business(
    kgs: list[ModuleKnowledgeGraph],
    domain_id: str,
) -> BusinessSummary:
    """
    Extract all business intelligence from KGs — ZERO LLM tokens.

    This is the reverse engineering engine: code → business logic.
    """
    workflows = _extract_workflows(kgs)
    graph = _extract_dependency_graph(kgs)
    intents = _classify_fields(kgs)
    qa = _generate_qa_pairs(kgs, workflows)

    logger.info(
        "Business extracted",
        domain=domain_id,
        workflows=len(workflows),
        relations=len(graph.relations),
        intents=len(intents),
        qa_pairs=len(qa),
    )

    return BusinessSummary(
        domain_id=domain_id,
        workflows=workflows,
        dependency_graph=graph,
        field_intents=intents,
        auto_qa=qa,
    )


def _extract_workflows(kgs: list[ModuleKnowledgeGraph]) -> list[BusinessWorkflow]:
    """Detect workflows from state fields + action methods."""
    workflows: list[BusinessWorkflow] = []

    for kg in kgs:
        for model in kg.models:
            if model.is_extension:
                continue

            # Find state field
            state_field = model.fields.get("state")
            if state_field is None or state_field.type != "selection":
                continue

            # Extract states
            states: list[str] = []
            if isinstance(state_field.selection, list):
                for item in state_field.selection:
                    if isinstance(item, list) and len(item) >= 1:
                        states.append(str(item[0]))
                    elif isinstance(item, str):
                        states.append(item)
            elif isinstance(state_field.selection, str):
                states = [state_field.selection]

            if not states:
                continue

            # Find action methods for this model
            transitions: list[StateTransition] = []
            model_actions = [a for a in kg.action_methods if a.model == model.name]
            for action in model_actions:
                target = _infer_target_state(action.name, states)
                if target:
                    transitions.append(
                        StateTransition(
                            from_state="*",
                            to_state=target,
                            method=action.name,
                            model=model.name,
                        )
                    )

            # Find timeline fields
            timeline: list[str] = [
                fname
                for fname, fdef in model.fields.items()
                if fdef.type in ("date", "datetime")
                and not fname.startswith(("create_", "write_", "__"))
            ]

            workflows.append(
                BusinessWorkflow(
                    model=model.name,
                    states=states,
                    transitions=transitions,
                    timeline_fields=timeline,
                    description=_describe_workflow(model.name, states),
                )
            )

    return workflows


def _infer_target_state(method_name: str, available_states: list[str]) -> str:
    """Infer the target state from an action method name."""
    # Direct mapping
    if method_name in _ACTION_STATE_MAP:
        target = _ACTION_STATE_MAP[method_name]
        if target in available_states:
            return target

    # Fuzzy: extract keyword from method name
    clean = method_name.replace("action_", "").replace("button_", "")
    for state in available_states:
        if state in clean or clean in state:
            return state

    return ""


def _describe_workflow(model_name: str, states: list[str]) -> str:
    """Auto-describe a workflow."""
    chain = " → ".join(states)
    return f"{model_name} passe par : {chain}"


def _extract_dependency_graph(
    kgs: list[ModuleKnowledgeGraph],
) -> DependencyGraph:
    """Build the dependency graph from relational fields."""
    relations: list[ModelRelation] = []
    extensions: list[str] = []
    computed: dict[str, list[str]] = {}

    for kg in kgs:
        for model in kg.models:
            if model.is_extension:
                extensions.append(model.name)

            model_computed: list[str] = []
            for fname, fdef in model.fields.items():
                # Relational fields
                if fdef.type in ("many2one", "one2many", "many2many") and fdef.relation:
                    relations.append(
                        ModelRelation(
                            source=model.name,
                            target=fdef.relation,
                            field=fname,
                            type=fdef.type,
                            required=fdef.required,
                        )
                    )

                # Computed fields
                if fdef.compute:
                    model_computed.append(fname)

            if model_computed:
                computed[model.name] = model_computed

    return DependencyGraph(
        relations=relations,
        extensions=extensions,
        computed_fields=computed,
    )


def _classify_fields(kgs: list[ModuleKnowledgeGraph]) -> list[FieldIntent]:
    """Classify fields by business intent using heuristics."""
    intents: list[FieldIntent] = []

    for kg in kgs:
        for model in kg.models:
            if model.is_extension and len(model.fields) < 3:
                continue

            for fname, fdef in model.fields.items():
                intent = _detect_intent(fname, fdef)
                if intent:
                    intents.append(
                        FieldIntent(
                            name=fname,
                            model=model.name,
                            type=fdef.type,
                            intent=intent,
                        )
                    )

    return intents


def _detect_intent(fname: str, fdef: object) -> str:
    """Detect business intent from field name and metadata."""
    for pattern, intent in _INTENT_PATTERNS:
        if re.search(pattern, fname):
            return intent

    # Check field properties
    if hasattr(fdef, "required") and getattr(fdef, "required", False):
        return "critical"
    if hasattr(fdef, "compute") and bool(getattr(fdef, "compute", None)):
        return "automation"

    return ""


def _generate_qa_pairs(
    kgs: list[ModuleKnowledgeGraph],
    workflows: list[BusinessWorkflow],
) -> list[AutoQAPair]:
    """Generate Q&A pairs from KG data — ZERO LLM tokens."""
    qa: list[AutoQAPair] = []

    for wf in workflows:
        model = wf.model
        # Find the KG model to get field info
        model_def = None
        for kg in kgs:
            for m in kg.models:
                if m.name == model and not m.is_extension:
                    model_def = m
                    break

        if model_def is None:
            continue

        # Q&A for each state
        for state in wf.states:
            qa.append(
                AutoQAPair(
                    question=f"Combien de {model} en etat '{state}' ?",
                    model=model,
                    domain_filter=f"[('state','=','{state}')]",
                    fields=["name", "state"],
                    method="search_count",
                )
            )

        # Q&A for overdue items (if timeline fields exist)
        for date_field in wf.timeline_fields:
            qa.append(
                AutoQAPair(
                    question=f"Quels {model} sont en retard ({date_field}) ?",
                    model=model,
                    domain_filter=f"[('state','not in',['done','cancel']),("
                    f"'{date_field}','<',fields.Date.today())]",
                    fields=_best_fields(model_def),
                    method="search_read",
                )
            )

        # Q&A for financial totals
        finance_fields = [
            fname
            for fname, fdef in model_def.fields.items()
            if fdef.type in ("monetary", "float")
            and ("amount" in fname or "total" in fname or "price" in fname)
        ]
        for ff in finance_fields[:2]:
            qa.append(
                AutoQAPair(
                    question=f"Quel est le total de {ff} pour {model} ?",
                    model=model,
                    domain_filter="[('state','not in',['cancel'])]",
                    fields=[ff],
                    method="read_group",
                    groupby="state",
                )
            )

        # Q&A for top records
        partner_field = next(
            (
                fname
                for fname, fdef in model_def.fields.items()
                if fdef.type == "many2one" and "partner" in fname
            ),
            None,
        )
        if partner_field and finance_fields:
            qa.append(
                AutoQAPair(
                    question=f"Top clients par {finance_fields[0]} sur {model} ?",
                    model=model,
                    domain_filter="[('state','not in',['cancel'])]",
                    fields=[finance_fields[0]],
                    method="read_group",
                    groupby=partner_field,
                )
            )

    return qa


def _best_fields(model_def: object) -> list[str]:
    """Return the most useful fields for display."""
    priority = ["name", "partner_id", "state", "amount_total", "date_order"]
    result: list[str] = []
    fields = getattr(model_def, "fields", {})
    for p in priority:
        if p in fields:
            result.append(p)
    if len(result) < 5:
        for fname in list(fields.keys())[:10]:
            if fname not in result and not fname.startswith(("_", "message_", "activity_")):
                result.append(fname)
            if len(result) >= 5:
                break
    return result
