# Review — ODAI-UI-003 + ODAI-UI-004

## Reviewer : Security Architect (07) + CPO (03)
## Date : 2026-03-19
## Status : APPROVED

---

## UI-003 : Formulaire connexion Odoo
- Modal propre avec champs URL, DB, login, API key ✅
- API key en champ password ✅
- Credentials en memoire React seulement (pas localStorage) ✅
- Indicateur connecte/deconnecte dans le header ✅
- Credentials envoyes dans le body POST (pas URL) ✅

## UI-004 : Landing page
- Pitch, stats, features, pricing, email capture ✅
- DA respectee (palette primary, accent) ✅
- Mobile-friendly ✅
- Email stocke dans waitlist.json (gitignore) ✅
- Deduplication des emails ✅
- Disclaimer "non affilie a Odoo SA" ✅

## Notes
- waitlist.json est un stockage temporaire — migrer vers DB en prod
- CORS autorise localhost:3000 — a restreindre en prod
