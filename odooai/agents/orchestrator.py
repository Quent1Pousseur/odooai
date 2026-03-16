"""
Module: agents/orchestrator.py
Role: Route user questions to the appropriate BA Agent.
      Sprint 1: simple domain detection + single BA Agent.
      Sprint 2: multi-agent routing, intent classification.
Dependencies: agents/ba_agent, knowledge/storage
"""

from __future__ import annotations

from pathlib import Path

import structlog

from odooai.agents.ba_agent import AgentResponse, ask_ba_agent
from odooai.knowledge.ba_factory import DOMAIN_NAMES
from odooai.knowledge.schemas.ba_profile import BAProfile

logger = structlog.get_logger(__name__)

# Keywords to domain mapping for simple intent detection
_DOMAIN_KEYWORDS: dict[str, list[str]] = {
    "sales_crm": ["vente", "devis", "commande", "client", "crm", "pipeline", "opportunite", "sale"],
    "supply_chain": [
        "stock",
        "inventaire",
        "entrepot",
        "livraison",
        "achat",
        "fournisseur",
        "reception",
    ],
    "manufacturing": [
        "fabrication",
        "production",
        "nomenclature",
        "bom",
        "mrp",
        "ordre de fabrication",
    ],
    "accounting": [
        "comptabilite",
        "facture",
        "paiement",
        "avoir",
        "relance",
        "journal",
        "ecriture",
    ],
    "hr_payroll": ["employe", "conge", "paie", "salaire", "contrat", "absence", "rh", "ressource"],
    "project_services": ["projet", "tache", "timesheet", "feuille de temps", "planning"],
    "helpdesk": ["ticket", "support", "helpdesk", "sla", "assistance"],
    "ecommerce": ["site web", "e-commerce", "boutique", "panier", "catalogue"],
    "pos": ["caisse", "point de vente", "pos", "terminal"],
}


def detect_domain(question: str) -> str | None:
    """
    Detect the most likely domain for a question using keyword matching.

    Sprint 1: simple keyword matching. Sprint 2: LLM-based classification.

    Args:
        question: User's question in natural language.

    Returns:
        Domain ID or None if no match.
    """
    lower = question.lower()
    scores: dict[str, int] = {}

    for domain_id, keywords in _DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw in lower)
        if score > 0:
            scores[domain_id] = score

    if not scores:
        return None

    return max(scores, key=scores.get)  # type: ignore[arg-type]


def load_ba_profile(
    domain_id: str,
    version: str = "17.0",
    store_path: Path | None = None,
) -> BAProfile | None:
    """
    Load a stored BA Profile from knowledge_store.

    Args:
        domain_id: Domain identifier (e.g. "sales_crm").
        version: Odoo version.
        store_path: Override store path (for testing).

    Returns:
        BAProfile or None if not found.
    """
    import json

    # Validate domain_id to prevent path traversal
    if domain_id not in DOMAIN_NAMES:
        logger.warning("Invalid domain_id", domain=domain_id)
        return None

    path = store_path or Path("knowledge_store")
    profile_file = path / version / "_ba_profiles" / f"{domain_id}.json"

    if not profile_file.exists():
        logger.warning("BA Profile not found", domain=domain_id, path=str(profile_file))
        return None

    try:
        data = json.loads(profile_file.read_text(encoding="utf-8"))
        return BAProfile.model_validate(data)
    except Exception as exc:
        logger.error("Failed to load BA Profile", domain=domain_id, error=str(exc))
        return None


async def handle_question(
    question: str,
    anthropic_api_key: str,
    version: str = "17.0",
    model: str = "claude-sonnet-4-20250514",
) -> AgentResponse:
    """
    Handle a user question end-to-end.

    Flow: detect domain → load BA Profile → call BA Agent → return response.

    Args:
        question: User's question.
        anthropic_api_key: Anthropic API key.
        version: Odoo version for KG/BA lookup.
        model: LLM model.

    Returns:
        AgentResponse with answer.
    """
    # Step 1: Detect domain
    domain_id = detect_domain(question)

    if domain_id is None:
        # Fallback: use sales_crm as default (most common)
        domain_id = "sales_crm"
        logger.info("No domain detected, defaulting to sales_crm", question=question[:100])
    else:
        domain_name = DOMAIN_NAMES.get(domain_id, domain_id)
        logger.info("Domain detected", domain=domain_id, name=domain_name)

    # Step 2: Load BA Profile
    profile = load_ba_profile(domain_id, version)

    if profile is None:
        return AgentResponse(
            answer=f"Le profil BA pour le domaine '{domain_id}' n'est pas disponible. "
            f"Generez-le avec : odooai generate-ba {domain_id} --save",
            domain=domain_id,
        )

    # Step 3: Call BA Agent
    return await ask_ba_agent(question, profile, anthropic_api_key, model)
