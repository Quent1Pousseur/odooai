# ODAI-AGENT-003 — Tool-Use : le LLM genere ses propres requetes Odoo

## Status
IN PROGRESS

## Auteur
AI Engineer (09) + Backend Architect (08)

## Reviewers
Security Architect (07), Odoo Expert (10), CTO (02)

## Date
2026-03-17

## Contexte
Le MVP CLI fonctionne mais le contexte live est predetermine (requetes fixes). Le LLM recoit les 10 dernieres commandes au lieu de chercher ce que l'utilisateur demande. Le fondateur a confirme : "les reponses sont a cote de la plaque".

## Objectif
Le LLM decide quoi requeter dans Odoo en fonction de la question. Pattern tool-use Anthropic : le LLM recoit des outils (search_read, search_count) et genere les appels.

## Principe
```
Question : "Combien de factures impayees ai-je ?"

Avant (contexte fixe) :
  → Charge les 10 dernieres commandes (hors sujet)
  → LLM invente une reponse

Apres (tool-use) :
  → LLM appelle search_count(account.move, [state=posted, payment_state=not_paid])
  → Guardian valide le domain
  → Odoo retourne : 7
  → LLM repond : "Vous avez 7 factures impayees"
```

## Design

### Tools exposes au LLM

```python
tools = [
    {
        "name": "odoo_search_read",
        "description": "Search and read records from the Odoo database",
        "input_schema": {
            "type": "object",
            "properties": {
                "model": {"type": "string", "description": "Odoo model (e.g. sale.order)"},
                "domain": {"type": "array", "description": "Search filter"},
                "fields": {"type": "array", "items": {"type": "string"}},
                "limit": {"type": "integer", "default": 10},
            },
            "required": ["model", "domain", "fields"]
        }
    },
    {
        "name": "odoo_search_count",
        "description": "Count records matching a filter",
        "input_schema": {
            "type": "object",
            "properties": {
                "model": {"type": "string"},
                "domain": {"type": "array"},
            },
            "required": ["model", "domain"]
        }
    }
]
```

### Pipeline securise
```
LLM genere tool_call(model, domain, fields)
  → Guardian.guard_model_access(model)     # BLOCKED → refuse
  → Guardian.guard_method("search_read")   # OK (lecture)
  → DomainValidator.validate_domain(domain) # injection → refuse
  → OdooClient.search_read(...)
  → Guardian.sanitize_response(...)        # anonymise SENSITIVE
  → Resultat renvoye au LLM
  → LLM formule la reponse finale
```

### Max tool calls par question
Limite a **3 appels** par question pour eviter les boucles et controler les couts.

## Definition of Done
- [ ] BA Agent utilise le tool-use Anthropic
- [ ] Tools : odoo_search_read, odoo_search_count
- [ ] Chaque tool call passe par le Guardian (model + method + domain)
- [ ] Reponse sanitisee avant retour au LLM
- [ ] Max 3 tool calls par question
- [ ] Tests avec mock OdooClient
- [ ] Review dans reviews/ODAI-AGENT-003-review.md
- [ ] Fondateur teste et confirme amelioration
- [ ] make check passe

## Fichiers impactes
| Fichier | Action |
|---------|--------|
| `odooai/agents/ba_agent.py` | Recrire — ajouter tool-use loop |
| `odooai/agents/_tools.py` | Creer — definition des tools + execution |
| `odooai/agents/_live_context.py` | Supprimer — remplace par tool-use |
| `odooai/agents/orchestrator.py` | Simplifier — passer le client au BA Agent |
| `tests/agents/test_tool_use.py` | Creer |
| `reviews/ODAI-AGENT-003-review.md` | Creer |

## Securite
- Chaque tool call est valide par le Guardian AVANT execution
- Le LLM ne peut PAS appeler de methodes d'ecriture (write, create) via tools
- Le domain_validator bloque les injections generees par le LLM
- Review Security Architect (07) obligatoire

## Dependances
- ODAI-AGENT-002 (DONE) — Guardian wire
- ODAI-CORE-004 (DONE) — Connexion live

## Estimation
M (1-3 jours)
