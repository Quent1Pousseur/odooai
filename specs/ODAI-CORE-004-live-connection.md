# ODAI-CORE-004 — Connexion Live Odoo dans le Chat CLI

## Status
IN PROGRESS

## Auteur
Backend Architect (08)

## Reviewers
Security Architect (07), Odoo Expert (10), CTO (02)

## Date
2026-03-17

## Contexte
Le chat CLI (AGENT-001) repond uniquement avec les BA Profiles (intelligence statique). Pour le aha moment reel, il faut que l'IA puisse interroger l'instance Odoo du client et personnaliser ses reponses.

Le OdooClient (CORE-002) et le Guardian (SEC-001 + AGENT-002) sont prets. Il manque l'integration dans le chat.

## Objectif
1. `odooai chat --url URL --db DB` demande login + API key au demarrage
2. L'Orchestrator detecte les modules installes via OdooClient
3. Les questions peuvent combiner BA Profile + donnees live
4. Le Guardian anonymise les donnees live avant le LLM

## Definition of Done
- [ ] CLI chat accepte `--url` et `--db` (optionnels — sans = mode BA-only)
- [ ] Au demarrage : authentification Odoo (detecte admin/interne, rejette portal)
- [ ] Detection des modules installes (ir.module.module search_read)
- [ ] L'Orchestrator peut faire un search_read guarde sur l'instance
- [ ] Les donnees live sont injectees dans le contexte du BA Agent
- [ ] Credentials en memoire seulement (pas de persistance disque)
- [ ] API key jamais dans les logs
- [ ] Tests (auth mock + guardian integration)
- [ ] Review dans reviews/ODAI-CORE-004-review.md
- [ ] make check passe

## Design

### Flow utilisateur
```
$ odooai chat --url https://mon-odoo.com --db production
Login Odoo : marie@acme.fr
API Key : ********

Connexion... OK (Odoo 17.0, 12 modules installes)
Modules : sale, stock, purchase, account, crm, ...

Posez vos questions. Tapez 'quit' pour quitter.

Vous > Combien de devis ai-je en brouillon ?
[Domaine : Ventes & CRM | Connexion live : oui]

OdooAI repond avec les donnees REELLES du client
(anonymisees par le Guardian si SENSITIVE)
```

### Architecture
```
CLI chat --url --db
  → input login + api_key (getpass, pas visible)
  → OdooClient.authenticate(login, api_key) → OdooUserInfo
  → OdooClient.search_read('ir.module.module', [('state','=','installed')]) → modules
  → Boucle questions :
    → Orchestrator.handle_question(question, odoo_client, profile)
      → detect_domain
      → load BA Profile
      → SI connexion live : guarded_odoo_read → donnees live
      → BA Agent(question, profile, odoo_context=live_data)
      → Reponse
```

### Modifications

**cli.py** : ajouter `--url`, `--db` au chat, auth au demarrage, passer le client a l'orchestrator

**orchestrator.py** : `handle_question` accepte un `OdooClient` optionnel, si present fait des appels live guardes

**ba_agent.py** : accepte un `odoo_context` optionnel (donnees live sanitisees) en plus du BA Profile

## Fichiers impactes
| Fichier | Action |
|---------|--------|
| `odooai/cli.py` | Modifier — `--url`, `--db`, auth, getpass |
| `odooai/agents/orchestrator.py` | Modifier — OdooClient optionnel, appels live |
| `odooai/agents/ba_agent.py` | Modifier — odoo_context optionnel |
| `tests/agents/test_orchestrator.py` | Etendre — tests connexion live mockee |
| `reviews/ODAI-CORE-004-review.md` | Creer |

## Securite
- Credentials en memoire seulement (variable locale, pas de stockage)
- API key saisie via `getpass` (pas visible dans le terminal)
- Guardian intercepte TOUTES les donnees live
- API key jamais loggee (structlog ne log que model/method/uid)
- Review Security Architect (07) obligatoire

## Dependances
- ODAI-CORE-002 (DONE) — OdooClient
- ODAI-SEC-001 (DONE) — Security Guardian
- ODAI-AGENT-002 (DONE) — Guardian wire

## Estimation
M (1-3 jours)
