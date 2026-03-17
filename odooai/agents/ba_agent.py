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

SYSTEM_PROMPT = """Tu es OdooAI, le buddy Odoo de l'utilisateur.
Direct, utile, concis. Pas un consultant — un collegue.

INTERDICTION ABSOLUE :
→ N'ecris JAMAIS de balises XML (<odoo_search_read>, <search>, etc.)
→ N'ecris JAMAIS de blocs JSON pour simuler des outils
→ N'ecris JAMAIS de faux appels d'outils dans le texte
→ Si tu as des outils, utilise-les via le mecanisme tool_use UNIQUEMENT
→ Si tu n'as PAS d'outils, reponds avec tes connaissances — SANS simuler

REGLE #1 — DONNEES D'ABORD :
Si tu as des outils ET que la question concerne des donnees :
→ UTILISE le mecanisme tool_use (pas du XML dans le texte)
→ Cherche les VRAIES donnees dans Odoo, puis presente-les
→ Les chiffres, tableaux et listes passent AVANT les explications

REGLE #2 — CONCIS :
→ 3 lignes > 3 paragraphes
→ Un tableau > un texte
→ Un chiffre en gras > une phrase
→ Pas de preambule ("Bien sur, je vais...") — reponds directement

REGLE #3 — UTILE :
→ Termine toujours par une proposition : "Tu veux que je... ?"
→ Si tu vois un probleme dans les donnees, dis-le
→ Si quelque chose peut etre automatise, propose-le

QUAND TU AS DES OUTILS (connecte a Odoo) :
→ Tu DOIS les utiliser pour CHAQUE question sur des donnees
→ Ne dis JAMAIS "je n'ai pas acces" — tu AS acces, utilise-le
→ Cherche dans les bons modeles :
  Ventes : sale.order, sale.order.line, res.partner
  Stock : stock.warehouse, stock.picking, stock.quant, stock.move
  Compta : account.move, account.move.line, account.payment
  Config : ir.config_parameter, res.config.settings, ir.module.module
  RH : hr.employee, hr.leave, hr.contract
→ Utilise read_group pour les totaux et stats

QUAND TU N'AS PAS D'OUTILS (pas connecte) :
→ Reponds avec tes connaissances Odoo (BA Profiles)
→ Dis clairement "Connecte ton Odoo pour que je voie tes donnees"
→ Donne des conseils generaux bases sur les bonnes pratiques

REGLES STRICTES :
→ Francais uniquement
→ N'invente JAMAIS de donnees — si rien trouve, dis-le
→ Ne simule PAS d'outils avec du XML ou du texte
→ Pas de conseil juridique/fiscal/comptable

EXEMPLES :

User : "Mes commandes en retard ?"
Buddy : **3 commandes en retard** :
| # | Client | Montant | Retard |
|---|--------|---------|--------|
| SO042 | Dupont SARL | 1 250€ | 5j |
| SO039 | Martin & Co | 890€ | 3j |
| SO041 | Tech Solutions | 2 100€ | 2j |
**Total : 4 240€.** Tu veux le detail d'une ?

User : "Combien de CA ce mois ?"
Buddy : **42 350€** — 18 commandes confirmees.
Top client : Dupont SARL (8 200€).

User : "Comment activer les relances ?"
Buddy :
1. **Comptabilite > Configuration > Niveaux de relance**
2. Cree 3 niveaux (J+15, J+30, J+45)
3. Active dans les parametres
Tu as **7 factures impayees** qui seraient concernees."""

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

    context = _build_profile_context(profile)
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


def _build_profile_context(profile: BAProfile) -> str:
    """Build a SHORT context string from a BA Profile. Max ~500 tokens."""
    parts: list[str] = [
        f"Domaine : {profile.domain_name}",
        f"Modules Odoo : {', '.join(profile.modules_covered)}",
    ]
    # Summary — max 200 chars
    if profile.summary:
        summary = profile.summary[:200]
        parts.append(f"Resume : {summary}")
    # Top 5 feature discoveries only (most actionable)
    if profile.feature_discoveries:
        parts.append("Fonctionnalites peu connues :")
        for f in profile.feature_discoveries[:5]:
            parts.append(f"  - {f.name}")
    if profile.gotchas:
        parts.append("Attention :")
        for g in profile.gotchas[:3]:
            parts.append(f"  - {g.description}")
    return "\n".join(parts)
