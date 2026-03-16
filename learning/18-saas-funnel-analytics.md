# Learning — Growth Engineer (18) — SaaS Funnel Analytics
## Date : 2026-03-21
## Duree : 3 heures

## Ce que j'ai appris

### Funnel type SaaS IA
```
Landing page visit → Email signup → Beta access → First question → Aha moment → Subscription
```

### Metriques a tracker (AARRR)
| Etape | Metrique | Outil |
|-------|---------|-------|
| Acquisition | Visites landing, source | Plausible (privacy-first) |
| Activation | 1ere question posee | Event backend |
| Retention | Questions/semaine | DB analytics |
| Revenue | Conversion free→paid | Stripe |
| Referral | Partages, invitations | Custom tracking |

### Plausible vs Google Analytics
- Plausible : privacy-first, pas de cookies, GDPR compliant, 9€/mois
- Google Analytics : gratuit mais cookies, banniere RGPD obligatoire, donnees Google
- **Recommandation : Plausible** — coherent avec notre positionnement securite

### Le "Aha Moment" d'OdooAI
Le moment ou l'utilisateur se dit "wow, ca m'est utile" :
- Hypothese : quand l'IA revele une fonctionnalite que l'utilisateur ne connaissait pas
- A valider avec les premiers beta users
- Tout le funnel doit optimiser vers ce moment

## Comment ca s'applique a OdooAI
- Zero analytics actuellement — on est aveugle
- Plausible sur la landing = 30min de setup
- Event tracking sur le backend (1ere question, domain detecte) = facile avec structlog

## Ce que je recommande
1. Sprint 5 : Plausible sur la landing page (30min)
2. Sprint 5 : Event tracking backend (1ere question, conversion)
3. Sprint 6 : Dashboard analytics simple

## Sources
- Plausible.io documentation
- "Lean Analytics" — Alistair Croll
