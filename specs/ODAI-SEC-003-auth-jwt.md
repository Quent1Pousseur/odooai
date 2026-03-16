# ODAI-SEC-003 — Auth JWT (signup, login, middleware)

## Status
IN PROGRESS

## Auteur
Backend Architect (08) + Senior Backend Dev (19)

## Reviewers
Security Architect (07), CTO (02)

## Date
2026-03-21

## Contexte
Actuellement, n'importe qui peut utiliser /api/chat sans authentification.
Pour le staging et la beta, il faut un minimum d'auth.

## Approche
JWT simple. Pas d'OAuth server. Email + password + token.

## Endpoints

### POST /api/auth/signup
```json
Request: { "email": "user@example.com", "password": "min8chars" }
Response: { "token": "eyJ...", "user_id": "uuid" }
```

### POST /api/auth/login
```json
Request: { "email": "user@example.com", "password": "min8chars" }
Response: { "token": "eyJ...", "user_id": "uuid" }
```

### Middleware
- Header: `Authorization: Bearer <token>`
- Endpoints proteges : /api/chat, /api/conversations
- Endpoints publics : /health, /metrics, /api/auth/*, /api/waitlist

## Schema DB
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    plan VARCHAR(50) DEFAULT 'starter',
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT now()
);
```

## Securite
- Passwords hashes avec bcrypt (12 rounds)
- JWT expire apres 24h (configurable)
- Secret key dans .env (SECRET_KEY)
- Rate limiting sur signup/login (5/minute)

## Fichiers

| Fichier | Action |
|---------|--------|
| odooai/api/routers/auth.py | Creer — signup, login |
| odooai/api/middleware.py | Modifier — JWT middleware |
| odooai/infrastructure/db/models.py | Modifier — User model |
| odooai/infrastructure/db/database.py | Modifier — create User table |
| tests/api/test_auth.py | Creer |

## Estimation
M (1-2 jours)

## Definition of Done
- [ ] Signup + login fonctionnels
- [ ] JWT middleware protege /api/chat
- [ ] Passwords bcrypt
- [ ] Tests
- [ ] make check passe
