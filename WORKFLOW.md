# OdooAI — Development Workflow

## Rituels d'Equipe

| Rituel | Frequence | Duree | Animateur | Sauvegarde |
|--------|-----------|-------|-----------|------------|
| **Kick-Off Phase/Sprint** | Debut de chaque phase/sprint | 2-3h | PM + CTO | `meetings/kickoff/YYYY-MM-DD-sprintX.md` |
| **Daily Standup** | Chaque jour | 45 min | PM | `meetings/daily/YYYY-MM-DD.md` |
| **Weekly Recap** | Vendredi | PM redige | PM | `meetings/weekly/YYYY-WXX.md` |
| **Sprint Retro** | Fin de sprint | 1h | PM | `meetings/retro/YYYY-MM-DD-sprintX.md` |

### Kick-Off (obligatoire a chaque debut de phase/sprint)
Le kick-off lance officiellement une phase ou un sprint. **TOUS les 42 agents participent.**
Le kick-off produit un **plan d'action concret** — pas juste une presentation.

**Contenu obligatoire :**
1. Direction cadre les objectifs et contraintes du sprint
2. Chaque agent recoit son assignment avec deadline et dependances
3. Les pistes de travail paralleles sont explicites (technique, business, legal, etc.)
4. Les dependances inter-agents sont identifiees (si X bloque, Y ne peut pas avancer)
5. Les VETOs potentiels sont identifies AVANT de coder
6. Les risques sont documentes avec mitigations et owners
7. Les metriques de succes du sprint sont definies
8. Le plan d'action est reporte dans `tasks/todo.md`

**Objectif** : apres le kick-off, chaque agent sait exactement quoi faire, quand, pourquoi, et qui depend de lui. Personne n'avance a l'aveugle.

Sauvegarde : `meetings/kickoff/`

### Daily Standup (avec challenges obligatoires)
Pas un rapport de status — un **debat**. Chaque agent avec un VETO doit poser au moins 1 question critique.
Les agents "en veille" participent aussi — leur expertise anticipe les problemes.
Details : voir [meetings/DAILY_STANDUP.md](meetings/DAILY_STANDUP.md)

### Sprint Retro (avec challenges obligatoires)
TOUS les 42 agents challengent le travail du sprint. Pas de consensus mou.
Le score de satisfaction doit refleter la realite, pas l'optimisme.

---

## La Regle d'Or : RIEN ne se code sans spec

```
SPEC → REVIEW → CODE → REVIEW → TEST → MERGE → DEPLOY
  ↑                                                 ↓
  └──────── feedback loop (si probleme) ────────────┘
```

---

## 1. Specs (avant tout code)

### Format d'un Spec ID
```
ODAI-[DOMAIN]-[NUMBER]

Domains :
  CORE    → Architecture, framework, fondations
  SEC     → Securite
  AGENT   → Agents du produit (BA, Visionary, etc.)
  API     → API, endpoints, integrations
  UI      → Frontend, mobile, design
  DATA    → Knowledge Graphs, pipelines, DB
  INFRA   → Infrastructure, CI/CD, monitoring
  BIZ     → Business (pricing, onboarding, growth)

Exemples :
  ODAI-CORE-001   → Setup du projet, structure, config
  ODAI-SEC-012    → Pipeline d'anonymisation des donnees
  ODAI-AGENT-003  → Business Analyst agent system prompt
  ODAI-API-007    → Integration Stripe Billing
  ODAI-UI-015     → Chat streaming UI
  ODAI-DATA-005   → Knowledge Graph schema v1
```

### Contenu d'une Spec
```markdown
# ODAI-[DOMAIN]-[NUMBER] — [Titre]

## Auteur
[Agent qui a redige la spec]

## Reviewers
[Agents qui doivent valider AVANT le code]

## Contexte
[Pourquoi cette spec existe. Quel probleme on resout.]

## Objectif
[Ce qu'on veut atteindre. Definition of Done claire.]

## Design
[Comment on le fait. Architecture, schemas, flux.]

## Fichiers Impactes
[Liste des fichiers a creer ou modifier]

## Securite
[Impact securite. Review par Security Architect si applicable.]

## Tests
[Strategie de test. Quels cas tester.]

## Dependances
[Autres specs dont celle-ci depend]

## Estimation
[S / M / L / XL]

## Status
[DRAFT → IN REVIEW → APPROVED → IN PROGRESS → DONE]
```

