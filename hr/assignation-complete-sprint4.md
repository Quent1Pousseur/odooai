# Assignation Complete Sprint 4 — Tous les agents actifs
## HR Director (44) + PM (04)
## Date : 2026-03-19

---

## Principe : PERSONNE ne reste inactif. Chaque agent a au moins 1 livrable cette semaine.

---

## Agents precedemment sous-utilises — NOUVELLES TACHES

### Chaos Engineer (31) — Charge 2/10 → 6/10
| # | Tache | Deadline | Collabore avec |
|---|-------|----------|---------------|
| 1 | Plan de backup & disaster recovery | 24 mars | DevOps (22), Infra (12) |
| 2 | Test de resilience : que se passe-t-il si Anthropic tombe ? | 25 mars | AI Eng (09) |
| 3 | Test de resilience : que se passe-t-il si la DB est corrompue ? | 25 mars | DBA (30) |
| 4 | Documenter les single points of failure | 23 mars | SRE (23) |

### AI Safety & Ethics (33) — Charge 2/10 → 5/10
| # | Tache | Deadline | Collabore avec |
|---|-------|----------|---------------|
| 1 | Document de conformite EU AI Act (draft) | 25 mars | Legal (16) |
| 2 | Audit des disclaimers et transparence dans le chat | 23 mars | Prompt Eng (25) |
| 3 | Checklist "AI Act limited risk" pour OdooAI | 24 mars | Legal (16), CTO (02) |

### Legal (16) — Charge 3/10 → 6/10
| # | Tache | Deadline | Collabore avec |
|---|-------|----------|---------------|
| 1 | Analyse LGPL definitive — est-ce que les KG sont "derived work" ? | 22 mars | CTO (02), CEO (01) |
| 2 | CGU v1 (draft) | 24 mars | CFO (15) |
| 3 | Contribuer au document EU AI Act avec AI Safety (33) | 25 mars | AI Safety (33) |
| 4 | Review privacy policy draft | 23 mars | Security Arch (07) |

### Integration Engineer (35) — Charge 2/10 → 5/10
| # | Tache | Deadline | Collabore avec |
|---|-------|----------|---------------|
| 1 | Spec Stripe integration (plans, webhooks, facturation) | 24 mars | CFO (15), SaaS Arch (06) |
| 2 | Spec MCP Server (OdooAI comme MCP provider) | 25 mars | AI Eng (09), CTO (02) |
| 3 | Audit des APIs existantes — OpenAPI spec | 23 mars | Backend Arch (08) |

### i18n Lead (36) — Charge 1/10 → 4/10
| # | Tache | Deadline | Collabore avec |
|---|-------|----------|---------------|
| 1 | Strategie i18n : anglais d'abord, puis FR, puis multi | 23 mars | CPO (03) |
| 2 | Audit i18n du frontend — identifier les strings hardcodees | 24 mars | Frontend Eng (21) |
| 3 | Proposer un framework i18n pour Next.js (next-intl vs react-i18next) | 25 mars | Frontend Eng (21) |

