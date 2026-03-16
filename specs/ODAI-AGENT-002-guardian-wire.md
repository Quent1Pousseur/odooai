# ODAI-AGENT-002 — Wire Guardian dans l'Orchestrator

## Status
IN PROGRESS

## Auteur
Backend Architect (08)

## Reviewers
Security Architect (07), CTO (02)

## Date
2026-03-17

## Contexte
Le Security Guardian (SEC-001) est implemente mais n'est appele nulle part dans le code de production. L'Orchestrator (AGENT-001) route les questions vers le BA Agent sans passer par le Guardian. Les donnees pourraient atteindre le LLM sans anonymisation.

Sprint 2 ajoute la connexion live Odoo — le Guardian DOIT etre wire AVANT.

## Objectif
Integrer le Security Guardian dans le pipeline de l'Orchestrator :
1. `guard_model_access()` avant toute operation Odoo
2. `guard_method()` avant les appels execute/write
3. `validate_domain()` avant les search_read
4. `sanitize_response()` apres chaque lecture de donnees Odoo

## Definition of Done
- [ ] Guardian appele dans l'Orchestrator pour chaque operation
- [ ] guard_model_access → BlockedModelError si BLOCKED
- [ ] guard_method → BlockedMethodError si unlink/sudo
- [ ] validate_domain → DomainInjectionError si malicieux
- [ ] sanitize_response → SanitizedResponse apres lecture
- [ ] Tests couvrant chaque point d'integration
- [ ] Review dans reviews/ODAI-AGENT-002-review.md
- [ ] make check passe

## Design

### Pipeline avec Guardian

```
User question
  → Orchestrator.handle_question()
    → detect_domain() → domain_id
    → load_ba_profile() → BAProfile
    → ask_ba_agent(question, profile) → LLM → reponse

Si connexion Odoo live (future CORE-004) :
  → guard_model_access(model) → OK ou BlockedModelError
  → guard_method(method) → OK ou BlockedMethodError
  → validate_domain(domain) → OK ou DomainInjectionError
  → OdooClient.search_read(...)
  → sanitize_response(model, category, records) → SanitizedResponse
  → donnees sanitisees injectees dans le prompt BA Agent
```

### Sprint 2 : Guardian gate sur l'Orchestrator
Pour Sprint 2, on ajoute une fonction `guarded_odoo_call()` dans l'Orchestrator qui encapsule le pipeline complet : guard → call → sanitize.

L'Orchestrator actuel (BA-only, pas de connexion live) n'appelle pas Odoo directement. Le wire complet se fera dans CORE-004. Mais on prepare l'integration en :
1. Ajoutant `guarded_odoo_call()` dans l'Orchestrator
2. Ajoutant les tests qui verifient que le Guardian est appele
3. Modifiant le BA Agent pour pouvoir recevoir des donnees Odoo sanitisees en plus du BA Profile

## Fichiers impactes
| Fichier | Action |
|---------|--------|
| `odooai/agents/orchestrator.py` | Modifier — ajouter guarded_odoo_call |
| `odooai/agents/ba_agent.py` | Modifier — accepter odoo_context optionnel |
| `tests/agents/test_orchestrator.py` | Creer |
| `reviews/ODAI-AGENT-002-review.md` | Creer apres review |

## Securite
C'est LA spec de wire securite. Review Security Architect (07) obligatoire.

## Dependances
- ODAI-SEC-001 (DONE) — Security Guardian
- ODAI-AGENT-001 (DONE) — Orchestrator

## Estimation
S (< 1 jour)
