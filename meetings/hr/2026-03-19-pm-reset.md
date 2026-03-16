# Meeting d'Urgence — Reset PM (04)
## Date : 2026-03-19
## Participants : Fondateur (00), CEO (01), CTO (02), HR Director (44), PM (04)
## Declencheur : Alerte RH — surcharge cognitive critique (9/10)

---

## Contexte (HR Director)

"Suite au team building d'hier soir, le PM m'a confie etre completement deborde. 65 commits, 18 specs, 5 sprints en 4 jours. Il ne suit plus le roadmap, les priorites changent trop vite, et il track tout dans sa tete. Ce n'est pas tenable."

## PM (04) — ce qu'il ressent

"Merci de ce meeting. Voila ou j'en suis honnêtement :
- Le roadmap dit Phase 1 mois 1-3 mais on est deja en Phase 3. Je ne sais plus ou on en est.
- Les priorites changent a chaque session. On commence une spec, puis on pivote sur une autre.
- Je n'ai pas d'outil visuel. Tout est dans des fichiers markdown que je dois parcourir.
- Je ne sais pas qui fait quoi. Les assignations sont implicites.
- Je perds du temps a retrouver ce qui a ete fait vs ce qui reste.

Ce dont j'ai besoin :
1. Un point zero — ou on en est EXACTEMENT
2. Un roadmap stable pour 2 semaines minimum
3. Un outil de suivi visuel
4. Des priorites qui ne changent pas toutes les heures"

## CTO (02) — diagnostic technique

"Le PM a raison. On a avance extremement vite mais sans structure de suivi. Voici l'etat reel :

### Ce qui est FAIT (livré, testé, fonctionnel)
| Spec | Livrable | Tests | Status |
|------|----------|-------|--------|
| ODAI-CORE-001 | Architecture hexagonale | 51 | ✅ Done |
| ODAI-CORE-002 | OdooClient dual-protocol | 20 | ✅ Done |
| ODAI-CORE-003 | Config + structlog | 12 | ✅ Done |
| ODAI-INFRA-001 | CI/CD 6 jobs | — | ✅ Done |
| ODAI-SEC-001 | Security Guardian | 24 | ✅ Done |
| ODAI-DATA-001 | Knowledge Graphs + Code Analyst | 28 | ✅ Done |
| ODAI-DATA-002 | BA Factory (9 BA Profiles) | 8 | ✅ Done |
| ODAI-AGENT-001 | Orchestrator + tool-use | 8 | ✅ Done |
| ODAI-AGENT-002 | Chat CLI (odooai chat) | 6 | ✅ Done |
| ODAI-AGENT-003 | Streaming + live context | 4 | ✅ Done |
| ODAI-AGENT-004 | Red teaming + fixes | 3 | ✅ Done |
| ODAI-CORE-004 | Connexion live Odoo | 2 | ✅ Done |
| ODAI-CORE-005 | Conversations persistantes | 4 | ✅ Done |
| ODAI-UI-001 | Frontend chat (Next.js) | — | ✅ Done |
| ODAI-UI-002 | Sidebar conversations | — | ✅ Done |
| ODAI-UI-003 | Formulaire connexion Odoo | — | ✅ Done |
| ODAI-UI-004 | Landing page | — | ✅ Done |
| ODAI-API-001 | CLI (analyze, chat, serve) | 8 | ✅ Done |

**Total : 18 specs livrees, 178 tests, 65 commits.**

### Ce qui est EN COURS / PREVU
- Phase technique : context window management, auth, multi-tenant
- Phase qualite : tests integration, eval framework, audit securite complet
- Phase business : 5 contacts PME, demo ciblee, avocat LGPL
- Phase infra : Docker, staging, PostgreSQL, monitoring"

## CEO (01) — realignment

"On a fait en 4 jours ce qui etait prevu en 3 mois. C'est exceptionnel mais ca a un cout humain. Je prends la responsabilite d'avoir pousse trop vite. Voici ce que je propose :

1. **On freeze les features pour 1 semaine.** Pas de nouvelle spec jusqu'au 26 mars.
2. **Sprint 4 = stabilisation + qualite + business.** Pas de nouveau code, on consolide.
3. **Le PM gere via GitHub Projects** — on migre le tracking depuis les fichiers markdown.
4. **Les priorites sont fixees pour 7 jours.** Pas de changement sauf VETO securite."

## CTO (02) — accord

"D'accord avec le feature freeze. Ca nous laisse le temps de :
- Faire l'audit securite complet (Security Arch + Auditor)
- Mettre en place les tests d'integration (QA Lead)
- Preparer la demo ciblee (Sales + CPO)
- Docker + staging (DevOps + Infra)

C'est ce que l'equipe Infra+Security demandait au team building."

## HR Director (44) — recommandation

"Bien. Voici comment on protege le PM :

1. **PM = coordinateur, pas executeur.** Il ne code pas, il ne redige pas de specs. Il suit et rapporte.
2. **Daily = 10 minutes max.** Le PM lit les updates, pas les produire.
3. **Un seul canal de changement de priorite** — le CEO, via le PM. Personne d'autre ne change les priorites.
4. **Point hebdomadaire** — chaque vendredi, 30min, CEO + CTO + PM. Pas plus."

## PM (04) — reponse

"Merci. Le feature freeze et GitHub Projects, c'est exactement ce qu'il me faut. Et le fait que les priorites viennent d'un seul canal, ca change tout. Je reprends le controle."

---

## DECISIONS

| # | Decision | Responsable | Deadline |
|---|----------|-------------|----------|
| 1 | Feature freeze jusqu'au 26 mars | CEO | Immediate |
| 2 | Sprint 4 = stabilisation + qualite + business | CTO + CEO | 20-26 mars |
| 3 | Migration tracking vers GitHub Projects | PM | 21 mars |
| 4 | Priorites fixees pour 7 jours, un seul canal (CEO) | CEO | Immediate |
| 5 | PM = coordinateur uniquement | HR Director | Immediate |
| 6 | Point hebdomadaire vendredi 30min | PM + CEO + CTO | Chaque vendredi |

---

## Score PM post-meeting
- Charge estimee : 9/10 → **6/10** (apres feature freeze + outils)
- Motivation estimee : 5/10 → **7/10** (se sent entendu et soutenu)

> **Prochain check-in PM** : vendredi 21 mars 2026
