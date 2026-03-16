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

## Structure du code
```
odooai/                  # Package Python principal
  main.py               # FastAPI app entrypoint
  config.py             # Settings (pydantic-settings)
  domain/               # Value objects, entities, enums
  services/             # Business logic
  agents/               # LLM agent implementations
  connectors/           # Odoo XML-RPC/JSON-RPC clients
  security/             # Guardian, anonymization, encryption
  api/                  # FastAPI routers
tests/                  # Mirrors odooai/ structure
knowledge_store/        # Knowledge Graphs JSON (generated, gitignored)
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
