# Learning — DBA (30) — Alembic Migration Patterns for Async SQLAlchemy
## Date : 2026-03-21 (Sprint 5, session 2)
## Duree : 3 heures

## Ce que j'ai appris

1. **Alembic supporte nativement async depuis la v1.7** — La configuration utilise
   `run_async` dans `env.py` avec `connectable = create_async_engine(url)`. Le pattern
   cle est d'envelopper la migration dans `async_engine.begin()` et d'appeler
   `run_sync(do_migrations)` sur la connexion async. Ca evite de maintenir un engine sync
   separe juste pour les migrations.

2. **L'autogeneration avec async necessite un metadata explicite** — Alembic autogenerate
   compare le schema en base avec le metadata SQLAlchemy. En async, il faut passer
   `target_metadata = Base.metadata` dans `env.py` et s'assurer que tous les models sont
   importes avant l'appel. Un `import odooai.infrastructure.db.models` explicite dans
   `env.py` est obligatoire.

3. **Les migrations "online" vs "offline" ont des implications differentes en async** — Le
   mode offline genere du SQL brut sans connexion (utile pour review). Le mode online
   execute directement. En production async avec asyncpg, toujours utiliser le mode online
   avec `run_async` pour eviter les incompatibilites de driver.

4. **Le pattern "data migration" separe du "schema migration"** — Ne jamais mixer ALTER TABLE
   et UPDATE de donnees dans la meme revision. Creer une revision schema (ajout colonne),
   puis une revision data (migration des valeurs), puis une revision schema (suppression
   ancienne colonne). Ca permet des rollbacks propres et des deployments blue-green.

5. **Les conventions de nommage des revisions evitent le chaos** — Utiliser le format
   `YYYYMMDD_HHMM_description_courte` pour les revision IDs. Alembic genere des hash par
   defaut, mais des noms lisibles simplifient enormement le debugging en production et les
   reviews de PR.

## Comment ca s'applique a OdooAI

- **Configuration env.py async pour notre stack** — Notre stack utilise SQLAlchemy async
  avec asyncpg (prod) et aiosqlite (dev). Le `env.py` doit detecter l'environnement et
  utiliser le bon driver async. Un seul `env.py` avec un switch sur `config.DATABASE_URL`
  couvre les deux cas.

- **Migrations pour les tables critiques** — Les tables `connections` (credentials chiffrees),
  `conversations`, et `messages` sont les premieres a migrer. Chaque evolution du schema de
  chiffrement AES-256-GCM (colonne `encrypted_password`) necessite une data migration
  dediee pour re-chiffrer les donnees existantes.

- **Zero-downtime migrations obligatoires** — En SaaS, les migrations ne doivent jamais
  bloquer le service. Le pattern expand-contract (ajouter d'abord, migrer, puis supprimer)
  est impose pour toute modification de colonne existante.

## Ce que je recommande

1. **Sprint 6 : setup Alembic async dans le projet** — Creer `alembic/` avec `env.py` async,
   `alembic.ini` configure, et une premiere revision `initial_schema`. Tester le cycle
   complet upgrade/downgrade sur SQLite et PostgreSQL.

2. **Sprint 7 : CI gate sur les migrations** — Ajouter un step CI qui execute
   `alembic upgrade head` puis `alembic downgrade base` sur une DB temporaire. Tout
   echec bloque le merge. Ca garantit la reversibilite.

3. **Sprint 8 : documenter le runbook de migration prod** — Procedure step-by-step pour
   deployer une migration en production : backup, dry-run, apply, verify, rollback plan.

## Sources

- Alembic Documentation — "Running with Asyncio" (official, 2025)
- Miguel Grinberg — "Database Migrations with Alembic" (blog series, 2024)
- SQLAlchemy Documentation — "Async Engine and Session" patterns (2025)
