# Mapping Concurrentiel Mondial — IA x Odoo/ERP
## Competitive Intelligence (34)
## Date : 2026-03-21

---

## 1. Concurrents directs (IA x Odoo)

| Produit | Approche | Marche | Forces | Faiblesses |
|---------|----------|--------|--------|-----------|
| **Prodooctivity** | MCP gateway | Devs/integrateurs | Multi-tenant, RBAC, Stripe | Pas d'intelligence metier |
| **OdooAI (nous)** | BA IA + KG | PME + integrateurs | Code source, recommandations | MVP, pas encore en prod |

**Verdict** : 1 seul concurrent direct identifie. Le marche est VIDE.

## 2. Concurrents indirects (IA x ERP)

| Produit | ERP cible | Approche | Prix |
|---------|----------|----------|------|
| Microsoft Copilot | Dynamics 365 | Integre dans l'ERP | Inclus dans licence |
| SAP Joule | SAP S/4HANA | Integre dans l'ERP | Inclus |
| Oracle AI | Oracle Cloud | Integre dans l'ERP | Inclus |
| Salesforce Einstein | Salesforce | CRM analytics | Inclus dans plans premium |

**Conclusion** : les grands ERP integrent l'IA nativement. Odoo n'a PAS d'IA integree. C'est notre opportunite.

## 3. Alternatives generiques

| Produit | Force | Faiblesse vs OdooAI |
|---------|-------|-------------------|
| ChatGPT | Generique, pas cher | Ne connait pas votre Odoo |
| Claude | Raisonnement avance | Ne connait pas votre Odoo |
| Perplexity | Sources citees | Pas de connexion ERP |
| Consultants Odoo | Expertise humaine | 200€/h, pas scalable |

## 4. Positionnement OdooAI

```
                    Generique ←→ Specialise Odoo
                         |
           ChatGPT       |       Consultants
                         |
         Perplexity      |     OdooAI ★
                         |
            Claude       |    Prodooctivity
                         |
                    Pas connecte ←→ Connecte a l'instance
```

**Notre position unique** : specialise Odoo + connecte a l'instance + intelligence du code source.

## 5. Barriere a l'entree (moat)

| Barriere | Difficulte a reproduire |
|----------|----------------------|
| 1218 modules parses (KG) | 2-3 semaines de dev |
| BA Profiles (9 domaines) | 1 semaine + couts LLM |
| Security Guardian | 1 semaine |
| Connaissance code source Odoo | Acces au code = gratuit (LGPL) |

**Realite** : notre moat technique est FAIBLE. N'importe qui peut parser le code Odoo.

**Le vrai moat** : execution, communaute, et brand. Etre le premier a s'etablir comme "le BA IA pour Odoo". Speed to market.

## 6. Risques concurrentiels

| Risque | Probabilite | Impact | Mitigation |
|--------|------------|--------|-----------|
| Odoo SA lance son propre IA | Moyenne (12-18 mois) | Tres eleve | Etre etabli avant, communaute, integrateurs |
| Prodooctivity ajoute de l'intelligence | Moyenne | Eleve | Executer plus vite, UX superieure |
| Un gros (Microsoft, Google) cible Odoo | Faible | Eleve | Niche trop petite pour les GAFAM |
| Fork open source de notre approche | Faible | Moyen | Closed source, execution, communaute |

## 7. Recommandation strategique

**Speed is everything.** Le marche est vide. Le premier a s'etablir gagne.

1. **Beta en 4 semaines** — avec 5-10 PME
2. **Integrateurs en 8 semaines** — programme partenaire
3. **Communaute Odoo** — presence forum + LinkedIn + events
4. **Moat execution** — iterer plus vite que quiconque
