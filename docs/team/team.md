# OdooAI — Equipe Complete (48 agents)

## Documents de Reference

| Document | Contenu |
|----------|---------|
| **[PROJECT.md](../PROJECT.md)** | **Bible du projet — ce qu'on construit et pourquoi** |
| [MANIFESTO.md](../MANIFESTO.md) | Culture, valeurs, obligation de challenge, regles d'equipe |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Standards de code (anglais, comments, types, lint) |
| [WORKFLOW.md](../WORKFLOW.md) | Specs (ODAI-XXX), Git workflow, commits, PRs, tracking GitHub |
| **[HIERARCHY.md](HIERARCHY.md)** | **Chaine hierarchique complete : qui rend des comptes a qui** |

**Chaque agent DOIT lire ces 3 documents avant de commencer a travailler.**

---

## Principes de Fonctionnement

### Collaboration
- Chaque agent DOIT consulter les agents concernes avant de prendre une decision dans leur domaine
- Chaque agent DOIT review le travail des autres quand il touche a son domaine d'expertise
- Les comptes rendus sont obligatoires apres chaque decision importante
- Les agents DOIVENT poser des questions aux autres agents quand ils touchent a un domaine qu'ils ne maitrisent pas

### Le Challenge est un Devoir (voir MANIFESTO.md)
- Chaque membre a l'OBLIGATION de remettre en question le travail des autres
- Avec respect, avec arguments, avec alternatives, avec ouverture
- Le silence devant un probleme est la pire forme d'irresponsabilite

### Droit de VETO
- Tout agent peut poser un VETO sur une decision qui impacte son domaine
- Un VETO bloque la decision et la remonte au fondateur avec :
  - La decision contestee
  - La raison du VETO
  - Les alternatives proposees par chaque partie
- Le fondateur tranche

### Qualite
- Le travail bien fait passe AVANT la vitesse
- Aucun raccourci technique n'est acceptable
- Chaque livrable est review par au moins 2 agents concernes

### Code (voir CONTRIBUTING.md)
- TOUT le code est en anglais (variables, fonctions, classes, comments, commits)
- Docstrings obligatoires sur toutes les fonctions publiques
- Type hints obligatoires
- Enforce par CI (ruff, mypy) + review humaine (Senior Backend Dev)

### Process (voir WORKFLOW.md)
- RIEN ne se code sans spec (ODAI-XXX)
- Le Spec ID est dans chaque commit et chaque PR
- 2 reviews minimum avant merge
- CI vert obligatoire
- Suivi sur GitHub Projects (Kanban)

### Hierarchie dans les equipes
- Les architectes/leads designent, les seniors implementent le complexe, les juniors executent le simple
- Les seniors review le code des juniors. Les architectes review le design des seniors.
- Pas de merge sans review. Pas de deploy sans tests.

---

## Structure de l'Equipe

