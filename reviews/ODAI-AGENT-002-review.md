# Review — ODAI-AGENT-002 (Guardian Wire dans Orchestrator)

## Reviewer : Security Architect (07)
## Date : 2026-03-17
## Status : APPROVED — Aucune issue critique

---

## Verdict
**Go.** Le Guardian est correctement wire. Aucun vecteur de bypass identifie.

## Points verifies

### Guardian appele pour TOUTES les operations
- `guarded_odoo_read()` : guard_model_access → sanitize_response ✅
- `guarded_odoo_write_check()` : guard_model_access → guard_method → validate_domain ✅
- Aucun appel direct a OdooClient sans passer par le Guardian ✅

### Modeles bloques
- ir.rule, res.users, res.groups, ir.config_parameter, ir.cron, ir.mail_server ✅
- BLOCKED non-overridable (frozenset + load_overrides skip) ✅

### Methodes bloquees
- unlink, sudo, _sudo ✅

### Donnees sanitisees
- Hidden fields supprimes (15 exacts + 3 patterns) ✅
- SENSITIVE : montants arrondis, emails masques, noms masques ✅
- M2O names masques sur SENSITIVE ✅
- Jamais de donnees raw vers le LLM ✅

### Domain validation
- Structure, operateurs, champs prives, patterns SQL ✅

### Tests
- 19 tests couvrant tous les gates de securite ✅
- Blocked models, methods, domains, sanitization, field filtering ✅

## Recommandations (LOW)
1. Ajouter un test d'integration handle_question → Guardian → audit log
2. Documenter la garantie Guardian dans un docstring
3. Considerer le rate limiting pour Sprint 3

## Bypass vectors analyses — AUCUN TROUVE
- Direct OdooClient : pas expose aux agents
- LLM tool injection : pas de tools, BA Agent read-only
- Domain injection : validate_domain bloque
- Hidden field disclosure : double blocklist (exact + pattern)
