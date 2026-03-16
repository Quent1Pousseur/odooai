# Review — ODAI-AGENT-004 (Streaming Natif)

## Reviewer : CTO (02) + Chat Engineer (43)
## Date : 2026-03-18
## Status : APPROVED

---

## Verdict
**Go.** Streaming natif via `anthropic.messages.stream()`. Token par token.

## Points verifies

### Backend streaming
- `_streaming.py` : utilise `client.messages.stream()` (natif Anthropic) ✅
- Tokens arrivent un par un via SSE ✅
- Tool calls geres : pause → execute → reprise streaming ✅
- Budget tokens (50000 max) respecte ✅
- Retry sur 529 (overloaded) ✅

### Frontend
- Events `tool_start` affiches ("Recherche dans Odoo...") ✅
- Texte progressif inchange (SSE parsing deja en place) ✅

### API
- Endpoint utilise `stream_ba_response()` au lieu de `handle_question()` ✅
- Detect domain + load BA Profile avant streaming ✅

## Notes
- Le CLI (`odooai chat`) continue d'utiliser la version non-streaming (ba_agent.py) — correct
- Le web utilise la version streaming (_streaming.py) — correct
- Separation propre entre les deux chemins
