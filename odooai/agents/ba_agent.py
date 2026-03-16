"""
Module: agents/ba_agent.py
Role: Business Analyst agent — answers questions using BA Profiles.
      Receives a question + BA Profile context, calls the LLM,
      returns a structured response with sources and actions.
Dependencies: anthropic, knowledge schemas
"""

from __future__ import annotations

from dataclasses import dataclass, field

import structlog

from odooai.knowledge.schemas.ba_profile import BAProfile

logger = structlog.get_logger(__name__)

SYSTEM_PROMPT = """Tu es OdooAI, un Business Analyst expert Odoo.
Tu aides les dirigeants et responsables de PME a mieux utiliser Odoo.

Regles absolues :
- Reponds en francais
- Cite toujours la source (module, modele, champ) quand tu fais une recommandation
- Si tu n'es pas sur, dis-le explicitement
- Ne donne JAMAIS de conseil juridique, fiscal ou comptable
- Propose des actions concretes avec le niveau de complexite (simple/moyen/complexe)
- Sois concis : pas plus de 3 paragraphes sauf si la question est complexe

Contexte : tu as acces aux Knowledge Graphs d'Odoo 17 qui decrivent chaque module,
modele, champ et contrainte. Tu bases tes reponses sur ces donnees factuelles."""

DISCLAIMER = (
    "\n\n---\n*OdooAI ne fournit pas de conseil juridique, fiscal ou comptable. "
    "Consultez un professionnel qualifie pour ces domaines.*"
)


@dataclass
class AgentResponse:
    """Response from the BA Agent."""

    answer: str
    domain: str
    sources: list[str] = field(default_factory=list)
    tokens_used: int = 0


async def ask_ba_agent(
    question: str,
    profile: BAProfile,
    anthropic_api_key: str,
    model: str = "claude-sonnet-4-20250514",
) -> AgentResponse:
    """
    Ask a question to the BA Agent with BA Profile context.

    Args:
        question: User's question in natural language.
        profile: BA Profile for the relevant domain.
        anthropic_api_key: Anthropic API key.
        model: LLM model to use.

    Returns:
        AgentResponse with answer, sources, and token usage.
    """
    import anthropic

    context = _build_profile_context(profile)

    user_message = f"""Contexte du domaine "{profile.domain_name}" :

{context}

Question de l'utilisateur :
{question}"""

    client = anthropic.Anthropic(api_key=anthropic_api_key)
    response = client.messages.create(
        model=model,
        max_tokens=2048,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_message}],
    )

    raw_text = ""
    for block in response.content:
        if hasattr(block, "text"):
            raw_text = block.text
            break

    tokens = response.usage.input_tokens + response.usage.output_tokens

    logger.info(
        "BA Agent responded",
        domain=profile.domain_id,
        tokens=tokens,
        answer_length=len(raw_text),
    )

    return AgentResponse(
        answer=raw_text + DISCLAIMER,
        domain=profile.domain_id,
        sources=profile.modules_covered,
        tokens_used=tokens,
    )


def _build_profile_context(profile: BAProfile) -> str:
    """Build a concise context string from a BA Profile for the LLM."""
    parts: list[str] = []

    parts.append(f"Domaine : {profile.domain_name}")
    parts.append(f"Modules : {', '.join(profile.modules_covered)}")
    parts.append(f"\nResume : {profile.summary}")

    if profile.capabilities:
        parts.append("\nCapacites :")
        for c in profile.capabilities:
            parts.append(f"  - {c.name} : {c.description}")

    if profile.feature_discoveries:
        parts.append("\nFonctionnalites a decouvrir :")
        for f in profile.feature_discoveries:
            parts.append(f"  - {f.name} ({f.module}.{f.model})")
            parts.append(f"    Valeur : {f.business_value}")
            parts.append(f"    Comment : {f.how_to_activate}")

    if profile.gotchas:
        parts.append("\nPieges connus :")
        for g in profile.gotchas:
            parts.append(f"  - {g.description}")
            if g.workaround:
                parts.append(f"    Solution : {g.workaround}")

    if profile.cross_module_combos:
        parts.append("\nCombos cross-modules :")
        for combo in profile.cross_module_combos:
            parts.append(f"  - {combo}")

    if profile.limitations:
        parts.append("\nLimitations :")
        for lim in profile.limitations:
            parts.append(f"  - {lim}")

    return "\n".join(parts)
