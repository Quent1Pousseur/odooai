# R&D — Content Strategist (37) — SEO Content Generator
## Date debut : 2026-03-22
## Status : En cours
## Lead : Content Strategist (37)
## Equipe : + AI Eng (09) si disponible

## Objectif
Script Python qui genere des articles SEO a partir des Knowledge Graphs OdooAI. Chaque article repond a une question frequente des forums Odoo, avec des donnees techniques extraites du code source.

## Plan
1. Extraire les 20 questions les plus frequentes (source : docs/business/marketing/ecosysteme-odoo.md)
2. Pour chaque question, trouver les modeles/champs pertinents dans les KG
3. Generer un article structure : titre SEO, intro, reponse detaillee, chemin Odoo
4. Output : fichiers markdown prets a publier

## MVP
Script qui genere 5 articles de blog a partir de 5 questions + KG du module sale.

## Avancement
### Session 1 (2026-03-22)
- Projet cree et documente
- Prochaine etape : script de base qui lit un KG et genere un article

### Session 2 (2026-03-17)
- Script `generate.py` complet : charge un KG via `load_module_kg()`, extrait modeles/champs, genere des articles markdown
- Architecture du script : dataclasses `FieldInfo`, `ModelInfo`, `ArticleSpec` + fonctions de generation par article
- CLI avec `--module`, `--questions`, `--dry-run`
- 5 articles generes pour le module `sale` a partir des donnees REELLES du KG :
  1. `01-automatiser-devis-odoo.md` — Devis automatises (require_signature, validity_date, require_payment)
  2. `02-suivre-commandes-vente.md` — Suivi commandes (state, invoice_status, qty_delivered/invoiced)
  3. `03-champs-importants-commande.md` — Reference complete des 56 champs sale.order + 38 champs sale.order.line
  4. `04-calcul-montant-total.md` — Calcul montants (_compute_amounts, _compute_amount, formules)
  5. `05-conditions-paiement.md` — Conditions paiement (payment_term_id, transaction_ids, payment.provider)
- Chaque article suit le format : titre SEO, reponse courte, details avec refs techniques, etapes activation, modeles concernes
- Donnees extraites : noms de champs, types, compute methods, help texts, relations, selections — tout vient du KG
- Output dans `rnd/seo-content-generator/output/`
- Prochaine etape : ajouter support multi-modules, templates configurables, scoring de pertinence des champs

### Session 3 (2026-03-22)
- 5 articles produced from real KG data
- Script supports --module, --questions, --dry-run CLI
- Next: multi-module support, template system
