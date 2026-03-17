"""
Module: agents/ba_agent.py
Role: Business Analyst agent — answers questions using BA Profiles + tool-use.
      When connected to a live Odoo, the LLM can call tools to query data.
Dependencies: anthropic, knowledge schemas, _tools
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import structlog

from odooai.knowledge.schemas.ba_profile import BAProfile

logger = structlog.get_logger(__name__)

SYSTEM_PROMPT = """Tu es un expert Odoo. Reponds en francais.

REGLE #1 — CONVERSATIONNEL :
Tu travailles EN BINOME avec l'utilisateur. C'est un dialogue.
- Si l'utilisateur demande de creer/modifier quelque chose,
  DEMANDE les details manquants AVANT d'agir.
- Ne cree JAMAIS un record avec des donnees inventees.
- Confirme toujours avant d'ecrire dans Odoo.
- Propose des choix quand c'est pertinent.

Exemple :
User: "Cree-moi un devis"
Toi: "Pour quel client ? Et quels produits ?"
User: "Dupont, 10 produits A"
Toi: [cherche le client et le produit avec les outils]
Toi: "Dupont SARL (ID 42), Produit A a 150€. Total 1500€ HT.
      Je cree le devis ?"
User: "Oui"
Toi: [cree le devis]

REGLE #2 — OUTILS :
- Utilise tes outils pour chercher les VRAIES donnees
- odoo_fields_get AVANT search_read si tu doutes des champs
- Si un outil echoue, adapte et reessaie
- Tu peux lire, compter, grouper, creer, modifier

REGLE #3 — FORMAT :
- Tableaux markdown pour les donnees
- Direct, pas de preambule
- Pour les audits/dashboards, genere un bloc :
```dashboard
{"title":"T","kpis":[{"label":"N","value":42,"icon":"📊",
"format":"number","color":"blue"}],
"bars":[{"label":"L","value":75,"max":100}],
"alerts":["A"]}
```"""

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
    odoo_client: Any | None = None,
    odoo_uid: int = 0,
    odoo_api_key: str = "",
    max_tools: int = 10,
) -> AgentResponse:
    """
    Ask a question with BA Profile context + optional tool-use for live data.

    If odoo_client is provided, the LLM can call tools to query the instance.
    """
    import anthropic

    from odooai.agents._tools import TOOL_DEFINITIONS, execute_tool

    context = _build_profile_context(profile, question=question)
    user_message = f"""Contexte du domaine "{profile.domain_name}" :

{context}

