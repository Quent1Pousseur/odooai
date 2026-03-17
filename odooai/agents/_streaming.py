"""
Module: agents/_streaming.py
Role: Streaming version of BA Agent — yields text chunks as they arrive.
      Used by the chat API endpoint for real-time display.
Dependencies: anthropic, _tools
"""

from __future__ import annotations

from collections.abc import AsyncGenerator
from typing import Any

import structlog

from odooai.agents._tools import TOOL_DEFINITIONS, execute_tool
from odooai.agents.ba_agent import DISCLAIMER, SYSTEM_PROMPT, _build_profile_context
from odooai.knowledge.schemas.ba_profile import BAProfile

logger = structlog.get_logger(__name__)

_TOOL_LABELS: dict[str, str] = {
    "odoo_search_read": "Analyse de vos donnees",
    "odoo_search_count": "Comptage des enregistrements",
    "odoo_read_group": "Calcul des statistiques",
}


def _tool_message(tool_name: str) -> str:
    """Human-readable message for a tool call."""
    return _TOOL_LABELS.get(tool_name, "Recherche en cours")


async def stream_ba_response(
    question: str,
    profile: BAProfile,
    anthropic_api_key: str,
    model: str = "claude-sonnet-4-20250514",
    odoo_client: Any | None = None,
    odoo_uid: int = 0,
    odoo_api_key: str = "",
    max_tools: int = 10,
    conversation_history: list[dict[str, str]] | None = None,
) -> AsyncGenerator[dict[str, Any], None]:
    """
    Stream BA Agent response as events.

    Yields dicts with type: "text", "tool_start", "tool_end", "done", "error".
    """
    import anthropic

    client = anthropic.Anthropic(api_key=anthropic_api_key)
    tools = TOOL_DEFINITIONS if odoo_client is not None else []

    # Only inject BA context when NOT connected (no tools)
    if tools:
        user_message = question
    else:
        context = _build_profile_context(profile, question=question)
        user_message = f"""Contexte Odoo :
{context}

{question}"""

    # Build messages with conversation history
    messages: list[dict[str, Any]] = []
    if conversation_history:
        history = conversation_history
        # If history is long, summarize the old part and keep recent messages
        if len(history) > 6:
            old_msgs = history[:-4]
            recent_msgs = history[-4:]
            # Create a summary of old messages
            summary_parts = []
            for msg in old_msgs:
                role = "User" if msg["role"] == "user" else "Buddy"
                text = msg["content"][:100]
                summary_parts.append(f"{role}: {text}")
            summary = "\n".join(summary_parts)
            messages.append(
                {
                    "role": "user",
                    "content": f"[Resume de la conversation precedente :\n{summary}\n]",
                }
            )
            messages.append(
                {
                    "role": "assistant",
                    "content": "Compris, je continue la conversation.",
                }
            )
            history = recent_msgs

        # Inject recent history — truncate long messages
        for msg in history:
            content = msg["content"]
            if len(content) > 500:
                content = content[:500] + "..."
            messages.append({"role": msg["role"], "content": content})
    messages.append({"role": "user", "content": user_message})
    total_tokens = 0
    tool_calls_made = 0
    max_budget = 50000

    for _round in range(max_tools + 1):
        if total_tokens > max_budget:
            break

        use_tools = tools if tools and tool_calls_made < max_tools else []

        try:
            with client.messages.stream(
                model=model,
                max_tokens=4096,
                system=SYSTEM_PROMPT,
                messages=messages,  # type: ignore[arg-type]
                tools=use_tools if use_tools else anthropic.NOT_GIVEN,  # type: ignore[arg-type]
            ) as stream:
                collected_content: list[Any] = []
                current_tool_input = ""
                current_tool_name = ""

                for event in stream:
                    if event.type == "content_block_start":
                        block = event.content_block
                        if hasattr(block, "text"):
                            pass  # Text block starting
                        elif hasattr(block, "name"):
                            # Tool use starting
                            current_tool_name = block.name
                            current_tool_input = ""
                            yield {
                                "type": "tool_start",
                                "tool": current_tool_name,
                                "message": _tool_message(current_tool_name),
                            }

                    elif event.type == "content_block_delta":
                        delta = event.delta
                        if hasattr(delta, "text"):
                            yield {"type": "text", "content": delta.text}
                        elif hasattr(delta, "partial_json"):
                            current_tool_input += delta.partial_json

                    elif event.type == "content_block_stop":
                        pass

                # Get final message for metadata
                response = stream.get_final_message()
                total_tokens += response.usage.input_tokens + response.usage.output_tokens
                collected_content = list(response.content)

        except anthropic.APIStatusError as exc:
            if exc.status_code == 529:
                yield {"type": "status", "content": "Serveur surcharge, nouvelle tentative..."}
                import asyncio

                await asyncio.sleep(2)
                continue
            yield {"type": "error", "content": f"Erreur API ({exc.status_code})"}
            return
        except Exception as exc:
            yield {"type": "error", "content": f"Erreur ({type(exc).__name__})"}
            return

        # Check if we need to process tool calls
        if response.stop_reason == "tool_use" and odoo_client is not None:
            tool_results = []
            for block in collected_content:
                if block.type == "tool_use":
                    tool_calls_made += 1
                    inp = block.input if isinstance(block.input, dict) else {}
                    odoo_model = inp.get("model", "")
                    yield {
                        "type": "tool_start",
                        "tool": block.name,
                        "message": _tool_message(block.name),
                        "model": odoo_model,
                    }
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
                    yield {"type": "tool_end", "tool": block.name}

            messages.append({"role": "assistant", "content": collected_content})
            messages.append({"role": "user", "content": tool_results})
        else:
            break

    # Disclaimer
    yield {"type": "text", "content": DISCLAIMER}

    # Done event with metadata
    yield {
        "type": "done",
        "tokens": total_tokens,
        "sources": profile.modules_covered,
        "domain": profile.domain_id,
    }