### Ou vivent les specs
```
specs/
  ODAI-CORE-001-project-setup.md
  ODAI-SEC-012-anonymization-pipeline.md
  ODAI-AGENT-003-business-analyst.md
  ...
```

### Qui review les specs
| Domain | Reviewers obligatoires |
|--------|----------------------|
| CORE | CTO + Backend Architect |
| SEC | Security Architect + CTO |
| AGENT | AI Engineer + Odoo Expert + Prompt Engineer |
| API | Backend Architect + Integration Engineer |
| UI | CPO + UX Designer + Frontend Engineer |
| DATA | Data Engineer + Odoo Expert + AI Engineer |
| INFRA | CTO + SRE + DevSecOps |
| BIZ | CEO + CFO + SaaS Architect |

---

## 2. Git Workflow

### Branches
```
main              → Production (protege, merge via PR uniquement)
staging           → Pre-production (auto-deploy depuis main)
feature/ODAI-XXX  → Feature branch (depuis main)
hotfix/ODAI-XXX   → Hotfix (depuis main, merge rapide)
```

### Commit Messages
```
Format OBLIGATOIRE :

[ODAI-XXX] type: description courte

Types :
  feat     → Nouvelle fonctionnalite
  fix      → Correction de bug
  refactor → Refactoring sans changement de comportement
  test     → Ajout ou modification de tests
  docs     → Documentation
  chore    → Maintenance (deps, config, CI)
  sec      → Correction de securite

Exemples :
  [ODAI-CORE-001] feat: initialize project structure with FastAPI and config
  [ODAI-SEC-012] feat: implement field-level anonymization pipeline
  [ODAI-SEC-012] test: add tests for mask_email and round_hundred methods
  [ODAI-AGENT-003] feat: create Business Analyst system prompt v1
  [ODAI-UI-015] fix: streaming response flickers on mobile Safari

Regles :
  - Le Spec ID est OBLIGATOIRE (sauf pour chore sans spec)
  - Description en anglais, present tense, imperative
  - Max 72 caracteres sur la premiere ligne
  - Corps optionnel pour les details (separe par une ligne vide)
```

### Pull Requests
```
Titre : [ODAI-XXX] type: description

Corps :
  ## What
  [Ce qui change]

  ## Why
  [Pourquoi ce changement]

  ## Spec
  Link vers la spec : specs/ODAI-XXX-...md

  ## Testing
  [Comment tester / quels tests ajoutés]

  ## Screenshots (si UI)
  [Avant / Apres]

  ## Checklist
  - [ ] Code en anglais
  - [ ] Docstrings sur toutes les fonctions publiques
  - [ ] Types hints complets
  - [ ] Tests ecrits et passes
  - [ ] Ruff lint passe
  - [ ] Mypy passe
  - [ ] Spec ID dans chaque commit
  - [ ] Security review (si touche aux donnees/auth/LLM)
  - [ ] Eval LLM passe (si touche aux prompts)
```

### Reviews obligatoires
| Type de PR | Reviewers minimum |
|-----------|------------------|
| Backend (CORE, SEC, API) | Senior Backend Dev + Backend Architect |
| Agents (AGENT) | AI Engineer + Prompt Engineer + Odoo Expert |
| Frontend (UI) | UX Designer + Frontend Lead |
| Infrastructure (INFRA) | DevOps + SRE |
| Data (DATA) | Data Engineer + Odoo Expert |
| Securite (SEC) | Security Architect (obligatoire) |
| Tout | Au moins 2 approbations avant merge |

