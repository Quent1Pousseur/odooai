# ODAI-DATA-002 — BA Profile Schema + BA Factory

## Status
DONE (spec redigee apres implementation — erreur de processus)

## Auteur
AI Engineer (09) + Backend Architect (08)

## Reviewers
Odoo Expert (10), Prompt Engineer (25), CTO (02)

## Date
2026-03-17

## Contexte
Les Knowledge Graphs (DATA-001) sont generes. Il faut maintenant les transformer en intelligence business exploitable par le LLM : les BA Profiles.

## Objectif
1. Schema Pydantic pour BA Profiles (par domaine fonctionnel, pas par module)
2. BA Factory : prompt LLM qui transforme un KG summary en BA Profile
3. CLI `odooai generate-ba <domain> --save`
4. 9 domaines fonctionnels couverts

## Definition of Done
- [x] Schema BAProfile (capabilities, feature_discoveries, gotchas)
- [x] BA Factory avec prompt structure (system + user)
- [x] KG summary builder (compress KG en ~2000 tokens)
- [x] CLI generate-ba avec save
- [x] 9 BA Profiles generes par le fondateur
- [x] Premiere depense LLM reelle

## Design

### Schema BA Profile
```python
BAProfile:
  domain_name, domain_id, modules_covered, language
  summary (2-3 phrases)
  capabilities: [DomainCapability]
  feature_discoveries: [FeatureDiscovery]  # hidden gems
  gotchas: [Gotcha]  # pieges
  cross_module_combos, limitations
  metadata: odoo_version, generated_at, model_used, token_count
```

### Pipeline
```
Knowledge Graphs → build_kg_summary() → 2000 tokens
→ build_ba_messages() → system prompt + user prompt
→ Anthropic API (Sonnet) → JSON response
→ parse + validate → BAProfile
→ save to knowledge_store/{version}/_ba_profiles/{domain}.json
```

### 9 domaines
sales_crm, supply_chain, manufacturing, accounting, hr_payroll,
project_services, helpdesk, ecommerce, pos

## Fichiers
| Fichier | Action |
|---------|--------|
| `odooai/knowledge/schemas/ba_profile.py` | Cree |
| `odooai/knowledge/ba_factory.py` | Cree |
| `odooai/knowledge/_ba_prompt.py` | Cree |
| `odooai/cli.py` | Modifie — ajout generate-ba |

## Securite
Les KG envoyes au LLM ne contiennent PAS de donnees client — que de la meta-information Odoo (noms de modeles, types de champs). Pas d'impact securite direct.

## NOTE PROCESSUS
**Cette spec a ete redigee APRES l'implementation.** C'est une violation de la regle d'or "RIEN ne se code sans spec". Ne plus jamais reproduire cette erreur.

## Estimation
M (1-3 jours) — realise en 1 session
