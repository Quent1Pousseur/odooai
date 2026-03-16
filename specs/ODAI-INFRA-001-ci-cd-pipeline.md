# ODAI-INFRA-001 — Pipeline CI/CD GitHub Actions

## Status
DONE

## Auteur
DevOps Engineer (22)

## Reviewers
CTO (02), Infra Engineer (12)

## Date
2026-03-16

## Contexte
Jusqu'ici, `make check` est execute manuellement. Sans CI/CD, du code non-conforme pourrait etre merge. Point negatif identifie dans la retro Sprint 0.

## Objectif
Automatiser les controles qualite sur chaque push et PR via GitHub Actions :
1. Lint (ruff check + format)
2. Type check (mypy --strict)
3. Tests (pytest, multi-Python)
4. Security scan (bandit)
5. Commit message format (`[ODAI-XXX] type: description`)
6. File length check (max 300 lignes)

## Definition of Done
- [x] Workflow `.github/workflows/ci.yml` cree
- [x] 6 jobs paralleles : lint, typecheck, test, security, commit-format, file-length
- [x] Tests sur Python 3.11, 3.12, 3.13
- [x] Coverage minimum 70% (sur 3.11)
- [x] Concurrency : annule les runs precedents sur le meme branch
- [x] Commit format verifie sur les PRs uniquement
- [x] Review par CTO (02)

## Design

### Jobs
| Job | Trigger | Bloquant |
|-----|---------|----------|
| lint | push + PR | Oui |
| typecheck | push + PR | Oui |
| test | push + PR | Oui (3 versions Python) |
| security | push + PR | Oui (medium+ severity) |
| commit-format | PR only | Oui |
| file-length | push + PR | Oui (max 300 lignes) |

### Securite
Pas d'impact securite. Le workflow n'a pas acces aux secrets.

## Fichiers Impactes
| Fichier | Action | Description |
|---------|--------|-------------|
| `.github/workflows/ci.yml` | creer | Pipeline CI complete |

## Tests
Le workflow se teste lui-meme a chaque push.

## Dependances
Aucune.

## Estimation
S (< 1 jour)

## Risques
- Temps d'execution si les deps sont lourdes → pip cache a considerer plus tard
