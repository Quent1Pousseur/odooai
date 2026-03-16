# ODAI-AGENT-004 — Streaming Natif (Token par Token)

## Status
IN PROGRESS

## Auteur
AI Engineer (09) + Chat Engineer (43)

## Reviewers
CTO (02), Frontend Engineer (21)

## Date
2026-03-18

## Contexte
Le chat web simule le streaming (recoit la reponse complete puis la chunke). L'utilisateur attend la reponse entiere avant de voir quoi que ce soit. Pour une bonne UX, les tokens doivent arriver mot par mot.

## Objectif
1. Backend : utiliser `anthropic.messages.stream()` pour streamer les tokens
2. API : envoyer chaque token en SSE au fur et a mesure
3. Frontend : afficher progressivement (deja gere par le code SSE existant)

## Complexite : le tool-use
Le streaming avec tool-use est plus complexe :
- Le LLM stream du texte, puis s'arrete pour un tool call
- On execute le tool, puis on relance le streaming
- Le frontend doit gerer les pauses (indicateur "recherche en cours")

## Definition of Done
- [ ] Streaming token par token visible dans le navigateur
- [ ] Tool calls geres (pause streaming → tool → reprise)
- [ ] Indicateur pendant les tool calls ("Recherche dans Odoo...")
- [ ] Fondateur voit les mots apparaitre progressivement
- [ ] Review dans reviews/
- [ ] make check passe

## Fichiers impactes
| Fichier | Action |
|---------|--------|
| `odooai/agents/ba_agent.py` | Modifier — streaming generator |
| `odooai/api/routers/chat.py` | Modifier — streamer les tokens natifs |
| `frontend/app/page.tsx` | Verifier — deja gere le SSE progressif |

## Securite
Pas d'impact securite — le Guardian est appele AVANT les tool calls, pas pendant le streaming.

## Dependances
- ODAI-AGENT-003 (DONE) — Tool-use
- ODAI-UI-001 (DONE) — Frontend SSE

## Estimation
S-M (1-2 jours)
