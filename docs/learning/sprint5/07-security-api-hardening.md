# Learning — Security Architect (07) — API Security Hardening Patterns

## Date : 2026-03-22 (Sprint 5, session 3)
## Duree : 3 heures

## Ce que j'ai appris

1. **Rate limiting multi-couche est indispensable** : Un seul rate limiter global ne suffit pas. Il faut trois niveaux : global (requetes/sec sur l'infra), par tenant (quota mensuel), et par endpoint (les routes LLM sont plus couteuses que /health). FastAPI avec slowapi ou un middleware custom permet cette granularite.

2. **Request validation stricte via Pydantic v2** : Chaque payload entrant doit etre valide par un schema Pydantic strict (pas de champs extra, types enforces, longueurs bornees). Cela bloque les injections de masse et les payloads malformes avant qu'ils n'atteignent la logique metier.

3. **CORS et CSP doivent etre restrictifs en production** : Le frontend Next.js est sur un domaine specifique. Le backend FastAPI ne doit accepter que ce domaine en CORS origin. Content-Security-Policy empeche le chargement de scripts tiers injectes.

4. **API key rotation et expiration** : Les cles API doivent avoir une date d'expiration (90 jours max) et supporter la rotation sans downtime. Le pattern "dual key" (primary + secondary) permet de migrer sans interruption de service.

5. **Input sanitization contre le prompt injection** : Comme OdooAI envoie des donnees utilisateur aux LLM, il faut un layer de sanitization qui detecte et neutralise les tentatives de prompt injection (instructions cachees dans les noms de champs Odoo, valeurs de records).

## Comment ca s'applique a OdooAI

1. **Security Guardian renforce** : Le module `security/guardian.py` (zero LLM) doit inclure un `InputSanitizer` qui filtre les payloads avant tout appel agent. Les patterns de prompt injection connus sont detectes par regex et scoring, sans appel LLM.

2. **Middleware hardening dans FastAPI** : Le `api/middleware.py` actuel (RequestID) doit etre etendu avec rate limiting par tenant, validation de headers (Content-Type strict, pas de headers inattendus), et logging de securite vers `security/audit.py`.

3. **Protection des credentials Odoo** : Les connexions Odoo stockees (AES-256-GCM via `infrastructure/crypto.py`) ne doivent jamais transiter en clair dans les logs. Le middleware doit scrub les champs sensibles de toute reponse d'erreur.

## Ce que je recommande

1. **Sprint 6** : Ajouter un middleware rate limiting tri-couche dans `api/middleware.py` avec Redis comme backend de comptage (reutiliser `infrastructure/cache/redis_client.py`).

2. **Sprint 6** : Implementer un `PromptInjectionDetector` dans `security/guardian.py` avec une liste de patterns connus et un score de risque. Bloquer au-dessus du seuil configurable.

3. **Sprint 7** : Mettre en place une rotation automatique des API keys avec notification 7 jours avant expiration, et audit log de chaque rotation dans `security/audit.py`.

## Sources

1. OWASP API Security Top 10 (2023 Edition)
2. Simon Willison, "Prompt Injection Attacks against GPT-3" — Research Notes (2024)
3. FastAPI Security Documentation — OAuth2, CORS, Dependencies (2025)
