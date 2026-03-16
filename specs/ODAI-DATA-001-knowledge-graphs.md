# ODAI-DATA-001 — Knowledge Graph Schema + Code Analyst

## Status
IN PROGRESS

## Auteur
AI Engineer (09) + Data Engineer (11) + Backend Architect (08)

## Reviewers
Odoo Expert (10), CTO (02), Security Architect (07)

## Date
2026-03-16

## Contexte
Les Knowledge Graphs sont le moat d'OdooAI — representations JSON structurees de tout ce qu'un module Odoo peut faire, extraites directement du code source. Sprint 1 couvre les schemas + le Code Analyst (parseur). La BA Factory (LLM) viendra en Sprint 2.

## Objectif
1. Schemas Pydantic validables pour chaque aspect d'un module Odoo
2. Code Analyst : parseur Python AST + XML qui extrait les KG depuis le code source
3. Stockage JSON versionne dans knowledge_store/
4. Best-effort : un module qui crash ne bloque pas les autres

## Exigences Odoo Expert (10) — VETO si non-respectees
1. `_inherits` (delegation) distinct de `_inherit` (extension)
2. `related` fields captures
3. `_inherit` sans `_name` = extension de modele existant, PAS nouveau modele
4. `store=False` par defaut pour les computed fields
5. Vues heritees (`inherit_id`) listees separement des vues principales

## Definition of Done
- [ ] Schemas Pydantic pour : manifest, models, constraints, actions, security, views, menus, index
- [ ] manifest_parser (ast.literal_eval, securise)
- [ ] python_parser (AST : models, fields, computed, depends, constrains, actions, sql_constraints)
- [ ] xml_parser (views, security CSV/XML, menus)
- [ ] analyzer (orchestrateur module complet)
- [ ] storage (lecture/ecriture JSON)
- [ ] Les 5 exigences Odoo Expert respectees
- [ ] Best-effort : erreurs loggees, module saute, pipeline continue
- [ ] Tests avec vrais extraits de modules Odoo (sale, stock)
- [ ] Review interne par Security Arch (07) + Odoo Expert (10)
- [ ] make check passe

## Estimation
L (3-5 jours)

## Dependances
- ODAI-CORE-001 (DONE)
- ODAI-CORE-003 (DONE) — structlog

## Risques
- Edge cases AST Python (heritage multiple, metaclasses, decorateurs custom)
- Mitigation : best-effort + test sur vrais modules
