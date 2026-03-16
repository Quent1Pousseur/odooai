# ODAI-UI-004 — Landing Page "Coming Soon"

## Status
IN PROGRESS

## Auteur
Brand Designer (42) + Growth (18)

## Reviewers
CEO (01), CPO (03), Content Strategist (37)

## Date
2026-03-19

## Contexte
Pas de presence web. Sales a besoin d'un lien a envoyer aux PME. Meme basique, une landing page "coming soon" commence a construire une audience.

## Objectif
Page statique dans le meme projet Next.js :
- Pitch : "Votre Odoo peut faire plus."
- Stats : 1218 modules analyses, 5514 modeles, 9 domaines
- 3 features cles
- Plans tarifaires (Starter €49, Pro €149, Enterprise €399)
- Formulaire email capture (early access)
- DA respectee (palette, typo)

## Definition of Done
- [ ] Page /landing ou page d'accueil separee
- [ ] Pitch + stats + features + pricing
- [ ] Formulaire email (stockage basique — fichier JSON ou DB)
- [ ] DA respectee
- [ ] Mobile-friendly
- [ ] Review dans reviews/

## Fichiers impactes
| Fichier | Action |
|---------|--------|
| `frontend/app/landing/page.tsx` | Creer |
| `frontend/components/pricing-card.tsx` | Creer |
| `odooai/api/routers/waitlist.py` | Creer — endpoint email capture |

## Estimation
S-M (1 session)
