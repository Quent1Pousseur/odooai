# ODAI-CORE-006 — Connexions Odoo persistantes

## Status
IN PROGRESS

## Auteur
Backend Architect (08) + Security Architect (07)

## Date
2026-03-22

## Contexte
Les credentials Odoo sont en memoire React — perdus a chaque refresh.
L'utilisateur doit re-saisir URL, DB, login, API key a chaque fois.

## Objectif
Stocker les connexions Odoo en DB (chiffrees AES-256-GCM).
Un utilisateur peut avoir plusieurs connexions (multi-instance).

## Schema DB

```sql
CREATE TABLE odoo_connections (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL REFERENCES users(id),
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    db_name TEXT NOT NULL,
    login TEXT NOT NULL,
    api_key_encrypted TEXT NOT NULL,
    odoo_version TEXT DEFAULT '',
    is_default BOOLEAN DEFAULT 0,
    last_connected_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API

### POST /api/connections
Creer une connexion (test + sauvegarde).

### GET /api/connections
Lister les connexions de l'utilisateur (sans les API keys).

### DELETE /api/connections/{id}
Supprimer une connexion.

### POST /api/connections/{id}/test
Tester si la connexion fonctionne.

## Securite
- API key chiffree AES-256-GCM avant stockage
- Cle de chiffrement dans .env (ODOO_CRYPTO_KEY)
- API key jamais retournee dans les GET (masquee)
- Seul le proprietaire peut voir/supprimer ses connexions

## Frontend
- Page de gestion des connexions (ou modal ameliore)
- Liste des connexions sauvegardees
- Bouton "Connecter" qui utilise une connexion sauvegardee
- Plus besoin de re-saisir a chaque fois

## Definition of Done
- [ ] Table odoo_connections creee
- [ ] CRUD API (create, list, delete, test)
- [ ] API key chiffree AES-256-GCM
- [ ] Frontend : liste + connecter + supprimer
- [ ] Tests
- [ ] make check passe
