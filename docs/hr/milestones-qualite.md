# Milestones de Qualite — Criteres de Deploiement
## Redige par : QA Lead (13) + Security Architect (07)
## Approuve par : CTO (02), CEO (01)
## Date : 2026-03-19

---

## Principe

**RIEN ne se deploie sans que TOUS les criteres soient verts.**

Ce document resout la tension vitesse vs qualite : les features avancent au rythme du fondateur, mais le deploiement ne se fait qu'avec le feu vert qualite/securite.

---

## Milestone 1 — Demo-Ready (cible : 24 mars)

Le produit peut etre montre a un integrateur/PME en appel video (localhost du fondateur).

| # | Critere | Responsable | Status |
|---|---------|-------------|--------|
| 1 | 5 questions types repondues correctement a 100% | Prompt Eng (25) | ⬜ |
| 2 | Chat web fonctionnel avec streaming | Frontend Eng (21) | ✅ |
| 3 | Connexion Odoo via formulaire web | Frontend Eng (21) | ✅ |
| 4 | Landing page professionnelle | Brand Designer (42) | ✅ |
| 5 | Zero crash sur un parcours de 10 questions | QA Lead (13) | ⬜ |
| 6 | Reponses en < 15 secondes | SRE (23) | ⬜ |

### Bloquants VETO
- Security Arch : aucun (demo en localhost, pas expose)
- QA Lead : critere 5 doit etre vert

---

## Milestone 2 — Staging-Ready (cible : Sprint 5)

Le produit peut tourner sur un VPS de staging accessible par l'equipe.

| # | Critere | Responsable | Status |
|---|---------|-------------|--------|
| 1 | Docker compose fonctionnel (backend + frontend + db) | DevOps (22) | ⬜ |
| 2 | HTTPS obligatoire | DevSecOps (24) | ⬜ |
| 3 | Auth utilisateur basique (email + password) | Backend Arch (08) | ⬜ |
| 4 | PostgreSQL (plus SQLite) | DBA (30) | ⬜ |
| 5 | Structured logging centralise | Observability (38) | ⬜ |
| 6 | Tests d'integration (10 minimum) | QA Lead (13) | ⬜ |
| 7 | Audit securite complet | Security Auditor (14) | ⬜ |
| 8 | Rate limiting sur les endpoints API | Security Arch (07) | ⬜ |
| 9 | Credentials Odoo chiffres en transit + at rest | Security Arch (07) | ⬜ |

### Bloquants VETO
- Security Arch : criteres 2, 8, 9
- Security Auditor : critere 7
- QA Lead : critere 6
- DevSecOps : critere 2

---

## Milestone 3 — Beta-Ready (cible : Sprint 7)

Le produit peut accueillir 5-10 PME en beta privee.

| # | Critere | Responsable | Status |
|---|---------|-------------|--------|
| 1 | Multi-tenant (isolation des donnees par user) | Backend Arch (08) | ⬜ |
| 2 | Stripe integration (paiement) | Integration Eng (35) | ⬜ |
| 3 | Onboarding guide (in-app) | Customer Success (17) | ⬜ |
| 4 | Knowledge base + FAQ | Support Eng (41) | ⬜ |
| 5 | Monitoring + alerting | SRE (23) + Observability (38) | ⬜ |
| 6 | GDPR compliance (privacy policy, data deletion) | Legal (16) | ⬜ |
| 7 | EU AI Act transparency document | AI Safety (33) | ⬜ |
| 8 | Eval framework (50+ questions benchmarkees) | Data Scientist (28) | ⬜ |
| 9 | Zero faille critique ouverte | Security Auditor (14) | ⬜ |
| 10 | Backup + disaster recovery | Chaos Eng (31) | ⬜ |

### Bloquants VETO
- Legal : criteres 6, 7
- Security Auditor : critere 9
- QA Lead : critere 8

---

## Process

1. Le PM track l'avancement de chaque milestone dans GitHub Projects
2. Chaque agent responsable met a jour son critere quand il est vert
3. Le CTO valide les milestones 1 et 2
4. Le CEO valide le milestone 3
5. Un VETO sur un critere bloquant = deploiement impossible
6. Le fondateur peut overrider un VETO (mais c'est documente et assume)

---

> "La qualite n'est pas un frein — c'est le carburant de la confiance." — QA Lead
