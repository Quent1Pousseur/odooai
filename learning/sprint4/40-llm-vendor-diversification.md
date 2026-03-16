# Learning — Vendor Manager (40) — LLM Vendor Diversification
## Date : 2026-03-20
## Duree : 3 heures

## Ce que j'ai appris

### Risque de single vendor LLM
- OdooAI depend a 100% d'Anthropic (Claude)
- Si Anthropic augmente ses prix de 50%, nos marges s'effondrent
- Si l'API tombe (OverloadedError deja vu), le produit est inutilisable
- Si Anthropic change ses policies (refus de certains contenus), nos BA Profiles pourraient etre impactes

### Alternatives evaluees

| Provider | Modele | Qualite (vs Sonnet) | Prix input/1M | Prix output/1M |
|----------|--------|---------------------|---------------|----------------|
| Anthropic | Sonnet 4 | Reference | $3 | $15 |
| Anthropic | Haiku 4.5 | 70% | $0.80 | $4 |
| OpenAI | GPT-4o | ~95% | $2.50 | $10 |
| OpenAI | GPT-4o-mini | ~75% | $0.15 | $0.60 |
| Mistral | Large | ~85% | $2 | $6 |
| Mistral | Medium | ~70% | $0.40 | $1.20 |
| Google | Gemini 2.0 Pro | ~90% | $1.25 | $5 |
| Local | Llama 3.1 70B | ~65% | GPU cost | GPU cost |

### Strategie recommandee : tiered fallback
1. **Primary** : Claude Sonnet (qualite max)
2. **Fallback 1** : GPT-4o (si Anthropic down)
3. **Fallback 2** : Mistral Large (si OpenAI aussi down)
4. **Budget mode** : Haiku ou GPT-4o-mini (pour les requetes simples)

### Implementation cote architecture
- Le port `ILLMProvider` existe deja (architecture hexagonale)
- Il suffit d'implementer `OpenAIProvider` et `MistralProvider`
- Le router choisit le provider selon : disponibilite → qualite → cout

## Comment ca s'applique a OdooAI
- L'architecture est deja LLM-agnostic (port `ILLMProvider`) — bon point
- Mais on n'a qu'une implementation (`AnthropicProvider`)
- Le plan B coute 2-3 jours de dev max grace aux ports
- Le budget mode pourrait reduire les couts de 80% sur les requetes simples

## Ce que je recommande
1. Sprint 5 : implementer `OpenAIProvider` comme fallback
2. Sprint 6 : routing intelligent (Sonnet pour complexe, Haiku pour simple)
3. Negocier avec Anthropic un volume discount si > 10K$/mois
4. Monitorer les couts par requete (metrique Observability)

## Sources
- Anthropic pricing page
- OpenAI pricing page
- Mistral AI pricing page
- "Multi-LLM Strategy" — a]16z blog
