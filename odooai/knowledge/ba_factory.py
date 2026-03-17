"""
Module: knowledge/ba_factory.py
Role: Generate BA Profiles from Knowledge Graphs using LLM.
Dependencies: anthropic, knowledge schemas
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from typing import Any

import structlog

from odooai.knowledge._ba_prompt import build_ba_messages, build_kg_summary
from odooai.knowledge.schemas.ba_profile import (
    BAProfile,
    DomainCapability,
    FeatureDiscovery,
    Gotcha,
    QAPair,
    RecommendedConfig,
    Workflow,
)
from odooai.knowledge.schemas.index import ModuleKnowledgeGraph

logger = structlog.get_logger(__name__)

DOMAINS: dict[str, list[str]] = {
    "sales_crm": ["sale", "crm", "sale_management", "sale_subscription"],
    "supply_chain": ["stock", "purchase", "stock_landed_costs", "delivery"],
    "manufacturing": ["mrp", "mrp_workorder", "quality", "quality_control"],
    "accounting": ["account", "account_payment", "account_bank_statement"],
    "hr_payroll": ["hr", "hr_contract", "hr_payslip", "hr_expense", "hr_holidays"],
    "project_services": ["project", "hr_timesheet", "planning"],
    "helpdesk": ["helpdesk", "rating"],
    "ecommerce": ["website_sale", "website", "payment"],
    "pos": ["point_of_sale"],
}

DOMAIN_NAMES: dict[str, str] = {
    "sales_crm": "Ventes & CRM",
    "supply_chain": "Supply Chain",
    "manufacturing": "Fabrication",
    "accounting": "Comptabilite & Finance",
    "hr_payroll": "RH & Paie",
    "project_services": "Projets & Services",
    "helpdesk": "Helpdesk",
    "ecommerce": "E-commerce",
    "pos": "Point de Vente",
}


async def generate_ba_profile(
    domain_id: str,
    kgs: list[ModuleKnowledgeGraph],
    anthropic_api_key: str,
    language: str = "fr",
    model: str = "claude-sonnet-4-20250514",
) -> BAProfile:
    """Generate a BA Profile for a functional domain using LLM."""
    import anthropic

    domain_name = DOMAIN_NAMES.get(domain_id, domain_id)
    modules_covered = [kg.manifest.technical_name for kg in kgs]
    kg_summary = build_kg_summary(kgs)

    logger.info("Generating BA Profile", domain=domain_id, modules=modules_covered)

    all_messages = build_ba_messages(domain_name, domain_id, kg_summary, language)
    # Anthropic API: system is a top-level param, not a message role
    system_msg = next((m["content"] for m in all_messages if m["role"] == "system"), "")
    user_messages = [m for m in all_messages if m["role"] != "system"]

    client = anthropic.Anthropic(api_key=anthropic_api_key)
    response = client.messages.create(
        model=model,
        max_tokens=4096,
        system=system_msg,
        messages=user_messages,  # type: ignore[arg-type]
    )

    # Extract text from response (first TextBlock)
    raw_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            raw_text = block.text
            break
    tokens = response.usage.input_tokens + response.usage.output_tokens
    logger.info("BA Profile generated", domain=domain_id, tokens=tokens)

    data = _parse_llm_json(raw_text)
    # Parse recommended_config
    rc_data = data.get("recommended_config", {})
    rec_config = (
        RecommendedConfig(
            small_company=str(rc_data.get("small_company", "")),
            medium_company=str(rc_data.get("medium_company", "")),
            large_company=str(rc_data.get("large_company", "")),
        )
        if rc_data
        else None
    )

    return BAProfile(
        domain_name=domain_name,
        domain_id=domain_id,
        modules_covered=modules_covered,
        language=language,
        summary=data.get("summary", ""),
        workflows=[_to_workflow(w) for w in data.get("workflows", [])],
        capabilities=[_to_capability(c) for c in data.get("capabilities", [])],
        feature_discoveries=[_to_feature(f) for f in data.get("feature_discoveries", [])],
        qa_pairs=[_to_qa(q) for q in data.get("qa_pairs", [])],
        gotchas=[_to_gotcha(g) for g in data.get("gotchas", [])],
        recommended_config=rec_config,
        cross_module_combos=data.get("cross_module_combos", []),
        limitations=data.get("limitations", []),
        odoo_version="17.0",
        generated_at=datetime.now(UTC).isoformat(),
        model_used=model,
        token_count=tokens,
    )


def _parse_llm_json(text: str) -> dict[str, Any]:
    """Parse JSON from LLM response, handling markdown fences."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [ln for ln in lines if not ln.strip().startswith("```")]
        cleaned = "\n".join(lines)
    try:
        return json.loads(cleaned)  # type: ignore[no-any-return]
    except json.JSONDecodeError:
        logger.error("Failed to parse LLM JSON", text=cleaned[:500])
        return {}


def _to_workflow(d: dict[str, Any]) -> Workflow:
    return Workflow(
        name=str(d.get("name", "")),
        description=str(d.get("description", "")),
        steps=d.get("steps", []),
        models_involved=d.get("models_involved", []),
        key_fields_per_step=d.get("key_fields_per_step", {}),
    )


def _to_qa(d: dict[str, Any]) -> QAPair:
    return QAPair(
        question=str(d.get("question", "")),
        answer=str(d.get("answer", "")),
        models_to_query=d.get("models_to_query", []),
        fields_to_fetch=d.get("fields_to_fetch", []),
        domain_filter_example=str(d.get("domain_filter_example", "")),
    )


def _to_capability(d: dict[str, Any]) -> DomainCapability:
    return DomainCapability(
        name=str(d.get("name", "")),
        description=str(d.get("description", "")),
        key_models=d.get("key_models", []),
        common_workflows=d.get("common_workflows", []),
    )


def _to_feature(d: dict[str, Any]) -> FeatureDiscovery:
    return FeatureDiscovery(
        name=str(d.get("name", "")),
        module=str(d.get("module", "")),
        model=str(d.get("model", "")),
        field_or_setting=str(d.get("field_or_setting", "")),
        description=str(d.get("description", "")),
        business_value=str(d.get("business_value", "")),
        how_to_activate=str(d.get("how_to_activate", "")),
        prerequisites=d.get("prerequisites", []),
        complexity=str(d.get("complexity", "simple")),
    )


def _to_gotcha(d: dict[str, Any]) -> Gotcha:
    return Gotcha(
        description=str(d.get("description", "")),
        source_model=str(d.get("source_model", "")),
        source_constraint=str(d.get("source_constraint", "")),
        workaround=str(d.get("workaround", "")),
    )