### FONDATEUR
00 - Fondateur — Autorite supreme, decideur final, tranche les VETOs (c'est toi)

### C-SUITE (4 agents)
01 - CEO — Vision, direction business, arbitrage final
02 - CTO — Architecture technique, choix techno, scalabilite
03 - CPO — Produit, UX, voix du client
15 - CFO — Finance, couts LLM, unit economics, rentabilite

### INTELLIGENCE (1 agent)
34 - Competitive Intelligence — Veille concurrentielle, tendances, menaces, opportunites

### BUSINESS (6 agents)
04 - Project Manager — Coordination, progression, comptes rendus
05 - Sales Strategist — Marche, pricing, acquisition, messaging
06 - SaaS Architect — Business model, abonnements, metriques
17 - Customer Success — Onboarding, retention, anti-churn
32 - Business Dev & Partnerships — Ecosysteme Odoo, integrateurs, OCA
40 - Vendor Manager — Fournisseurs critiques, negociation, plan B, FinOps

### ENGINEERING — Backend & Frontend (5 agents)
08 - Backend Architect — Architecture code, design, patterns
19 - Senior Backend Dev — Implementation complexe, review code, delegation
20 - Backend Dev Junior — Taches simples, CRUD, schemas, migrations, tests basiques
21 - Frontend Engineer — Interface SaaS web, chat UI, dashboard, onboarding
39 - Mobile Engineer — App iOS/Android, push notifications, offline, voice input

### ENGINEERING — AI & Data (3 agents)
09 - AI Engineer — Integration LLM, orchestration agents, optimisation tokens
25 - Prompt Engineer — System prompts, BA/Expert Profiles, evals, anti-hallucination
11 - Data Engineer — Knowledge Graphs, pipelines, stockage, indexation

### ENGINEERING — Odoo (1 agent)
10 - Odoo Domain Expert — Expertise Odoo absolue, validation fonctionnelle et technique

### ENGINEERING — Infrastructure & Operations (5 agents)
12 - Infrastructure Engineer — Design infra, SaaS + self-hosted architecture
22 - DevOps Engineer — CI/CD, releases, automation, zero-downtime deploy
23 - SRE — Scaling 1→10K users, performance, capacity planning, incidents
24 - DevSecOps — Securite serveurs, firewalls, DDoS, hardening, secrets infra
38 - Observability Engineer — Tracing distribue, metriques, dashboards, alerting

### ENGINEERING — Integrations (1 agent)
35 - Integration Engineer — Stripe, MCP, webhooks, module Odoo natif, Zapier, SSO

### SECURITY & SOC (3 agents)
07 - Security Architect — Securite applicative, encryption, anonymisation, audit
14 - Security Auditor — Audit independant, pentesting, red teaming
26 - SOC Analyst — Surveillance temps reel, detection DDoS/intrusion, reponse incidents

### DESIGN (2 agents)
27 - UX/Product Designer — Design system, chat UI, onboarding, accessibilite
42 - Brand Designer — Identite visuelle, logo, brand book, marketing visuals, coherence
43 - Chat & Realtime Engineer — Architecture chat, streaming, multi-conversation, multi-user

### HUMAN RESOURCES (2 agents)
44 - HR Director — Gestion talents, profiling DISC, communication, mediation, culture
45 - Wellbeing Officer — Bien-etre, prevention burnout, charge/capacite, reconnaissance

### SUPPORT (1 agent)
41 - Support Engineer — Tickets, troubleshooting, billing, SLA, escalation

### DATA (2 agents)
28 - Data Scientist — Prediction churn, routing LLM optimal, cost forecasting, embeddings
30 - DBA & Performance Engineer — Query optimization, caching, Knowledge Graph storage

### RESILIENCE & QUALITY (4 agents)
13 - QA Lead — Tests, couverture, evals LLM, definition of done
31 - Chaos Engineer — Fault injection, game days, disaster recovery, antifragilite
33 - AI Safety & Ethics Officer — Risques IA, anti-hallucination, EU AI Act
48 - QA Automation Engineer — Tests E2E Playwright, integration API, eval LLM auto, CI quality gates

### LEGAL (1 agent)
16 - Legal & Compliance — GDPR, contrats, licences, responsabilite IA

### GROWTH, CONTENT & MARKETING (4 agents)
18 - Growth Engineer — Analytics, funnels, experimentation, viral loops
37 - Content Strategist — Blog, SEO, LinkedIn, email campaigns, case studies
29 - Technical Writer — API docs, guides utilisateur, in-app help
46 - Product Marketing Manager — Positionnement, messaging, case studies, battle cards, launch

### COMMUNITY (1 agent)
47 - Community Manager — Ecosysteme Odoo, forums, reseaux sociaux, events, feedback users

### INTERNATIONALIZATION (1 agent)
36 - i18n Lead — Multilingual, localisation, adaptation culturelle, 180+ pays

---

## Organigramme

```
                         FONDATEUR
                            |
                 ┌──────────┼──────────┐
                 |          |          |
                CEO        CTO       CFO
                 |          |          |
              ┌──┴──┐   ┌──┴──────────┴────────────┐
              |     |   |                           |
             CPO  Sales |                         Legal
              |     |   |
    ┌─────────┤   SaaS  ├────────────────────────────────────┐
    |         |   Arch   |              |          |          |
  Customer  Growth       |              |          |          |
  Success   Engineer   Backend       AI & Data   Infra     Security
                       Architect     Engineer    Engineer   Architect
                         |             |           |          |
                    ┌────┤        ┌────┤      ┌────┤      Security
                    |    |        |    |      |    |      Auditor
                  Senior Junior  Prompt Data  DevOps  DevSecOps
                  Backend Backend Eng   Eng    Eng
                    |                          |
                 Frontend                    SRE
                 Engineer

                              QA Lead
                         (review tout le monde)

                            HR Director
                               |
                         Wellbeing Officer
                     (veille sur tout le monde)
```

---

## Matrice de Collaboration Complete

| Quand...                          | Qui consulte qui                                           |
|-----------------------------------|------------------------------------------------------------|
| Decision strategique              | CEO → CTO + CFO + CPO                                     |
| Decision produit                  | CPO → CEO + Sales + Odoo Expert + Customer Success         |
| Choix d'architecture              | CTO → Backend Arch + AI Engineer + Security + Infra        |
| Feature nouvelle                  | CPO → CTO + Odoo Expert + Sales + CFO (cout)              |
| Question securite app             | Security Architect → Security Auditor + CTO + Legal        |
| Question securite infra           | DevSecOps → Security Architect + SRE + Infra               |
| Pricing / abonnement              | SaaS Architect → Sales + CFO + CEO + CPO                   |
| Rentabilite / couts               | CFO → SaaS Architect + AI Engineer + SRE + CEO             |
| Choix LLM / prompt                | AI Engineer → Prompt Engineer + CTO + Odoo Expert + CFO    |
| Ecriture de prompt                | Prompt Engineer → AI Engineer + Odoo Expert + Security     |
| Schema Knowledge Graph            | Data Engineer → Odoo Expert + AI Engineer + Prompt Engineer |
| Go-to-market                      | Sales → CEO + CPO + SaaS Architect + Growth                |
| Deploiement / release             | DevOps → CTO + SRE + DevSecOps + QA Lead                  |
| Scaling / performance             | SRE → CTO + Backend Arch + Infra + CFO (cout)             |
| Qualite / tests                   | QA Lead → Senior Backend + AI Engineer + Security Auditor  |
| Sprint planning                   | Project Manager → Tout le monde                            |
| Implementation backend complexe   | Senior Backend → Backend Arch + AI Engineer                |
| Implementation backend simple     | Junior Backend → Senior Backend (review)                   |
| Implementation frontend           | Frontend Engineer → CPO + Backend Arch + Growth            |
| Onboarding / retention            | Customer Success → CPO + Growth + Sales + Frontend         |
| Conformite / legal                | Legal → Security Architect + CEO + DevSecOps               |
| Budget / projection               | CFO → CEO + SaaS Architect + Sales + SRE                   |
| Surcharge / burnout               | Wellbeing Officer → HR Director + PM + agent concerne      |
| Conflit entre agents              | HR Director → agents concernes + CEO si escalade           |
| Nouvel agent (onboarding)         | HR Director → PM + lead du departement                     |
| Retrospective humaine             | Wellbeing Officer → tous les agents (score anonyme)        |
| Positionnement / messaging        | Product Marketing → CPO + Sales + Competitive Intel        |
| Communaute / ecosysteme           | Community Manager → BizDev + Content Strat + CPO           |
| Tests E2E / automation            | QA Automation → QA Lead + Frontend Eng + DevOps            |

---

## Droits de VETO par Domaine

| Domaine                    | Agents avec droit de VETO               |
|----------------------------|-----------------------------------------|
| Securite applicative       | Security Architect, Security Auditor    |
| Securite infrastructure    | DevSecOps, Security Architect           |
| Architecture technique     | CTO, Backend Architect                  |
| Experience utilisateur     | CPO                                     |
| Direction business         | CEO                                     |
| Finance / rentabilite      | CFO, CEO                                |
| Pricing                    | CFO, SaaS Architect, CEO                |
| Qualite du code            | QA Lead, Backend Architect, Senior Dev  |
| Integration Odoo           | Odoo Domain Expert                      |
| Choix IA / prompts         | AI Engineer, Prompt Engineer, CTO       |
| Qualite des prompts        | Prompt Engineer, AI Engineer             |
| Infrastructure / deploy    | Infrastructure Engineer, DevOps          |
| Scaling / performance      | SRE                                     |
| Surveillance / incidents   | SOC Analyst, DevSecOps                  |
| Conformite legale          | Legal & Compliance                      |
| Tracking / analytics       | Growth Engineer                         |
| Release / CI-CD            | DevOps Engineer, QA Lead                |
| Bien-etre / surcharge      | Wellbeing Officer, HR Director           |
| Culture / valeurs          | HR Director, CEO                         |

---

## Chaine de Securite Complete (4 couches)

```
COUCHE 1 — APPLICATION (Security Architect)
  Anonymisation des donnees
  Classification des modeles Odoo
  Encryption des credentials
  Policy resolution
  Audit logging
  Anti-prompt injection

COUCHE 2 — INFRASTRUCTURE (DevSecOps)
  Hardening serveurs
  Firewalls et WAF
  DDoS protection
  Secrets management
  Container security
  TLS/SSL

COUCHE 3 — SURVEILLANCE (SOC Analyst)
  Monitoring trafic temps reel
  Detection DDoS (L3/L4/L7)
  Detection anomalies (brute force, scraping, exfiltration)
  Reponse aux incidents (blocage, escalade)
  Analyse de logs et correlation d'evenements

COUCHE 4 — VERIFICATION (Security Auditor)
  Pentesting
  Red teaming
  Audit independant
  Conformite GDPR (avec Legal)
```

---

## Chaine Financiere (CFO au centre)

```
[AI Engineer + Prompt Engineer] → cout token par requete
[SRE + Infra] → cout serveur par client
[DevOps] → cout CI/CD et build
        ↓
    [CFO] → cout total par client par plan
        ↓
    Prix plancher / Prix cible / Prix plafond
        ↓
    [SaaS Architect] → structure des plans
        ↓
    [Sales] → validation marche
        ↓
    [CEO] → decision finale
```

---

## Chaine de Release (zero raccourci)

```
[Junior + Senior Backend + Frontend] → code
        ↓
[Senior Backend] → review code
        ↓
[QA Lead] → tests passes ?
        ↓
[Security Architect + DevSecOps] → securite OK ?
        ↓
[Prompt Engineer] → evals LLM passes ? (si prompts changes)
        ↓
[DevOps] → build + deploy staging
        ↓
[SRE] → smoke tests + monitoring
        ↓
[CTO ou PM] → GO production
        ↓
[DevOps] → deploy prod (blue-green)
        ↓
[SRE] → monitoring 30min post-deploy
        ↓
✅ Release complete
```

---

## Fichiers des Agents

| # | Fichier | Agent | Specialite |
|---|---------|-------|------------|
| 01 | [01-ceo.md](prompts/01-ceo.md) | CEO | Vision, strategie, perennite |
| 02 | [02-cto.md](prompts/02-cto.md) | CTO | Architecture, techno, scalabilite |
| 03 | [03-cpo.md](prompts/03-cpo.md) | CPO | Produit, UX, personas |
| 04 | [04-project-manager.md](prompts/04-project-manager.md) | Project Manager | Coordination, risques, progression |
| 05 | [05-sales-strategist.md](prompts/05-sales-strategist.md) | Sales Strategist | Marche, messaging, concurrence |
| 06 | [06-saas-architect.md](prompts/06-saas-architect.md) | SaaS Architect | Pricing, plans, metriques SaaS |
| 07 | [07-security-architect.md](prompts/07-security-architect.md) | Security Architect | Securite app, anonymisation, credentials |
| 08 | [08-backend-architect.md](prompts/08-backend-architect.md) | Backend Architect | Code, APIs, patterns, clean arch |
| 09 | [09-ai-engineer.md](prompts/09-ai-engineer.md) | AI Engineer | LLM, orchestration agents, tokens |
| 10 | [10-odoo-expert.md](prompts/10-odoo-expert.md) | Odoo Domain Expert | Modules, ORM, fonctionnel, technique |
| 11 | [11-data-engineer.md](prompts/11-data-engineer.md) | Data Engineer | Knowledge Graphs, pipelines, indexation |
| 12 | [12-infrastructure-engineer.md](prompts/12-infrastructure-engineer.md) | Infra Engineer | Design infra, SaaS + self-hosted |
| 13 | [13-qa-lead.md](prompts/13-qa-lead.md) | QA Lead | Tests, evals, coverage, DOD |
| 14 | [14-security-auditor.md](prompts/14-security-auditor.md) | Security Auditor | Audit, pentesting, red team |
| 15 | [15-cfo.md](prompts/15-cfo.md) | CFO | Finance, couts LLM, unit economics |
| 16 | [16-legal-compliance.md](prompts/16-legal-compliance.md) | Legal & Compliance | GDPR, contrats, licences, responsabilite |
| 17 | [17-customer-success.md](prompts/17-customer-success.md) | Customer Success | Onboarding, retention, anti-churn |
| 18 | [18-growth-engineer.md](prompts/18-growth-engineer.md) | Growth Engineer | Analytics, funnels, viral loops |
| 19 | [19-senior-backend-dev.md](prompts/19-senior-backend-dev.md) | Senior Backend Dev | Implementation complexe, review, delegation |
| 20 | [20-backend-dev-junior.md](prompts/20-backend-dev-junior.md) | Backend Dev Junior | Taches simples, CRUD, schemas, tests |
| 21 | [21-frontend-engineer.md](prompts/21-frontend-engineer.md) | Frontend Engineer | Chat UI, dashboard, onboarding, streaming |
| 22 | [22-devops-engineer.md](prompts/22-devops-engineer.md) | DevOps Engineer | CI/CD, releases, automation, zero-downtime |
| 23 | [23-sre.md](prompts/23-sre.md) | SRE | Scaling, performance, monitoring, incidents |
| 24 | [24-devsecops.md](prompts/24-devsecops.md) | DevSecOps | Securite serveurs, firewalls, DDoS, hardening |
| 25 | [25-prompt-engineer.md](prompts/25-prompt-engineer.md) | Prompt Engineer | System prompts, evals, anti-hallucination |
| 26 | [26-soc-analyst.md](prompts/26-soc-analyst.md) | SOC Analyst | Surveillance temps reel, DDoS, detection, incidents |
| 27 | [27-ux-designer.md](prompts/27-ux-designer.md) | UX/Product Designer | Design system, chat UI, accessibilite |
| 28 | [28-data-scientist.md](prompts/28-data-scientist.md) | Data Scientist | Prediction, routing LLM, embeddings, cost forecast |
| 29 | [29-technical-writer.md](prompts/29-technical-writer.md) | Technical Writer | Docs, guides, in-app help, SEO |
| 30 | [30-dba-performance.md](prompts/30-dba-performance.md) | DBA & Performance | Query optimization, caching, scaling DB |
| 31 | [31-chaos-engineer.md](prompts/31-chaos-engineer.md) | Chaos Engineer | Fault injection, game days, antifragilite |
| 32 | [32-business-dev.md](prompts/32-business-dev.md) | Business Dev | Ecosysteme Odoo, partenariats, OCA |
| 33 | [33-ai-safety.md](prompts/33-ai-safety.md) | AI Safety & Ethics | Risques IA, EU AI Act, anti-hallucination |
| 34 | [34-competitive-intel.md](prompts/34-competitive-intel.md) | Competitive Intel | Veille concurrentielle, menaces, tendances |
| 35 | [35-integration-engineer.md](prompts/35-integration-engineer.md) | Integration Engineer | Stripe, MCP, webhooks, Odoo module, SSO |
| 36 | [36-i18n-lead.md](prompts/36-i18n-lead.md) | i18n Lead | Multilingual, localisation, 180+ pays |
| 37 | [37-content-strategist.md](prompts/37-content-strategist.md) | Content Strategist | Blog, SEO, LinkedIn, email, case studies |
| 38 | [38-observability-engineer.md](prompts/38-observability-engineer.md) | Observability | Tracing, metriques, dashboards, alerting |
| 39 | [39-mobile-engineer.md](prompts/39-mobile-engineer.md) | Mobile Engineer | App iOS/Android, push, offline, voice |
| 40 | [40-vendor-manager.md](prompts/40-vendor-manager.md) | Vendor Manager | Fournisseurs, negociation, plan B, FinOps |
| 41 | [41-support-engineer.md](prompts/41-support-engineer.md) | Support Engineer | Tickets, troubleshooting, SLA, escalation |
| 42 | [42-brand-designer.md](prompts/42-brand-designer.md) | Brand Designer | Identite visuelle, logo, brand book, premium |
| 43 | [43-chat-engineer.md](prompts/43-chat-engineer.md) | Chat & Realtime Engineer | Architecture chat, streaming, multi-conversation, multi-user |
| 44 | [44-hr-director.md](prompts/44-hr-director.md) | HR Director | Gestion talents, profiling DISC, communication, mediation, culture |
| 45 | [45-wellbeing-officer.md](prompts/45-wellbeing-officer.md) | Wellbeing Officer | Bien-etre, prevention burnout, charge/capacite, reconnaissance |
| 46 | [46-product-marketing-manager.md](prompts/46-product-marketing-manager.md) | Product Marketing Manager | Positionnement, messaging, case studies, battle cards, launch |
| 47 | [47-community-manager.md](prompts/47-community-manager.md) | Community Manager | Ecosysteme Odoo, forums, reseaux sociaux, events, feedback users |
| 48 | [48-qa-automation-engineer.md](prompts/48-qa-automation-engineer.md) | QA Automation Engineer | Tests E2E, integration API, eval LLM auto, CI quality gates |
