# OdooAI — Instructions Claude Code

## Projet
OdooAI est un Business Analyst IA qui a lu chaque ligne du code source Odoo.
SaaS-first, closed source, concurrent de prodooctivity (pas un fork).

## Stack
- **Backend**: Python 3.11+, FastAPI (uvicorn), SQLAlchemy (async), Pydantic v2
- **LLM**: Anthropic Claude (Haiku/Sonnet/Opus selon agent)
- **Database**: SQLite (dev), PostgreSQL + asyncpg (prod)
- **Cache**: Redis
- **Frontend**: Next.js 14+ (App Router), TypeScript strict, Tailwind, Shadcn/ui
- **Testing**: pytest, Vitest + Testing Library
- **Quality**: ruff (lint+format), mypy --strict, bandit

## Structure du code (hexagonal — ODAI-CORE-001)
```
odooai/
  main.py                        # create_app() factory + lifespan wiring
  config.py                      # pydantic-settings
  exceptions.py                  # OdooAIError hierarchy (message + user_message)
  domain/
    entities/connection.py       # OdooConnection
    value_objects/               # ModelCategory, OdooUserInfo, SanitizedResponse
    ports/                       # IOdooClient, ICache, ILLMProvider, ICrypto
  services/                      # field_scorer, model_classifier
  security/                      # guardian, anonymizer, audit (ZERO LLM)
  infrastructure/                # Concrete port implementations
    odoo/client.py               # XML-RPC + JSON-RPC
    cache/redis_client.py        # Redis / in-memory
    db/database.py               # SQLAlchemy async
    llm/anthropic_provider.py    # Claude SDK
    crypto.py                    # AES-256-GCM
  api/
    dependencies.py              # wire() + Depends() factories
    middleware.py                 # RequestID
    routers/health.py            # /health
tests/                           # Mirrors odooai/ structure
knowledge_store/                 # Knowledge Graphs JSON (gitignored)
```

## Conventions code
- **Langue du code** : ANGLAIS uniquement (variables, fonctions, classes, comments, commits)
- **Langue governance** : FRANCAIS (docs projet, agents, meetings)
- Naming : snake_case (files, functions, vars), PascalCase (classes), UPPER_SNAKE_CASE (constants)
- Max 100 chars/ligne, 300 lignes/fichier, 50 lignes/fonction
- Type hints obligatoires sur toutes les fonctions publiques
- Frozen dataclasses pour les value objects
- Imports : stdlib > third-party > local (absolus, jamais relatifs)
- Exceptions typees avec `message` + `user_message`

## Workflow
- Spec ID format : `ODAI-[DOMAIN]-[NUMBER]` (CORE, SEC, AGENT, API, UI, DATA, INFRA, BIZ)
- Commit format : `[ODAI-XXX] type: description` (feat, fix, refactor, test, docs, chore, sec)
- 2 reviews minimum avant merge, squash merge only
- CI : ruff + mypy + tests + bandit doivent passer

## Commandes
```bash
make install         # pip install -e ".[dev]"
make lint            # ruff check + format
make typecheck       # mypy --strict
make test            # pytest
make check           # all checks
make run             # uvicorn dev server :8000
```

## Regles importantes
- Ne pas coder avant validation de l'architecture (feedback fondateur)
- Security Guardian = ZERO LLM (logique pure), Data Operations = ZERO LLM
- Double validation avant toute ecriture dans Odoo client
- Knowledge Graphs sont le moat : extraits du code source, pas de la doc
- LLM-agnostic : architecture permettant de switcher de provider

## Regles INTRANSIGEANTES (jamais derogeable)
- **MEETINGS OBLIGATOIRES** : daily matin + daily fin a CHAQUE session. Kick-off a chaque phase. Retro a chaque fin de sprint. JAMAIS oublier.
- **ZERO INACTIVITE** : a chaque daily matin, verifier que les 48 agents ont une tache, aident un collegue, ou se forment (CR dans learning/). Template : hr/daily-checklist-template.md. PERSONNE ne reste inactif.
- **SPECS AVANT CODE** : RIEN ne se code sans spec ODAI-XXX ecrite et committee.
- **REVIEWS DOCUMENTEES** : chaque review interne est sauvegardee dans reviews/. Le fondateur doit pouvoir les lire.
- **CHALLENGES ACTIFS** : les agents DOIVENT se challenger dans les meetings. Pas de consensus mou.
- **LEARNING SI PAS DE TACHE** : tout agent sans tache produit un CR de formation dans learning/ le jour meme.
- **VERIFICATION CRs BLOQUANTE** : a chaque daily matin, Section 0 du template = verifier que les CRs de la session precedente existent. Si un CR manque, l'agent le produit AVANT toute discussion. J'ai ete rappele 5 FOIS — c'est fini.
- **KPIs MESURABLES** : chaque agent a des KPIs dans hr/kpis-individuels.md. Verifies a chaque retro. Pas de KPI = pas de mesure = pas de progres.
- **WEEKLY RECAP** : chaque vendredi, le PM + CEO font un weekly dans meetings/weekly/. Budget, KPIs, risques, plan. Template : meetings/weekly/template.md.
- **BUDGET TRACKER** : le CFO met a jour budget/budget-tracker.md chaque semaine. Couts LLM + infra + outils.
- **PROCESS.md** : le document central. TOUT le monde le lit. Si un process n'est pas dans PROCESS.md, il n'existe pas.
