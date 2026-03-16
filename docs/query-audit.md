# Audit Queries — N+1 et Performance
## DBA (30) + Senior Backend (19)
## Date : 2026-03-21

## Queries identifiees

### _live_context.py — 4 queries sequentielles
| Query | Modele | Risque N+1 | Note |
|-------|--------|-----------|------|
| sales context | sale.order | Non | limit=10, 1 query |
| stock context | stock.picking | Non | limit=10, 1 query |
| accounting context | account.move | Non | limit=10, 1 query |
| installed modules | ir.module.module | Non | limit=50, 1 query |

**Risque** : les 4 queries sont sequentielles. Si Odoo est lent, ca fait 4 x 200-500ms = 800ms-2s.
**Fix** : `asyncio.gather()` pour les executer en parallele. Gain : 600ms-1.5s.

### _tools.py — queries LLM-driven
| Query | Risque N+1 | Note |
|-------|-----------|------|
| search_read | Non | 1 query par tool call, limit=20 |
| search_count | Non | 1 query, pas de data |
| read_group | Non | 1 query, aggregation |

**Risque** : le LLM peut faire 10 tool calls sequentiels. Chaque tool call = 1 Odoo query + 1 LLM call. C'est par design, pas un N+1.

### database.py — SQLAlchemy async
| Query | Risque N+1 | Note |
|-------|-----------|------|
| get conversations | Non | 1 query avec order_by |
| get messages | Potentiel | Si on charge chaque conversation puis ses messages |
| save message | Non | 1 insert |

**Risque** : charger la sidebar (liste de conversations) puis les messages de la conversation selectionnee = 2 queries. C'est acceptable. Le vrai risque N+1 serait de charger les messages de TOUTES les conversations — ca n'arrive pas.

## Verdict

**Aucun N+1 critique detecte.** L'architecture est saine.

**1 optimisation recommandee** : parallelize les 4 queries de `_live_context.py` avec `asyncio.gather()`. Gain estime : 600ms-1.5s sur la premiere reponse.

## Fix recommande (Sprint 5)

```python
# Avant (sequentiel)
sales_data = await odoo_client.search_read(...)
stock_data = await odoo_client.search_read(...)
# ...

# Apres (parallele)
sales_data, stock_data, accounting_data, modules = await asyncio.gather(
    odoo_client.search_read(...),  # sales
    odoo_client.search_read(...),  # stock
    odoo_client.search_read(...),  # accounting
    odoo_client.search_read(...),  # modules
)
```

## Indexes recommandes (PostgreSQL)

Deja documentes dans ODAI-INFRA-002 :
- `idx_conversations_user` — multi-tenant
- `idx_conversations_updated` — tri sidebar
- `idx_messages_conversation` — messages d'une conv
- `idx_messages_domain` — analytics
