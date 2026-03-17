# R&D — Observability Engineer (38) — OpenTelemetry Dashboard
## Date debut : 2026-03-22
## Status : En cours
## Lead : Observability Engineer (38)
## Equipe : + Frontend Eng (21) si disponible

## Objectif
Page /dashboard dans le frontend qui affiche les metriques OdooAI en temps reel. Utilise le endpoint /metrics existant.

## Plan
1. Creer une page Next.js /dashboard
2. Fetch /metrics toutes les 5s
3. Afficher les 5 metriques : chat requests, tokens, latence p50/p95, tool calls, conversations
4. Charts basiques avec des barres/compteurs

## MVP
Page /dashboard avec 5 compteurs qui se rafraichissent en temps reel.

## Avancement
### Session 1 (2026-03-22)
- Projet cree et documente
- Prochaine etape : page Next.js avec fetch /metrics
