# ODAI-UI-003 — Formulaire Connexion Odoo dans le Web

## Status
IN PROGRESS

## Auteur
Frontend Engineer (21) + Backend Architect (08)

## Reviewers
Security Architect (07), CPO (03)

## Date
2026-03-19

## Contexte
La connexion live Odoo ne fonctionne qu'en CLI (--url --db). Pour les demos PME, il faut un formulaire dans l'interface web.

## Objectif
Formulaire dans le header ou un modal :
- URL instance Odoo
- Nom de la base de donnees
- Login
- API Key (champ password)
- Bouton "Connecter" → auth → indicateur connecte/deconnecte

## Definition of Done
- [ ] Formulaire dans un modal ou panel
- [ ] Champs : URL, DB, login, API key
- [ ] API key en champ password (pas visible)
- [ ] Indicateur connecte/deconnecte dans le header
- [ ] Credentials envoyes dans POST /api/chat (deja supporte)
- [ ] Deconnexion (clear state)
- [ ] Review dans reviews/

## Fichiers impactes
| Fichier | Action |
|---------|--------|
| `frontend/components/odoo-connect.tsx` | Creer |
| `frontend/app/page.tsx` | Modifier — integrer le formulaire |

## Securite
- API key jamais stockee en localStorage (memoire React seulement)
- HTTPS obligatoire en production
- Credentials transmis dans le body POST (pas dans l'URL)

## Estimation
S (< 1 jour)
