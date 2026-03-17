# Re-Audit Securite Sprint 5
## Security Auditor (14)
## Date : 2026-03-21

---

## Findings Sprint 4 — Status

| Finding | Severite | Fix | Status |
|---------|----------|-----|--------|
| F1 Rate limiting absent | HIGH | slowapi 10/min (#50) | **RESOLU** ✅ |
| F2 HTTP clair | HIGH | HTTPS prevu (#63) | EN COURS |
| F3 CORS permissif | MEDIUM | CORS restrictif (#65) | **RESOLU** ✅ |

## Nouveaux tests Sprint 5

### T1 — Rate limiting fonctionne
- Envoye 15 requetes en 60 secondes → les 5 dernieres retournent 429
- **Resultat : PASS** ✅

### T2 — CORS bloque les origines non-autorisees
- Requete depuis http://evil.com → bloquee
- Requete depuis http://localhost:3000 → autorisee
- **Resultat : PASS** ✅

### T3 — Sentry capture les erreurs
- SENTRY_DSN configure → sentry_sdk.init() appele
- Pas de DSN → skip silencieux (pas de crash)
- **Resultat : PASS** ✅

### T4 — Telemetry /metrics
- GET /metrics retourne les compteurs
- Pas d'information sensible dans les metriques
- **Resultat : PASS** ✅

## Findings restants

### F2 — HTTPS (toujours ouvert)
- Bloquant pour staging
- Fix : nginx reverse proxy + Let's Encrypt (#63)
- **Action : Sprint 5 semaine 2**

### F5 — Pas d'auth utilisateur (nouveau)
- N'importe qui peut utiliser /api/chat
- Bloquant pour staging public
- Fix : JWT auth (#49)
- **Action : Sprint 5 semaine 1**

## Verdict

**Dev : SAFE** (2/3 findings resolus)
**Staging : 2 fixes restants** (HTTPS + auth JWT)
