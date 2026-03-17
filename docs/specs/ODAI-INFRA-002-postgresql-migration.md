# ODAI-INFRA-002 — Migration SQLite → PostgreSQL

## Status
SPEC READY

## Auteur
DBA & Performance (30)

## Reviewers
Backend Architect (08), CTO (02), SRE (23)

## Date
2026-03-21

## Contexte
SQLite suffit en dev mais ne tiendra pas en prod multi-tenant :
- Pas de connexions concurrentes (1 writer a la fois)
- Pas de full-text search natif
- Pas de JSONB pour les metadonnees
- Pas de backup point-in-time (PITR)

## Schema actuel (SQLite)

```sql
-- conversations
CREATE TABLE conversations (
    id TEXT PRIMARY KEY,
    title TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- messages
CREATE TABLE messages (
    id TEXT PRIMARY KEY,
    conversation_id TEXT REFERENCES conversations(id),
    role TEXT NOT NULL,  -- 'user' | 'assistant'
    content TEXT NOT NULL,
    domain TEXT,
    tokens INTEGER DEFAULT 0,
    sources TEXT,  -- JSON array as string
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Schema PostgreSQL cible

```sql
-- conversations
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    title VARCHAR(255),
    user_id UUID,  -- prep multi-tenant
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_conversations_updated ON conversations(updated_at DESC);

-- messages
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(10) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    domain VARCHAR(50),
    tokens INTEGER DEFAULT 0,
    sources JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT now()
);

CREATE INDEX idx_messages_conversation ON messages(conversation_id, created_at);
CREATE INDEX idx_messages_domain ON messages(domain);
```

## Changements cles

| Aspect | SQLite | PostgreSQL |
|--------|--------|-----------|
| IDs | TEXT (UUID string) | UUID natif |
| Timestamps | TIMESTAMP | TIMESTAMPTZ (timezone-aware) |
| sources | TEXT (JSON string) | JSONB (queryable) |
| metadata | — | JSONB (extensible) |
| user_id | — | UUID (prep multi-tenant) |
| Indexes | Aucun | 4 indexes |
| ON DELETE | Manuel | CASCADE |
| Concurrence | 1 writer | Illimite |

## Index strategy (challenge DBA)

- `idx_conversations_user` — pour le multi-tenant (toutes les convs d'un user)
- `idx_conversations_updated` — pour le tri par recence (sidebar)
- `idx_messages_conversation` — pour charger les messages d'une conv (composite)
- `idx_messages_domain` — pour les analytics par domaine

## Migration

### Etape 1 — Double driver (Sprint 5)
- `DATABASE_URL=sqlite+aiosqlite:///` → SQLite (dev)
- `DATABASE_URL=postgresql+asyncpg://` → PostgreSQL (staging/prod)
- SQLAlchemy async gere les deux avec le meme code

### Etape 2 — Alembic (Sprint 5)
- Ajouter Alembic pour les migrations
- Migration initiale = schema PostgreSQL ci-dessus
- SQLite reste en dev sans Alembic (create_all)

### Etape 3 — Docker compose avec PostgreSQL (Sprint 5)
- Ajouter un service `db` dans docker-compose
- `DATABASE_URL=postgresql+asyncpg://odooai:odooai@db:5432/odooai`

## Estimation
M (2-3 jours) — Alembic setup + migration + tests + docker update

## Definition of Done
- [ ] Alembic initialise avec migration PostgreSQL
- [ ] docker-compose avec service PostgreSQL
- [ ] Tests passent sur SQLite ET PostgreSQL
- [ ] Documentation mise a jour
