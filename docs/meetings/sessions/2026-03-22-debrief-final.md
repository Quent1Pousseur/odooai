# Debrief Final — 2026-03-22

---

## Ce que chaque agent a fait AUJOURD'HUI

### Agents avec taches directes (code/produit)

| # | Agent | Livrable concret |
|---|-------|-----------------|
| 02 | CTO | Review pipeline, decisions archi, validation |
| 08 | Backend Arch | Business Extractor integration (action flows) |
| 09 | AI Eng | Prompt v3 + v4 (formatting), BA pipeline |
| 11 | Data Eng | Business Extractor (workflow detector, dependency graph, Q&A generator) |
| 21 | Frontend Eng | Markdown rendering pro (tables, code, headers), tool status fix |
| 25 | Prompt Eng | Prompt v3 data-first + formatting rules + few-shot |
| 27 | UX Designer | Chat rendering overhaul, remark-gfm |
| 43 | Chat Eng | Tool status single bubble (auto-update + disappear) |

### Agents R&D (code dans rnd/)

| # | Agent | Projet | Livrable |
|---|-------|--------|----------|
| 37 | Content Strat | SEO Content Generator | `generate.py` + 5 articles depuis le vrai KG |
| 38 | Observability | OTel Dashboard | `page.tsx` — 11 metriques, auto-refresh 5s |

### Agents en formation (CRs dans docs/learning/sprint5/)

| # | Agent | Sujet | Fichier |
|---|-------|-------|---------|
| 06 | SaaS Arch | Usage-based pricing | 06-saas-usage-based-pricing.md |
| 07 | Security Arch | API hardening | 07-security-api-hardening.md |
| 08 | Backend Arch | Event sourcing | 08-backend-arch-event-sourcing.md |
| 09 | AI Eng | RAG patterns | 09-ai-eng-rag-patterns.md |
| 11 | Data Eng | Graph databases | 11-data-eng-graph-databases.md |
| 13 | QA Lead | Contract testing | 13-qa-contract-testing.md |
| 15 | CFO | SaaS financial metrics | 15-cfo-saas-metrics.md |
| 19 | Senior Backend | CQRS pattern | 19-senior-backend-cqrs.md |
| 20 | Junior Backend | Python AST module | 20-junior-backend-ast-python.md |
| 21 | Frontend Eng | React Server Components | 21-frontend-react-server-components.md |
| 25 | Prompt Eng | Chain-of-thought | 25-prompt-eng-chain-of-thought.md |
| 26 | SOC | Threat modeling | 26-soc-threat-modeling.md |
| 31 | Chaos Eng | Failure mode analysis | 31-chaos-eng-failure-modes.md |
| 33 | AI Safety | Hallucination detection | 33-ai-safety-hallucination-detection.md |
| 39 | Mobile Eng | React Native Web | 39-mobile-eng-react-native-web.md |
| 41 | Support Eng | Ticket automation | 41-support-eng-ticket-automation.md |

### Agents en support/coordination

| # | Agent | Activite |
|---|-------|----------|
| 01 | CEO | Validation decisions, review pipeline |
| 03 | CPO | Review UI/UX, feedback reponses |
| 04 | PM | Tracker issues, coordination |
| 10 | Odoo Expert | Validation KG sale resolus, review action flows |
| 44 | HR Director | Process compliance, meeting |
| 45 | Wellbeing Officer | Monitoring charge |

### Agents en attente (mais avec learnings anterieurs)

