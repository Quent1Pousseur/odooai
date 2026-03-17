# ODAI-CORE-001 — Hexagonal Architecture & Package Structure

## Status
IN PROGRESS

## Auteur
Backend Architect (08)

## Reviewers
CTO (02), Senior Backend Dev (19)

## Date
2026-03-16

## Contexte
OdooAI demarre Sprint 1. Toutes les specs suivantes (CORE-002 OdooClient, SEC-001 Security Guardian, DATA-001 Knowledge Graphs) dependent d'une structure de code claire avec des interfaces definies. Le scaffold actuel contient des packages vides. Il faut definir la structure definitive, les interfaces, la strategie d'erreurs, et le wiring.

## Objectif
Etablir l'architecture hexagonale (ports & adapters) du package `odooai/` avec :
1. Domain layer : entities, value objects, ports (interfaces abstraites)
2. Services layer : logique applicative
3. Infrastructure layer : implementations concretes (remplace connectors/)
4. Security layer : Guardian, anonymisation, audit
5. API layer : routers, middleware, dependency injection
6. Exception hierarchy avec message technique + user_message LLM-safe

## Definition of Done
- [x] Structure des packages definie et creee
- [x] Domain layer : ModelCategory, OdooUserInfo, SanitizedResponse, OdooConnection
- [x] Ports : IOdooClient, ICache, ILLMProvider, ICrypto
- [x] Services : FieldScorer, ModelClassifier
- [x] Security : Anonymizer (pure logic), Guardian (stub), Audit (stub)
- [x] Infrastructure : Crypto (AES-256-GCM), stubs OdooClient/Cache/DB/LLM
- [x] API : dependencies wiring, middleware, health router
- [x] Exception hierarchy complete
- [x] main.py refactored avec create_app factory + lifespan
- [x] Tests ecrits et passes
- [x] make check passe (lint + types + tests + security)
- [x] Review par CTO (02) et Senior Backend Dev (19)

## Design

### Architecture

```
                    ┌──────────────┐
                    │   API Layer  │  FastAPI routers, middleware
                    └──────┬───────┘
                           │
                    ┌──────▼───────┐
                    │   Services   │  Field scorer, model classifier
                    └──────┬───────┘
                           │
              ┌────────────▼────────────┐
              │      Domain Layer       │  Entities, value objects, ports
              └────────────┬────────────┘
                           │ (ports/interfaces)
           ┌───────────────┼───────────────┐
    ┌──────▼──────┐ ┌──────▼──────┐ ┌──────▼──────┐
    │Infrastructure│ │  Security   │ │     LLM     │
    │  Odoo/Cache │ │  Guardian   │ │  Providers  │
    │  DB/Crypto  │ │  Anonymizer │ │             │
    └─────────────┘ └─────────────┘ └─────────────┘
```

**Regle de dependance** : les couches internes ne dependent jamais des couches externes. Domain est pur. Services depend de domain. Infrastructure implemente les ports de domain.

### Package Structure

```
odooai/
  __init__.py                  exceptions.py
  main.py                      config.py
  domain/
    entities/connection.py
    value_objects/model_category.py, odoo_user_info.py, sanitized_response.py
    ports/i_odoo_client.py, i_cache.py, i_llm_provider.py, i_crypto.py
  services/field_scorer.py, model_classifier.py
  security/guardian.py, anonymizer.py, audit.py
  infrastructure/odoo/client.py, cache/redis_client.py, db/database.py, llm/anthropic_provider.py, crypto.py
  api/dependencies.py, middleware.py, routers/health.py
```

### Securite
- ModelCategory BLOCKED set : ir.rule, ir.model.access, res.users, res.groups, ir.config_parameter, ir.cron, ir.mail_server
- Anonymizer : round amounts, mask emails, mask names
- Crypto : AES-256-GCM pour credentials Odoo
- Security review par Security Architect (07) requise pour SEC-001

## Fichiers Impactes
| Fichier | Action | Description |
|---------|--------|-------------|
| `odooai/exceptions.py` | creer | Hierarchie d'exceptions |
| `odooai/domain/entities/connection.py` | creer | OdooConnection entity |
| `odooai/domain/value_objects/model_category.py` | creer | ModelCategory + classifier |
| `odooai/domain/value_objects/odoo_user_info.py` | creer | Frozen dataclass |
| `odooai/domain/value_objects/sanitized_response.py` | creer | Frozen dataclass |
| `odooai/domain/ports/i_odoo_client.py` | creer | Interface abstraite |
| `odooai/domain/ports/i_cache.py` | creer | Interface abstraite |
| `odooai/domain/ports/i_llm_provider.py` | creer | Interface abstraite |
| `odooai/domain/ports/i_crypto.py` | creer | Interface abstraite |
| `odooai/services/field_scorer.py` | creer | Score + select top fields |
| `odooai/services/model_classifier.py` | creer | Service wrapper |
| `odooai/security/anonymizer.py` | creer | Pure logic anonymisation |
| `odooai/security/guardian.py` | modifier | Stub → classification gate |
| `odooai/security/audit.py` | creer | Stub audit logger |
| `odooai/infrastructure/` | creer | Remplace connectors/ |
| `odooai/infrastructure/crypto.py` | creer | AES-256-GCM |
| `odooai/infrastructure/odoo/client.py` | creer | Stub |
| `odooai/infrastructure/cache/redis_client.py` | creer | Stub |
| `odooai/infrastructure/db/database.py` | creer | Stub |
| `odooai/infrastructure/llm/anthropic_provider.py` | creer | Stub |
| `odooai/api/dependencies.py` | creer | wire() + Depends |
| `odooai/api/middleware.py` | creer | RequestID |
| `odooai/api/routers/health.py` | creer | Extrait de main.py |
| `odooai/main.py` | modifier | create_app + lifespan |
| `odooai/config.py` | modifier | + crypto key, log level |
| `odooai/connectors/` | supprimer | Remplace par infrastructure/ |

## Tests
- `tests/domain/test_model_category.py` — classify BLOCKED/SENSITIVE/STANDARD/OPEN, overrides
- `tests/domain/test_value_objects.py` — frozen immutability, equality
- `tests/services/test_field_scorer.py` — score_field, select_top_fields
- `tests/security/test_anonymizer.py` — mask_email, mask_name, round_amount
- `tests/security/test_guardian.py` — reject BLOCKED, pass OPEN
- `tests/infrastructure/test_crypto.py` — encrypt/decrypt round-trip
- `tests/test_health.py` — GET /health → 200 (existant, adapter)

## Dependances
Aucune — c'est la spec fondation.

## Estimation
L (3-5 jours)

## Risques
- Over-engineering : mitige par des stubs pour OdooClient/LLM/DB
- Renommage connectors/ : aucun code existant ne l'importe

## Alternatives Rejetees
- **DI framework (dependency-injector)** : trop de magie, FastAPI Depends() suffit
- **Protocol au lieu de ABC** : ABC donne des messages d'erreur plus clairs quand une methode manque
- **application/services/ + application/use_cases/** : trop de nesting pour Phase 1, un seul services/ suffit
