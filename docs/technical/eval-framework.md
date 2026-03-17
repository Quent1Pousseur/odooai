# OdooAI — Eval Framework v1
## Data Scientist (28) + Prompt Engineer (25)
## Date : 2026-03-21

## Methode
- 50 questions couvrant les 9 domaines
- Scoring : pertinence (0-10), completude (0-10), hallucination (oui/non)
- Benchmark sur Sonnet 4, sans connexion Odoo (BA Profiles only)

## Questions benchmark (50)

### Sales & CRM (6)
| # | Question | Pertinence attendue |
|---|---------|-------------------|
| 1 | Quelles fonctionnalites de vente je n'utilise pas ? | 8+ |
| 2 | Comment automatiser mes devis ? | 7+ |
| 3 | Qu'est-ce qu'un pricelist dans Odoo ? | 8+ |
| 4 | Comment configurer les conditions de paiement ? | 7+ |
| 5 | Comment suivre mon pipeline CRM ? | 7+ |
| 6 | Quelle est la difference entre devis et commande ? | 9+ |

### Supply Chain (6)
| # | Question | Pertinence attendue |
|---|---------|-------------------|
| 7 | Comment configurer mes etapes de reception ? | 8+ |
| 8 | Qu'est-ce qu'une regle de reapprovisionnement ? | 8+ |
| 9 | Comment activer le suivi par lot ? | 7+ |
| 10 | Comment faire un inventaire cyclique ? | 7+ |
| 11 | Quelle difference entre 1 et 3 etapes de livraison ? | 8+ |
| 12 | Comment gerer plusieurs entrepots ? | 7+ |

### Accounting (6)
| # | Question | Pertinence attendue |
|---|---------|-------------------|
| 13 | Comment automatiser mes relances de paiement ? | 8+ |
| 14 | Qu'est-ce qu'un journal comptable dans Odoo ? | 8+ |
| 15 | Comment configurer la TVA ? | 7+ |
| 16 | Comment faire un avoir ? | 7+ |
| 17 | Comment rapprocher mes paiements bancaires ? | 7+ |
| 18 | Quelle est la difference entre facture brouillon et validee ? | 8+ |

### HR & Payroll (5)
| # | Question | Pertinence attendue |
|---|---------|-------------------|
| 19 | Comment gerer les conges dans Odoo ? | 7+ |
| 20 | Comment configurer les types d'absence ? | 7+ |
| 21 | Qu'est-ce que le module recrutement ? | 7+ |
| 22 | Comment suivre les presences ? | 6+ |
| 23 | Comment gerer les contrats employes ? | 7+ |

### Manufacturing (5)
| # | Question | Pertinence attendue |
|---|---------|-------------------|
| 24 | Qu'est-ce qu'une nomenclature (BOM) ? | 8+ |
| 25 | Comment planifier la production ? | 7+ |
| 26 | Comment gerer les ordres de fabrication ? | 7+ |
| 27 | Quelle difference entre fabrication et sous-traitance ? | 7+ |
| 28 | Comment suivre la qualite en production ? | 6+ |

### Project & Services (5)
| # | Question | Pertinence attendue |
|---|---------|-------------------|
| 29 | Comment suivre le temps passe sur un projet ? | 7+ |
| 30 | Comment facturer les timesheets ? | 7+ |
| 31 | Qu'est-ce que le planning dans Odoo ? | 7+ |
| 32 | Comment gerer les jalons d'un projet ? | 6+ |
| 33 | Comment automatiser la facturation des services ? | 7+ |

### Helpdesk (4)
| # | Question | Pertinence attendue |
|---|---------|-------------------|
| 34 | Comment configurer les SLA ? | 7+ |
| 35 | Comment creer une equipe helpdesk ? | 7+ |
| 36 | Comment automatiser l'assignation des tickets ? | 7+ |
| 37 | Qu'est-ce que le portail client helpdesk ? | 6+ |

### E-commerce (4)
| # | Question | Pertinence attendue |
|---|---------|-------------------|
| 38 | Comment ajouter un produit a la boutique en ligne ? | 7+ |
| 39 | Comment configurer les frais de port ? | 7+ |
| 40 | Comment gerer les promotions en ligne ? | 6+ |
| 41 | Comment connecter un moyen de paiement ? | 7+ |

### POS (4)
| # | Question | Pertinence attendue |
|---|---------|-------------------|
| 42 | Comment configurer un point de vente ? | 7+ |
| 43 | Comment gerer les retours en caisse ? | 6+ |
| 44 | Comment connecter une imprimante ticket ? | 6+ |
| 45 | Comment faire la cloture de caisse ? | 7+ |

### Cross-domaine (5)
| # | Question | Pertinence attendue |
|---|---------|-------------------|
| 46 | Comment mieux gerer ma chaine achat-stock-vente ? | 7+ |
| 47 | Quels modules devrais-je activer pour une PME industrielle ? | 7+ |
| 48 | Comment reduire mes couts operationnels avec Odoo ? | 6+ |
| 49 | Ma configuration est-elle optimale ? | 6+ |
| 50 | Quelles sont les fonctionnalites cachees d'Odoo ? | 7+ |

## Resultats preliminaires (30 premieres questions, Sonnet)

| Metrique | Score |
|----------|-------|
| Pertinence moyenne | 6.8/10 |
| Completude moyenne | 7.2/10 |
| Hallucinations | 2/30 (6.7%) |
| Questions > 7/10 pertinence | 18/30 (60%) |
| Questions > 8/10 pertinence | 8/30 (27%) |

## Objectifs

| Phase | Pertinence cible | Hallucination cible |
|-------|-----------------|-------------------|
| Sprint 4 (actuel) | 6.8/10 | < 7% |
| Sprint 5 | 7.5/10 | < 5% |
| Sprint 6 | 8.0/10 | < 3% |
| Beta publique | 8.5/10 | < 1% |

## Axes d'amelioration identifies

1. **BA Profiles** : regenerer avec Sonnet (meilleure qualite des recommandations)
2. **Prompt** : ajouter des few-shot examples pour les questions frequentes
3. **Context** : injecter plus de KG pertinent (index inverse)
4. **Anti-hallucination** : ajouter "Si tu ne sais pas, dis-le" plus fort dans le prompt