### DBA & Performance (30) — Charge 2/10 → 5/10
| # | Tache | Deadline | Collabore avec |
|---|-------|----------|---------------|
| 1 | Spec migration PostgreSQL (issue #23) | 25 mars | DevOps (22), Backend Arch (08) |
| 2 | Audit des queries actuelles — N+1, full scans | 24 mars | Senior Backend (19) |
| 3 | Plan d'indexation pour les conversations (scaling 10K users) | 25 mars | SRE (23) |

### Competitive Intel (34) — Charge 3/10 → 5/10
| # | Tache | Deadline | Collabore avec |
|---|-------|----------|---------------|
| 1 | Rapport prodooctivity (issue #20) | 21 mars | — |
| 2 | Mapping des concurrents IA x Odoo (mondiaux) | 24 mars | Sales (05) |
| 3 | Battle card OdooAI vs consultants traditionnels | 25 mars | Product Marketing (46) |

---

## Nouveaux recrutes — PREMIERE SEMAINE

### Product Marketing Manager (46) — Onboarding
| # | Tache | Deadline | Collabore avec |
|---|-------|----------|---------------|
| 1 | Lire PROJECT.md, MANIFESTO.md, GLOSSARY.md | 20 mars | — |
| 2 | Messaging framework v1 (tagline, elevator pitch, value props) | 23 mars | CPO (03), Sales (05) |
| 3 | One-pager persona Marie (PME gerant) | 24 mars | CPO (03) |
| 4 | Preparer les objection handlers pour la demo | 24 mars | Sales (05) |

### Community Manager (47) — Onboarding
| # | Tache | Deadline | Collabore avec |
|---|-------|----------|---------------|
| 1 | Lire PROJECT.md, MANIFESTO.md, GLOSSARY.md | 20 mars | — |
| 2 | Audit presence Odoo — forums, OCA, LinkedIn | 22 mars | BizDev (32) |
| 3 | Plan communaute v1 (canaux, frequence, ton) | 24 mars | Content Strat (37), CPO (03) |
| 4 | Creer la page LinkedIn OdooAI (draft) | 25 mars | Brand Designer (42) |

### QA Automation Engineer (48) — Onboarding
| # | Tache | Deadline | Collabore avec |
|---|-------|----------|---------------|
| 1 | Lire PROJECT.md, CONTRIBUTING.md, codebase | 20 mars | — |
| 2 | Setup Playwright + premier test E2E (envoyer un message) | 23 mars | Frontend Eng (21) |
| 3 | 5 tests d'integration API (chat endpoint) | 24 mars | QA Lead (13), Backend Arch (08) |
| 4 | Integrer tests E2E dans le CI | 25 mars | DevOps (22) |

---

## TABLEAU DE CHARGE POST-ASSIGNATION

| Agent | Avant | Apres | Delta |
|-------|-------|-------|-------|
| Chaos Eng (31) | 2/10 | 6/10 | +4 ✅ |
| AI Safety (33) | 2/10 | 5/10 | +3 ✅ |
| Legal (16) | 3/10 | 6/10 | +3 ✅ |
| Integration Eng (35) | 2/10 | 5/10 | +3 ✅ |
| i18n Lead (36) | 1/10 | 4/10 | +3 ✅ |
| DBA (30) | 2/10 | 5/10 | +3 ✅ |
| Competitive Intel (34) | 3/10 | 5/10 | +2 ✅ |
| Product Marketing (46) | 0/10 | 5/10 | NEW ✅ |
| Community Manager (47) | 0/10 | 4/10 | NEW ✅ |
| QA Automation (48) | 0/10 | 5/10 | NEW ✅ |

**Charge moyenne equipe estimee** : 4.8/10 → **5.4/10** (mieux repartie)
**Agents a < 3/10** : 7 → **1** (i18n Lead a 4/10, tous les autres au-dessus)
**Motivation estimee** : 6.3/10 → **7.0/10** (cible atteinte)

---

## TOTAL LIVRABLES SPRINT 4

| Piste | Issues | Nouvelles taches | Total |
|-------|--------|-----------------|-------|
| A — Technique | 5 | 0 | 5 |
| B — Qualite | 4 | 0 | 4 |
| C — Business | 5 | 0 | 5 |
| D — Personnes | 6 | 0 | 6 |
| E — Infra | 3 | 0 | 3 |
| F — Legal & Compliance | 0 | 4 | 4 |
| G — Resilience | 0 | 4 | 4 |
| H — i18n & Integrations | 0 | 6 | 6 |
| I — Marketing & Community | 0 | 7 | 7 |
| J — QA Automation | 0 | 4 | 4 |
| **TOTAL** | **23** | **25** | **48** |

**48 taches, 48 agents. Tout le monde contribue.**
