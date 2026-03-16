# Learning — Vendor Manager (40) — OpenAI Fallback (approfondissement)
## Date : 2026-03-21
## Duree : 3 heures (jour 2)

## Ce que j'ai appris (approfondissement)

### Implementation concrete du fallback
Le port `ILLMProvider` existe deja. Il suffit de :

1. Creer `OpenAIProvider` qui implemente le meme interface
2. Ajouter un `FALLBACK_LLM_PROVIDER` dans config
3. Try Anthropic → catch → try OpenAI → catch → erreur

### Mapping des modeles
| Anthropic | OpenAI equivalent | Qualite |
|-----------|------------------|---------|
| Sonnet 4 | GPT-4o | ~95% |
| Haiku 4.5 | GPT-4o-mini | ~90% |

### Differences de format
- Anthropic : `system` est un parametre separe
- OpenAI : `system` est un message avec role "system"
- Anthropic : `tool_use` block type
- OpenAI : `function_call` / `tool_calls`

Le mapping est simple mais il faut adapter la serialisation des tool calls.

### Estimation effort
- `OpenAIProvider` : 1 jour (format messages + tool mapping)
- Tests : 0.5 jour
- Config : 2h
- **Total : 2 jours**

## Ce que je recommande
Sprint 6 : implementer `OpenAIProvider`. Pas Sprint 5 (trop de choses).

## Sources
- OpenAI API documentation
- Anthropic → OpenAI migration guide
