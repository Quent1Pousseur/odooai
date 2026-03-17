# DPA Anthropic — Data Processing Agreement
## Legal (16)
## Date : 2026-03-21
## Status : TEMPLATE — a signer avec Anthropic

---

## Contexte
OdooAI envoie des donnees utilisateur (questions + donnees Odoo anonymisees) a l'API Anthropic pour generer des reponses. Selon le RGPD, Anthropic est un sous-traitant (processor) et OdooAI est le responsable de traitement (controller).

## Anthropic DPA Standard
Anthropic fournit un DPA standard disponible sur leur site :
- URL : https://www.anthropic.com/legal/data-processing-agreement
- Couvre les obligations RGPD articles 28-29
- Inclut les clauses contractuelles types (CCT) pour transferts USA

## Actions

| # | Action | Responsable | Status |
|---|--------|-------------|--------|
| 1 | Telecharger le DPA Anthropic standard | Legal (16) | A faire |
| 2 | Verifier les clauses vs nos obligations | Legal (16) | A faire |
| 3 | Signer electroniquement | Fondateur (00) | A faire |
| 4 | Archiver dans le dossier legal | Legal (16) | A faire |

## Points a verifier dans le DPA
- [ ] Anthropic ne stocke PAS les donnees API (confirme dans leurs terms)
- [ ] Anthropic ne forme PAS ses modeles sur les donnees API (confirme)
- [ ] Clauses CCT pour transfert USA-EU incluses
- [ ] Notification en cas de breach
- [ ] Droit d'audit
- [ ] Sous-sous-traitants listes (AWS, GCP)

## Note
Le DPA est un prerequis AVANT la beta publique (donnees de tiers).
En beta privee avec le fondateur seulement, c'est moins urgent.