Question de l'utilisateur :
{question}"""

    client = anthropic.Anthropic(api_key=anthropic_api_key)

    # Use tools only if connected to live Odoo
    tools = TOOL_DEFINITIONS if odoo_client is not None else []

    messages: list[dict[str, Any]] = [{"role": "user", "content": user_message}]
    total_tokens = 0
    max_token_budget = 50000  # Stop if token budget exceeded

    # Tool-use loop
    tool_calls_made = 0
    for _i in range(max_tools + 1):
        if total_tokens > max_token_budget:
            logger.warning("Token budget exceeded", tokens=total_tokens)
            break

        use_tools = tools if tools and tool_calls_made < max_tools else []

        # Retry on overloaded errors
        response = _call_with_retry(
            client,
            model,
            SYSTEM_PROMPT,
            messages,
            use_tools,
        )

        total_tokens += response.usage.input_tokens + response.usage.output_tokens

        # Check if the LLM wants to use a tool
        if response.stop_reason == "tool_use" and odoo_client is not None:
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    tool_calls_made += 1
                    logger.info("Tool call", tool=block.name, call=tool_calls_made)
                    result = await execute_tool(
                        block.name,
                        block.input,
                        odoo_client,
                        odoo_uid,
                        odoo_api_key,
                    )
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        }
                    )

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})
        else:
            break

    # Extract text from final response
    raw_text = ""
    for block in response.content:
        if hasattr(block, "text") and block.text:
            raw_text += block.text

    # If the final response is just an intro ("Laissez-moi examiner...") or empty,
    # and we made tool calls, force a summary response without tools
    is_intro_only = len(raw_text) < 200 and tool_calls_made > 0
    if (not raw_text or is_intro_only) and tool_calls_made > 0:
        logger.info("Requesting final summary after tool calls", text_length=len(raw_text))
        # Add current response to messages if it has content
        if response.content:
            messages.append({"role": "assistant", "content": response.content})
        messages.append(
            {
                "role": "user",
                "content": "Maintenant donne ta reponse complete basee sur les donnees trouvees.",
            },
        )
        summary_resp = client.messages.create(
            model=model,
            max_tokens=4096,
            system=SYSTEM_PROMPT,
            messages=messages,  # type: ignore[arg-type]
        )
        total_tokens += summary_resp.usage.input_tokens + summary_resp.usage.output_tokens
        raw_text = ""
        for block in summary_resp.content:
            if hasattr(block, "text") and block.text:
                raw_text += block.text

    logger.info(
        "BA Agent responded",
        domain=profile.domain_id,
        tokens=total_tokens,
        text_length=len(raw_text),
    )

    return AgentResponse(
        answer=raw_text + DISCLAIMER,
        domain=profile.domain_id,
        sources=profile.modules_covered,
        tokens_used=total_tokens,
    )


def _call_with_retry(
    client: Any,
    model: str,
    system: str,
    messages: list[dict[str, Any]],
    tools: list[dict[str, Any]],
    max_retries: int = 2,
) -> Any:
    """Call Anthropic API with retry on overloaded errors."""
    import time

    import anthropic

    for attempt in range(max_retries + 1):
        try:
            return client.messages.create(
                model=model,
                max_tokens=4096,
                system=system,
                messages=messages,
                tools=tools if tools else anthropic.NOT_GIVEN,
            )
        except anthropic.APIStatusError as exc:
            if exc.status_code != 529:  # 529 = Overloaded
                raise
            if attempt < max_retries:
                wait = 2 * (attempt + 1)
                logger.warning("Anthropic overloaded, retrying", attempt=attempt + 1, wait=wait)
                time.sleep(wait)
            else:
                raise


def _build_profile_context(profile: BAProfile, question: str = "") -> str:
    """Build context from BA Profile — targeted to the question."""
    parts: list[str] = [
        f"Domaine : {profile.domain_name}",
        f"Modules : {', '.join(profile.modules_covered)}",
    ]
    if profile.summary:
        parts.append(f"Resume : {profile.summary[:200]}")

    # Q&A pairs — filter by relevance to the question
    if profile.qa_pairs:
        relevant_qa = profile.qa_pairs
        if question:
            q_lower = question.lower()
            scored = []
            for qa in profile.qa_pairs:
                # Simple keyword overlap scoring
                qa_words = set(qa.question.lower().split())
                q_words = set(q_lower.split())
                score = len(qa_words & q_words)
                scored.append((score, qa))
            scored.sort(key=lambda x: x[0], reverse=True)
            relevant_qa = [qa for _, qa in scored[:5]]

        parts.append("\nQuestions types et comment y repondre :")
        for qa in relevant_qa:
            models = ", ".join(qa.models_to_query) if qa.models_to_query else ""
            fields = ", ".join(qa.fields_to_fetch) if qa.fields_to_fetch else ""
            parts.append(f"  Q: {qa.question}")
            if models:
                parts.append(f"  → Modele: {models} | Champs: {fields}")
            if qa.domain_filter_example:
                parts.append(f"  → Filtre: {qa.domain_filter_example}")

    # Workflows — help LLM understand how things connect
    if profile.workflows:
        parts.append("\nWorkflows :")
        for w in profile.workflows[:3]:
            steps = " → ".join(w.steps[:5]) if w.steps else ""
            parts.append(f"  {w.name}: {steps}")

    # Feature discoveries — short
    if profile.feature_discoveries:
        parts.append("\nFonctionnalites peu connues :")
        for f in profile.feature_discoveries[:5]:
            parts.append(f"  - {f.name} ({f.how_to_activate})")

    return "\n".join(parts)
