# Learning — CTO (02) — Advanced Async Patterns pour Python
## Date : 2026-03-21
## Duree : 3 heures

## Ce que j'ai appris

1. **asyncio.gather vs TaskGroup** — Python 3.11+ introduit `asyncio.TaskGroup` qui est
   superieur a `asyncio.gather` pour la gestion d'erreurs : si une task echoue, toutes
   les autres sont annulees proprement. Avec `gather(return_exceptions=True)`, les erreurs
   sont silencieusement melangees aux resultats, ce qui est dangereux en production.

2. **Semaphores pour le rate limiting LLM** — `asyncio.Semaphore(n)` est le pattern
   standard pour limiter les appels concurrents a l'API Claude. Avec Haiku a 100 RPM
   et Sonnet a 50 RPM, utiliser un semaphore par tier de modele evite les 429.
   Pattern : `async with semaphore: await llm_call()`.

3. **Connection pooling async avec SQLAlchemy** — `create_async_engine(pool_size=5,
   max_overflow=10, pool_recycle=3600)` est le sweet spot pour un SaaS early stage.
   Le `pool_pre_ping=True` evite les connexions mortes apres un restart PostgreSQL.

4. **Le pattern "fan-out/fan-in" pour l'analyse multi-modules** — Quand on analyse
   les 1218 modules Odoo, lancer N workers avec un `asyncio.Queue` est plus efficace
   que `gather` sur 1218 coroutines. La queue permet le backpressure naturel.

5. **Structured concurrency et contextvars** — `contextvars.ContextVar` permet de
   propager le request_id a travers les tasks async sans le passer en parametre.
   Essentiel pour le logging structure dans FastAPI + nos appels LLM.

## Comment ca s'applique a OdooAI

1. **Refactor du LLM provider** : Notre `anthropic_provider.py` doit utiliser un
   `asyncio.Semaphore` par modele (Haiku=20, Sonnet=10, Opus=3) pour eviter les
   rate limits. Actuellement aucun mecanisme de throttling n'est en place.

2. **Analyse parallele des modules** : Quand un utilisateur demande un audit complet,
   on peut analyser les modules en parallele avec un TaskGroup + Queue(maxsize=20).
   Gain estime : 5-10x sur le temps de reponse pour les requetes complexes.

3. **Request tracing end-to-end** : Utiliser `contextvars` pour propager le `request_id`
   du middleware FastAPI jusqu'aux appels Claude, permettant de tracer une requete
   utilisateur a travers tous les services async.

## Ce que je recommande

1. **Sprint 7** : Ajouter `asyncio.Semaphore` dans `ILLMProvider` avec des limites
   configurables par modele dans `config.py`. Ecrire un test qui verifie que N+1
   appels concurrents respectent le semaphore. Fichier : `odooai/infrastructure/llm/`.

2. **Sprint 8** : Implementer le pattern fan-out/fan-in dans un nouveau service
   `odooai/services/parallel_analyzer.py` pour l'analyse multi-modules.
   Target : analyser 100 modules en < 30 secondes avec Haiku.

3. **Sprint 7** : Remplacer tout usage de `asyncio.gather` par `asyncio.TaskGroup`
   dans le codebase. Ajouter une regle ruff custom pour interdire `gather`.

## Sources

1. Python docs — "Asynchronous I/O" — TaskGroup et Semaphore (docs.python.org/3.11)
2. "Python Concurrency with asyncio" — Matthew Fowler (Manning, 2022) — Chapitres 8-10
3. Anthropic API docs — Rate limits par tier et best practices pour le batching
