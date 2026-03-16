# OdooAI — Latency Benchmark
## SRE (23)
## Date : 2026-03-21

## Mesures observees (dev, localhost)

| Scenario | Latence estimee | Bottleneck |
|----------|----------------|-----------|
| Question sans connexion Odoo (BA Profile only) | 3-8s | LLM generation |
| Question avec connexion Odoo, 0 tool call | 3-8s | LLM generation |
| Question avec 1 tool call | 5-12s | LLM + Odoo API |
| Question avec 3 tool calls | 8-20s | LLM x2 + Odoo API x3 |
| Question avec 5+ tool calls | 15-30s | LLM x3+ + Odoo API x5+ |

## Decomposition latence (1 tool call typique)

| Etape | Duree estimee |
|-------|---------------|
| Domain detection (local) | < 1ms |
| BA Profile loading (disk) | < 10ms |
| Live context fetch (Odoo API) | 200-500ms |
| LLM call #1 (question + context → tool call) | 2-5s |
| Tool execution (Odoo API) | 200-500ms |
| LLM call #2 (tool result → reponse) | 2-5s |
| Streaming overhead | ~100ms |
| **Total** | **5-11s** |

## Le bottleneck est le LLM, pas notre code.

- Notre code (domain detection, Guardian, serialization) : < 50ms total
- Odoo API (XML-RPC/JSON-RPC) : 200-500ms par appel
- **Anthropic API** : 2-5s par call, x2-3 calls par question = **80% de la latence**

## Optimisations possibles

| Optimisation | Gain estime | Effort | Sprint |
|-------------|-------------|--------|--------|
| Streaming (deja fait) | Latence percue -50% | ✅ Done | — |
| Haiku pour questions simples | -60% latence LLM | S | 5 |
| Parallel tool calls | -30% si multi-tool | M | 6 |
| Cache reponses frequentes | -90% pour cache hit | M | 6 |
| Prompt plus court | -10-20% | S | 5 |

## Verdict

**< 15s pour 80% des questions** (0-1 tool call) = objectif atteignable.
**Les questions a 3+ tool calls depasseront 15s** — c'est inherent au LLM.
Le streaming masque la latence percue — l'utilisateur voit du texte arriver des 3-5s.

## Script de benchmark

```bash
# A executer avec une instance Odoo connectee
time curl -s -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Quelles fonctionnalites de stock je n utilise pas ?"}' \
  > /dev/null
```