### Merge Rules
```
- Squash merge uniquement (1 commit propre par PR)
- Le Spec ID DOIT etre dans le commit final
- CI doit etre vert (tests, lint, type check, security scan)
- Au moins 2 approvals
- Pas de self-merge (sauf hotfix critique approuve par CTO)
- Le PR author resolve ses conversations avant merge
```

---

## 3. Tracking sur GitHub

### Labels
```
Par domain :
  core, security, agent, api, ui, data, infra, biz

Par type :
  feature, bug, refactor, test, docs, chore

Par priorite :
  P0-critical, P1-high, P2-medium, P3-low

Par status :
  spec-draft, spec-review, spec-approved, in-progress, in-review, done

Special :
  veto (un VETO a ete pose)
  blocked (bloque par une dependance)
  needs-discussion (besoin de discussion d'equipe)
```

### GitHub Projects (Kanban)
```
Colonnes :
  📋 Spec Draft       → Spec en redaction
  🔍 Spec Review      → Spec en review
  ✅ Spec Approved    → Pret a coder
  🏗️ In Progress      → En cours de dev
  👀 In Review        → PR ouverte, en review
  🧪 Testing          → En test (staging)
  ✅ Done             → Merge, deploye
```

### Qui voit quoi
```
Le PM voit : vue Kanban globale (toutes les specs, tous les agents)
Le CTO voit : filtre par domain CORE + SEC + INFRA
Le CPO voit : filtre par domain UI + AGENT + BIZ
Le CFO voit : filtre par label qui impacte les couts
Chaque agent voit : filtre par ses specs assignees
```

### Milestones
```
Chaque sprint (2 semaines) = 1 milestone GitHub
  Milestone "Sprint 1 — Fondations"
  Milestone "Sprint 2 — Agents Core"
  ...
Le PM ferme le milestone a la fin du sprint avec un rapport
```

---

## 4. Qui Enforce Quoi

| Regle | Enforce par | Comment |
|-------|-----------|---------|
| Code en anglais | Senior Backend Dev | Review PR manuelle |
| Docstrings presentes | CI (ruff) | Automatique |
| Type hints complets | CI (mypy) | Automatique |
| Spec ID dans commits | CI (hook) | Regex sur commit message |
| Tests presents | QA Lead + CI | Coverage check + review |
| Security review | Security Architect | Label obligatoire sur PR SEC |
| Guidelines respectees | Backend Architect | Review PR |
| Manifesto respecte | TOUT LE MONDE | Culture |
| 2 reviews minimum | GitHub (branch protection) | Automatique |
| No merge sans CI vert | GitHub (branch protection) | Automatique |

---

## 5. Cycle de Vie Complet d'une Feature

```
1. IDEATION
   CPO ou CEO identifie un besoin
   → Discussion avec les agents concernes

2. SPEC
   L'agent responsable redige la spec (ODAI-XXX)
   → Review par les agents listes dans le tableau
   → Si VETO → discussion + fondateur tranche
   → Si approuve → Status: APPROVED

3. PLANNING
   PM ajoute au sprint
   → Assigne a l'agent qui implemente
   → Estime (S/M/L/XL)

4. IMPLEMENTATION
   Dev cree la branche feature/ODAI-XXX
   → Code avec commits [ODAI-XXX] type: description
   → Tests ecrits en parallele
   → PR ouverte quand pret

5. REVIEW
   2 reviewers minimum (voir tableau)
   → Feedback → corrections → re-review
   → Security review si applicable
   → Eval LLM si prompts changes

6. MERGE
   CI vert + 2 approvals → squash merge dans main
   → Auto-deploy staging

7. STAGING
   Smoke tests (DevOps)
   Monitoring 24h (SRE)

8. PRODUCTION
   CTO ou PM approuve le deploy prod
   → Blue-green deploy (DevOps)
   → Monitoring 30min (SRE)
   → Done ✅

9. POST-DEPLOY
   Customer Success : communique aux clients (si feature visible)
   Technical Writer : met a jour la doc
   Content Strategist : article de blog (si feature majeure)
```
