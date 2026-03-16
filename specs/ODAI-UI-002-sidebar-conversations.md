# ODAI-UI-002 — Sidebar Conversations

## Status
IN PROGRESS

## Auteur
Frontend Engineer (21) + Chat Engineer (43)

## Reviewers
CPO (03), CTO (02)

## Date
2026-03-18

## Contexte
Les conversations sont persistees en DB (CORE-005) mais l'utilisateur ne peut pas les retrouver. Il faut une sidebar avec la liste des conversations et la possibilite de reprendre ou creer une nouvelle.

## Objectif
1. Sidebar gauche avec liste des conversations
2. "Nouvelle conversation" en haut
3. Clic sur une conversation → charge l'historique
4. Conversation courante surlignee
5. Responsive (sidebar cachee sur mobile)

## Definition of Done
- [ ] Sidebar avec liste des conversations (GET /api/conversations)
- [ ] Bouton "Nouvelle conversation"
- [ ] Clic → charge l'historique (GET /api/conversations/{id}/messages)
- [ ] conversation_id envoye dans POST /api/chat
- [ ] Conversation courante surlignee
- [ ] Responsive (collapse sur mobile)
- [ ] Review dans reviews/
- [ ] Fondateur teste

## Fichiers impactes
| Fichier | Action |
|---------|--------|
| `frontend/app/page.tsx` | Modifier — ajouter sidebar + state |
| `frontend/components/sidebar.tsx` | Creer |

## Estimation
S (< 1 jour)
