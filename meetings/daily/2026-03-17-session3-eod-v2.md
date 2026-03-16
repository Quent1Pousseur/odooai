# Daily Standup — 2026-03-17 (Session 3 — End of Day v2)

## Status Sprint : 🟢 Sprint 2 — MVP complet, pipeline end-to-end valide

## Checklist session
- [x] Daily avant
- [x] Spec ecrite avant code (ODAI-CORE-004)
- [x] Review dans reviews/
- [x] make check (178 tests)
- [x] Push + CI
- [x] Fondateur a teste sur son Odoo
- [x] Daily fin ← maintenant

**Zero violation processus.**

---

## Evenement majeur
**Le fondateur s'est connecte a son Odoo 17 en live via `odooai chat --url --db`.**

Pipeline end-to-end valide :
- Auto-detection version → XML-RPC pour Odoo 17 ✅
- Auth interactive (getpass) ✅
- Detection modules installes ✅
- Questions avec donnees live + BA Profiles ✅
- Guardian actif sur les donnees ✅

**Feedback fondateur** : "il me repond mais pas encore correctement — cherche des donnees un peu a cote de la plaque". C'est attendu pour un MVP : le contexte live est predetermine (10 dernieres commandes) au lieu d'etre adapte a la question.

---

## BLOC 1 — Challenges

### AI Engineer (09)
- "Le probleme identifie est clair : `_live_context.py` fait des requetes fixes au lieu de comprendre la question et generer la requete Odoo adaptee. La solution : le LLM genere le domain filter en fonction de la question. C'est un tool-use pattern classique."
- **Proposition Sprint 3** : "Le BA Agent recoit des 'tools' (search_read, search_count) et le LLM decide quoi requeter. Le Guardian valide chaque requete avant execution."

### Prompt Engineer (25)
- "En attendant le tool-use, on peut ameliorer le prompt pour que le LLM explique mieux ce qu'il a vu dans le contexte live et ce qu'il ne peut pas encore faire."

### Odoo Expert (10)
- "Les requetes fixes (10 dernieres commandes) ne sont pas inutiles — elles donnent un apercu. Mais pour repondre a 'combien de factures impayees', il faudrait un domain `[('state','=','posted'),('payment_state','=','not_paid')]`. C'est le LLM qui doit generer ca."

### CPO (03)
- "Pour le MVP c'est OK. Le fondateur a dit que ca fonctionne. Les reponses ne sont pas parfaites mais le pipeline prouve la valeur. On peut montrer ca aux PME."

### Security Architect (07)
- "Si le LLM genere des domain filters en Sprint 3, le `domain_validator` devient encore plus critique. Chaque domain genere par le LLM doit passer par la validation anti-injection."

---

## Bilan Sprint 2 a date

| Piste | Status |
|-------|--------|
| A. Guardian wire | ✅ DONE |
| A. Connexion live | ✅ DONE — teste par fondateur |
| B. Frontend Next.js | Pas commence |
| C. BA Profile validation | Pas commence |
| D. Business (PME + avocat) | Action fondateur |
| E. Qualite | Reviews documentees ✅ |

## Metriques

| Metrique | Valeur |
|----------|--------|
| Commits | 40 |
| Specs | 11 |
| Tests | 178 |
| Reviews documentees | 3 |
| Violations processus Sprint 2 | **0** |
| Pipeline end-to-end | ✅ Valide par fondateur |

## Prochaines actions

| Action | Qui | Quand |
|--------|-----|-------|
| Spec ODAI-UI-001 (frontend Next.js) | Frontend Eng (21) | Prochaine session |
| BA Profile validation (sales_crm) | Odoo Expert (10) | Prochaine session |
| 5 contacts PME | Fondateur | Cette semaine |
| RDV avocat LGPL | Fondateur | Cette semaine |
| Ameliorer live context (tool-use) | AI Eng (09) | Sprint 3 |

## Amelioration a planifier (Sprint 3)
Le LLM doit pouvoir generer ses propres requetes Odoo au lieu de recevoir un contexte predetermine. Pattern : tool-use avec Guardian validation sur chaque requete generee.

---

> **Prochain meeting** : Daily debut prochaine session
