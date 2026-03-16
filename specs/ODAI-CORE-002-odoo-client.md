# ODAI-CORE-002 — OdooClient XML-RPC + JSON-RPC

## Status
IN PROGRESS

## Auteur
Backend Architect (08)

## Reviewers
CTO (02), Odoo Expert (10), Security Architect (07)

## Date
2026-03-16

## Contexte
OdooAI doit se connecter aux instances Odoo des clients via deux protocoles :
- **XML-RPC** : Odoo 17.0, 18.0 (protocole historique, synchrone)
- **JSON-2** : Odoo 19.0+ (protocole moderne, HTTP natif, Bearer token)

Le stub dans `infrastructure/odoo/client.py` doit etre remplace par une implementation reelle.

## Objectif
Implementer un client Odoo async, dual-protocole, avec :
1. Detection auto de la version serveur
2. Authentification avec detection admin/interne/portal (rejet portal)
3. 8 operations CRUD : search_read, search_count, create, write, execute, get_model_fields, check_access_rights
4. Retry avec backoff sur erreurs transitoires
5. Error mapping vers exceptions domaine
6. Split en 6 fichiers (max 300 lignes chacun)

## Definition of Done
- [ ] Dual-protocole XML-RPC + JSON-2 fonctionnel
- [ ] Authentification detecte admin/interne et rejette portal
- [ ] 8 operations implementees
- [ ] Retry avec backoff exponentiel (2 retries)
- [ ] Error mapping complet (auth, validation, record not found, connection)
- [ ] Aucun fichier > 300 lignes
- [ ] Tests unitaires avec mocks
- [ ] make check passe (ruff + mypy + tests + bandit)
- [ ] Review par CTO (02) et Odoo Expert (10)

## Design

### Signature simplifiee
url/db stockes dans le constructeur (1 client = 1 instance Odoo) :
```python
client = OdooClient(base_url="https://myco.odoo.com", db="mydb", api_type=OdooApiType.JSON2)
info = await client.authenticate(login="user@co.com", api_key="key123")
records = await client.search_read(api_key="key123", model="sale.order", ...)
```

### Auth flow
```
authenticate(login, api_key)
  → JSON-2: context_get → read user → has_group (parallel)
  → XML-RPC: common.authenticate → users.read → has_group (parallel)
  → Detect: is_system (group_system), is_internal (group_user / share=False)
  → REJECT if portal (not is_internal) → OdooAuthError
  → Return OdooUserInfo + server_version
```

### Securite
- Rejet des utilisateurs portal (share=True, pas group_user)
- API keys jamais loggees (ni en debug, ni en error)
- Timeout 30s par defaut
- Review Security Architect (07) requise

## Fichiers Impactes
| Fichier | Action | Description |
|---------|--------|-------------|
| `odooai/domain/entities/connection.py` | modifier | OdooApiType: JSON2 + XML_RPC |
| `odooai/domain/ports/i_odoo_client.py` | modifier | Nouvelle signature (url/db dans constructeur) |
| `odooai/infrastructure/odoo/__init__.py` | modifier | Exports |
| `odooai/infrastructure/odoo/_http.py` | creer | httpx pool + lifecycle |
| `odooai/infrastructure/odoo/_errors.py` | creer | Error mapping |
| `odooai/infrastructure/odoo/_xmlrpc.py` | creer | XML-RPC helpers |
| `odooai/infrastructure/odoo/_json2.py` | creer | JSON-2 helpers |
| `odooai/infrastructure/odoo/client.py` | recrire | Facade dual-protocole |
| `odooai/main.py` | modifier | Adapter wiring |
| `tests/infrastructure/test_odoo_client.py` | creer | Tests avec mocks |

## Tests
- Test authenticate → OdooUserInfo avec is_system/is_internal
- Test authenticate portal → OdooAuthError
- Test search_read routes vers JSON-2 ou XML-RPC
- Test error mapping (auth error, validation, not found, connection)
- Test retry sur erreur transitoire
- Test version detection

## Dependances
- ODAI-CORE-001 : Architecture hexagonale (DONE)

## Estimation
M (1-3 jours)

## Risques
- Pas d'instance Odoo de test disponible → tests avec mocks uniquement
- JSON-2 endpoint non documente officiellement par Odoo → base sur prodooctivity battle-tested

## Alternatives Rejetees
- **Monolithique** (comme prodooctivity) : 1553 lignes dans un seul fichier, viole la regle des 300 lignes
- **url/db dans chaque appel** (signature actuelle du stub) : repetitif, le client est lie a une instance
