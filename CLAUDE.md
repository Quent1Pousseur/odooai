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
- **ZERO INACTIVITE** : verifier que les 48 agents ont tache/aide/R&D/formation. Template : docs/hr/session-checklist.md.
- **SPECS AVANT CODE** : RIEN ne se code sans spec dans docs/specs/. Template : docs/TEMPLATES.md.
- **REVIEWS DOCUMENTEES** : chaque review dans docs/reviews/. Template obligatoire.
- **CHALLENGES ACTIFS** : les agents DOIVENT se challenger dans les meetings. Pas de consensus mou.
- **R&D OU LEARNING SI PAS DE TACHE** : R&D dans docs/rnd/, formation dans docs/learning/sprintN/. R&D > formation. Voir docs/hr/cellule-rnd.md.
- **VERIFICATION CRs BLOQUANTE** : Section 0 du template session = verifier CRs AVANT toute discussion. Rappele 5 FOIS — c'est fini.
- **KPIs MESURABLES** : docs/hr/kpis.md. Verifies a chaque retro.
- **BUDGET TRACKER** : docs/governance/budget-tracker.md. CFO chaque semaine.
- **TEMPLATES OBLIGATOIRES** : tout fichier suit le template de son type (docs/TEMPLATES.md). Review rejetee si non-conforme.
- **PROCESS.md** : le document central. Si un process n'est pas dans PROCESS.md, il n'existe pas.
