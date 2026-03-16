# Audit Securite Sprint 4 — Rapport Final
## Security Auditor (14) + Security Architect (07) + DevSecOps (24)
## Date : 2026-03-21
## Status : 3 findings, 0 critique pour dev, 3 bloquants staging

---

## Scope
- Backend API (FastAPI)
- Security Guardian (anonymisation, classification, domain validation)
- Connexion Odoo (credentials, transport)
- Frontend (CORS, input sanitization)

## Findings

### F1 — Rate Limiting absent (CRITIQUE pour staging)
- **Endpoint** : POST /api/chat
- **Risque** : spam LLM → couts illimites, bruteforce credentials Odoo
- **Severite** : HIGH (staging), LOW (dev)
- **Fix** : slowapi, 10 req/min/IP — 30 lignes (Sprint 5)
- **Status** : Documente, fix prevu

### F2 — Credentials en HTTP clair (CRITIQUE pour staging)
- **Transport** : body JSON en POST sans HTTPS
- **Risque** : interception des credentials Odoo en transit (MITM)
- **Severite** : HIGH (staging), N/A (localhost)
- **Fix** : HTTPS obligatoire via nginx/Cloudflare (Sprint 5)
- **Status** : Documente, fix prevu

### F3 — CORS trop permissif
- **Config** : `allow_origins=["*"]` en dev
- **Risque** : n'importe quel site peut appeler notre API
- **Severite** : MEDIUM (staging)
- **Fix** : restreindre aux domaines autorises en prod
- **Status** : Documente, fix prevu

## Points positifs

| Element | Evaluation |
|---------|-----------|
| Security Guardian (classification) | ✅ Solide — BLOCKED/SENSITIVE/STANDARD/OPEN |
| Domain validator (anti-injection) | ✅ 36 tests, edge cases couverts |
| Anonymisation HR/salaires | ✅ Fonctionne correctement |
| Credentials non stockes (session only) | ✅ Bonne pratique |
| AES-256-GCM encryption | ✅ Implementation correcte |
| Red teaming (3 failles → 3 fixes) | ✅ Cycle complet |
| Modeles BLOCKED (ir.rule, ir.config) | ✅ Correctement bloques |
| `ast.literal_eval` (pas `eval`) | ✅ Securise |

## Verdict

**Dev/localhost : SAFE.** Aucun risque pour le fondateur en local.
**Staging : 3 fixes requis** (rate limiting, HTTPS, CORS) avant deploiement.
**Beta publique : OK** apres les fixes staging + auth utilisateur.

## Checklist pre-staging

- [ ] Rate limiting (slowapi) — F1
- [ ] HTTPS (nginx/Cloudflare) — F2
- [ ] CORS restrictif — F3
- [ ] Auth utilisateur (JWT) — a implementer
- [ ] Re-audit apres fixes

---

> "La securite en dev est acceptable. La securite en staging est non-negociable." — Security Auditor (14)
