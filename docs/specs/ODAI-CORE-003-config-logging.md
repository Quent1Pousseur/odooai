# ODAI-CORE-003 — Config Validation & Structured Logging

## Status
DONE

## Auteur
Backend Architect (08)

## Reviewers
Senior Backend Dev (19), Infra Engineer (12)

## Date
2026-03-16

## Contexte
Retro Sprint 0 a identifie 2 problemes :
1. Config avec valeurs vides par defaut → erreurs silencieuses en production
2. Pas de logging structure configure → logs difficilement exploitables

## Objectif
1. Ajouter `validate_production()` fail-fast sur Settings
2. Configurer structlog (JSON en prod, console coloree en dev)
3. Integrer dans le lifespan de l'app

## Definition of Done
- [x] `Settings.validate_production()` raise `ConfigurationError` si secrets manquent
- [x] `Settings.is_production` / `is_development` properties
- [x] `odooai/logging.py` configure structlog (JSON prod / console dev)
- [x] Lifespan appelle validation + setup logging
- [x] Tests pour validation config (6 cas)
- [x] make check passe

## Fichiers Impactes
| Fichier | Action | Description |
|---------|--------|-------------|
| `odooai/config.py` | modifier | Ajout validate_production + properties |
| `odooai/logging.py` | creer | Setup structlog |
| `odooai/main.py` | modifier | Integrer logging + validation |
| `tests/test_config.py` | creer | Tests validation |

## Dependances
- ODAI-CORE-001 (DONE)

## Estimation
S (< 1 jour)
