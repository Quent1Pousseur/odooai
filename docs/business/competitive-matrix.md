# OdooAI — Matrice Concurrentielle

## Auteur : Competitive Intelligence (34)
## Date : 2026-03-16

---

## Paysage concurrentiel

### Concurrents directs (assistant IA pour Odoo)

| Produit | Type | Ce qu'il fait | Ce qu'il ne fait PAS | Menace |
|---------|------|--------------|---------------------|--------|
| **Serveurs MCP Odoo** (GitHub, open source) | CRUD basique | search_read, create, write via MCP protocol | Aucune intelligence business, aucun conseil, aucune analyse | Faible — pas de moat, pas de business model |
| **ChatGPT + Odoo** (plugins/custom GPTs) | Chat generique | Repond a des questions sur Odoo via doc/internet | Pas connecte a l'instance, hallucinations, pas de KG | Faible — pas de contexte client, pas fiable |
| **Consultants Odoo** (integrateurs) | Humain | Configuration, formation, support personalise | Pas scalable, 150-300€/h, temporaire | Moyen — on les complement, on ne les remplace pas tous |

### Concurrents indirects (IA pour ERP)

| Produit | ERP | Approche | Differentiation OdooAI |
|---------|-----|----------|----------------------|
| Copilot for Dynamics 365 | Microsoft | IA integree nativement | Odoo only, mais Knowledge Graphs > doc |
| SAP Joule | SAP | Assistant IA pour SAP | Marche different (enterprise vs PME) |
| Oracle AI | Oracle | Analytics + predictions | Pas comparable (trop enterprise) |

### Menace Odoo SA

| Signal | Analyse | Impact |
|--------|---------|--------|
| Recrutements ML sur LinkedIn | 3-5 profils ML recrutes en 2025 | Moyen — pourrait indiquer un assistant IA interne |
| Aucune annonce officielle | Pas de roadmap publique avec IA | Faible a court terme |
| OdooExperience 2026 (octobre) | Historiquement, les nouveautes majeures y sont annoncees | Risque si assistant IA annonce |
| Odoo 19 (Q4 2026) | Nouvelle version majeure | L'IA pourrait etre une feature de v19 |

**Evaluation** : Odoo SA est le seul vrai risque. Mais meme s'ils lancent un assistant IA :
- Notre avantage : Knowledge Graphs extraits du code (ils utiliseraient la doc)
- Notre avantage : multi-version (17, 18, 19) — Odoo SA ne supporte que la derniere
- Notre avantage : objectif business > CRUD — les premiers assistants IA sont toujours du CRUD

## Notre moat (avantage concurrentiel defensif)

| Avantage | Duree de l'avance | Imitable ? |
|----------|-------------------|------------|
| **Knowledge Graphs** (1218 modules, 5514 modeles, 21013 champs) | 6-12 mois | Oui mais couteux (notre Code Analyst a pris 1 jour) |
| **BA Profiles** (intelligence business par domaine) | 12+ mois | Necessite expertise Odoo + LLM + validation humaine |
| **Expert Profiles** (recettes d'execution) | 12+ mois | Meme difficulte que BA |
| **Multi-version** (17, 18, 19) | Permanent | Chaque version = effort de maintenance |
| **Connexion live** (client instance) | 3-6 mois | Technique connue mais integration complexe |

## Positionnement

```
                    Intelligence business
                           ^
                           |
          OdooAI ●         |
                           |
    Consultants ●          |         ● Copilot/Joule
                           |           (enterprise)
    ────────────────────────+───────────────────────
    Manuel/cher            |          Automatise/scalable
                           |
         Forums ●          |     ● MCP Odoo (CRUD)
                           |
    ChatGPT+Odoo ●        |
                           |
                    CRUD basique
```

OdooAI est positionne en haut a droite : **intelligence business + automatise + scalable**. Personne n'est dans ce quadrant aujourd'hui.

## Recommandations strategiques

1. **Lancer en beta AVANT OdooExperience (octobre 2026)** — si Odoo SA annonce un assistant, on doit deja avoir des utilisateurs
2. **Cibler le multi-version** comme differentiation — "OdooAI fonctionne sur Odoo 17, 18 et 19" (Odoo SA ne supporterait que la derniere)
3. **Approcher les integrateurs comme partenaires, pas concurrents** — ils ont les clients, on a l'IA
4. **Documenter les KG comme moat** — chaque version d'Odoo analysee renforce notre avance
5. **Surveiller OdooExperience 2026** — si annonce IA, pivoter vers "compatible + meilleur"

> **CEO (01)** : "Le point 1 est critique. Date limite beta : **septembre 2026**. Ca nous donne 6 mois."
>
> **Sales (05)** : "Le point 3 est mon approche. Integrateurs = canal d'acquisition #1."
