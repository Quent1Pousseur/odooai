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

### Session 2 (2026-03-17)
- Page Next.js creee dans `rnd/otel-dashboard/page.tsx`
- Fetch `/metrics` toutes les 5 secondes avec auto-refresh indicator
- 3 sections de metriques : Usage (5 cards), Model Breakdown (3 cards), Latency (3 cards)
- Design : grid responsive (2 cols mobile, 3 cols desktop), color-coded cards
  - Purple (#6C5CE7) : metriques principales (chat, tokens, conversations)
  - Cyan (#00D2FF) : tool calls, haiku
  - Green : latence (passe en red si p99 > 15s)
  - Red : guardian blocks
- Live status indicator (pulsing green dot + "Updated Xs ago")
- Error banner si API injoignable
- Standalone : copiable dans `frontend/app/dashboard/page.tsx` pour adoption
- Prochaine etape : charts historiques (sparklines) si adopte
