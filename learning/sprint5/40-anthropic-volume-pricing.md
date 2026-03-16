# Learning — Vendor Manager (40) — Anthropic Volume Pricing
## Date : 2026-03-21 (Sprint 5)
## Duree : 3 heures

## Ce que j'ai appris
- Anthropic propose des volume discounts a partir de $10K/mois
- Le programme "Anthropic for Startups" offre des credits API pour les early-stage
- Les Batches API reduisent les couts de 50% pour les traitements non-temps-reel (BA Profile generation)
- Claude Haiku 4.5 est 6x moins cher que Sonnet — le routing est la meilleure optimisation

## Comment ca s'applique a OdooAI
- BA Profile generation devrait utiliser les Batches API (pas de contrainte temps reel)
- Postuler au programme startups pour des credits gratuits
- A 100 clients Pro (149€), on depense ~650€/mois en tokens — loin du seuil $10K

## Ce que je recommande
1. Sprint 5 : postuler au programme Anthropic for Startups (credits gratuits)
2. Sprint 6 : utiliser Batches API pour regenerer les BA Profiles
3. Plus tard : negocier volume discount quand on depasse $5K/mois

## Sources
- Anthropic pricing page + enterprise contact
- Anthropic Batches API documentation
