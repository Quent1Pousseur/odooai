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
