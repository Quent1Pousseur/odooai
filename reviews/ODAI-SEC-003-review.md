# Review — ODAI-SEC-003 Auth JWT
## Reviewer : Security Architect (07)
## Date : 2026-03-21
## Status : APPROVED

## Points positifs
- Bcrypt 12 rounds — standard correct
- JWT avec expiration 24h
- Rate limiting sur signup (5/min) et login (10/min)
- Public paths bien definies
- Dev mode = auth optionnelle, prod = obligatoire
- Passwords jamais logges

## Points d'attention
- Le secret_key par defaut est insecure — OK car valide_production() le bloque
- Pas de refresh token — a ajouter Sprint 6
- Pas de email verification — a ajouter Sprint 7
- Pas de password reset — a ajouter Sprint 7
