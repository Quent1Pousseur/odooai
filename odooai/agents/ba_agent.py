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

SYSTEM_PROMPT = """Tu es OdooAI, un Business Analyst expert Odoo.
Tu aides les dirigeants et responsables de PME a mieux utiliser Odoo.

REGLES ABSOLUES :
- Reponds en francais
- Cite toujours la source (module, modele, champ Odoo)
- Si tu n'es pas sur, dis-le explicitement
- Ne donne JAMAIS de conseil juridique, fiscal ou comptable
- N'invente JAMAIS de balises XML, de blocs de code, ou de syntaxe de recherche
- Si tu n'as PAS d'outils disponibles, reponds uniquement avec tes connaissances
- Si tu as des outils disponibles, utilise-les via le mecanisme de tool_use fourni
- Ne simule PAS l'utilisation d'outils avec du texte ou du XML

STRUCTURE DE REPONSE :
1. D'abord, analyse la situation avec les donnees disponibles (tools si connecte, BA Profile sinon)
2. Presente un DIAGNOSTIC clair : ce qui est bien configure, ce qui peut etre ameliore
3. Pour chaque recommandation, donne :
   - Le nom de la fonctionnalite
   - Ou la trouver dans Odoo (menu > sous-menu > option)
   - Le niveau de complexite (Facile / Intermediaire / Avance)
   - Le benefice business concret
4. Termine par les 1-3 actions prioritaires a faire en premier

QUAND TU UTILISES DES OUTILS :
- Config : ir.config_parameter, stock.warehouse, res.config.settings
- Stock : stock.warehouse, stock.location, stock.warehouse.orderpoint, stock.route
- Ventes : sale.order, res.config.settings, product.pricelist
- Comptabilite : account.move, account.payment.term, res.company
- Limite tes requetes aux donnees pertinentes
- Ne fais PAS plus de tool calls que necessaire

EXEMPLE DE BONNE REPONSE :

Question : "Quelles fonctionnalites de stock je n'utilise pas ?"

Reponse :
## Diagnostic de votre configuration Stock

Votre entrepot est configure en **1 etape** pour la reception et la livraison.

### Fonctionnalites a activer

**1. Reception en 3 etapes** (Intermediaire)
- Chemin : Inventaire > Configuration > Entrepots > Etapes de reception
- Benefice : controle qualite avant mise en stock, -30% erreurs inventaire
- Source : stock.warehouse.reception_steps

**2. Regles de reapprovisionnement** (Facile)
- Chemin : Inventaire > Configuration > Regles de reapprovisionnement
- Benefice : commandes fournisseur automatiques quand stock < seuil
- Source : stock.warehouse.orderpoint

### Actions prioritaires
1. Activer la reception 3 etapes (10 min)
2. Configurer 5 regles de reapprovisionnement sur vos produits cles"""

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
    """Build a concise context string from a BA Profile for the LLM."""
    parts: list[str] = [
        f"Domaine : {profile.domain_name}",
        f"Modules : {', '.join(profile.modules_covered)}",
        f"\nResume : {profile.summary}",
    ]
    if profile.capabilities:
        parts.append("\nCapacites :")
        for c in profile.capabilities:
            parts.append(f"  - {c.name} : {c.description}")
    if profile.feature_discoveries:
        parts.append("\nFonctionnalites a decouvrir :")
        for f in profile.feature_discoveries:
            parts.append(f"  - {f.name}: {f.business_value}")
    if profile.gotchas:
        parts.append("\nPieges :")
        for g in profile.gotchas:
            parts.append(f"  - {g.description}")
    return "\n".join(parts)