| # | Agent | Dernier learning | Status |
|---|-------|-----------------|--------|
| 05 | Sales | demo storytelling (session 3) | Attente beta users |
| 12 | Infra Eng | — | Attente VPS pour staging |
| 14 | Security Auditor | penetration testing (session 2) | Attente staging pour audit |
| 16 | Legal | GDPR checklist (session 2) | Attente avocat |
| 17 | Customer Success | NPS (session 3) | Attente beta users |
| 18 | Growth | — | Attente Plausible + staging |
| 22 | DevOps | GitHub Actions CD (session 2) | Attente VPS |
| 23 | SRE | uptime monitoring (session 2) | Attente staging |
| 24 | DevSecOps | — | Rate limiting fait, attente staging |
| 28 | Data Scientist | — | Eval framework en attente BA regeneres |
| 29 | Tech Writer | in-app help (session 2) | Attente UI stable |
| 30 | DBA | Alembic (session 3) | Attente PostgreSQL staging |
| 32 | BizDev | partner program (session 3) | Attente teaser |
| 34 | Competitive Intel | AI x ERP (session 2) | Veille continue |
| 35 | Integration Eng | — | Attente MCP/Stripe sprint 6 |
| 36 | i18n Lead | next-intl (session 3) | Attente i18n sprint 6 |
| 40 | Vendor Mgr | Anthropic pricing (session 2) | Formation continue |
| 42 | Brand Designer | motion design (session 3) | Attente design system |
| 46 | Product Marketing | — | Attente teaser |
| 47 | Community Mgr | — | Attente LinkedIn launch |
| 48 | QA Automation | — | Attente staging pour E2E |

---

## PARTAGE LEARNING — Les plus impactants

**AI Eng (09) — RAG patterns** : "Au lieu d'envoyer tout le BA Profile au LLM, on devrait chunker et ne recuperer que les parties pertinentes a la question. Ca reduirait les tokens de 50% et ameliorerait la pertinence. Le Business Extractor est deja le debut d'un RAG — il structure l'info avant injection."

**Junior Backend (20) — Python AST** : "J'ai etudie le module AST qu'on utilise dans le method_analyzer. ast.walk() parcourt tout l'arbre. ast.NodeVisitor permet de cibler des patterns. Ca m'a aide a comprendre comment on detecte les self.env['model'] — c'est du pattern matching sur l'AST."

**AI Safety (33) — Hallucination detection** : "On pourrait verifier chaque reponse du LLM contre les KG. Si le LLM mentionne un champ qui n'existe pas dans le KG → hallucination detectee. Ca serait un 'fact checker' ZERO LLM, comme le Guardian."

**Chaos Eng (31) — Failure modes** : "J'ai identifie 6 composants critiques avec leur mode de defaillance. Le plus risque : le LLM qui retourne du JSON tronque (on l'a vu avec max_tokens=4096). Le fix etait simple mais sans analyse FMEA on l'aurait pas anticipe."

---

## Metriques

| Metrique | Valeur |
|----------|--------|
| Commits | 130+ |
| Tests | 225 |
| Learning CRs Sprint 5 | **35** |
| Learning CRs total | **61** |
| R&D projets actifs | **2** (avec code) |
| Articles SEO generes | 5 |
| BA Profiles regeneres | 3/9 |
| Action flows detectes | 29 (sale) |
| Selection constants resolues | 2 (SALE_ORDER_STATE, INVOICE_STATUS) |

---

## Bilan honnete

**Ce qui a bien marche :**
- Le reverse engineering pipeline est COMPLET (AST → KG → Business → BA → Chat)
- Les R&D produisent du vrai code
- 16 learning CRs cette session — les agents sans tache apprennent
- L'UI s'ameliore (tables, code blocks, tool status)

**Ce qui reste a ameliorer :**
- 20 agents en attente (staging, VPS, beta users, avocat)
- Les reponses sont "deja mieux" mais pas encore "wow"
- Le rendering markdown reste imparfait sur certains formats LLM
- 6 BA Profiles pas encore regeneres avec le nouveau pipeline

**Actions pour la prochaine session :**
1. Regenerer les 6 BA restants
2. Re-analyser les modules cles (stock, account, hr) avec le nouveau parseur
3. Les agents en attente doivent lancer des projets R&D ou approfondir leurs learnings
