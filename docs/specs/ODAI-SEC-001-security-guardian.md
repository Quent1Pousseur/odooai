# ODAI-SEC-001 — Security Guardian Pipeline

## Status
IN PROGRESS

## Auteur
Security Architect (07) + Backend Architect (08)

## Reviewers
CTO (02), QA Lead (13)

## Date
2026-03-16

## Contexte
Le Security Guardian est le composant le plus critique d'OdooAI. Il intercepte TOUTES les donnees Odoo avant qu'elles n'atteignent le LLM. ZERO LLM — logique pure deterministe.

## Objectif
Transformer le stub en pipeline complet :
1. Classification modele (BLOCKED → rejet)
2. Classification methode (unlink/sudo → rejet)
3. Validation domain (anti-injection)
4. Filtrage champs + anonymisation (SENSITIVE → mask)
5. Audit logging

## Definition of Done
- [ ] Pipeline guardian complet (classify → method → domain → filter → anonymize → audit)
- [ ] Blocked methods : unlink, sudo, _sudo
- [ ] Domain validator anti-injection
- [ ] Anonymisation automatique par categorie (SENSITIVE)
- [ ] Audit logging avec structlog
- [ ] Tests couvrant chaque etape du pipeline
- [ ] make check passe
- [ ] Review par CTO (02) et QA Lead (13)

## Securite
C'est LA spec securite. Review Security Architect (07) obligatoire.
ZERO tolerance pour les failles : pas de donnees sensibles non-anonymisees vers le LLM.

## Estimation
M (1-3 jours)

## Dependances
- ODAI-CORE-001 (DONE) — ModelCategory, anonymizer
- ODAI-CORE-003 (DONE) — structlog
