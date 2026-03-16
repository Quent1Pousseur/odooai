# OdooAI — Cost Forecasting
## CFO (15) + AI Engineer (09) + Observability (38)
## Date : 2026-03-21

## 1. Cout par requete

| Modele | Input tokens | Output tokens | Cout moyen/question |
|--------|-------------|---------------|-------------------|
| Sonnet 4 (complexe) | ~3000 | ~1500 | $0.030 (0.025€) |
| Haiku 4.5 (simple) | ~2000 | ~800 | $0.005 (0.004€) |
| Moyenne (routing 60/40) | ~2400 | ~1100 | $0.015 (0.013€) |

## 2. Projection par plan

| Plan | Prix | Requetes/mois | Cout LLM | Cout infra | Marge |
|------|------|--------------|----------|-----------|-------|
| Starter (49€) | 49€ | 100 | 1.30€ | 2€ | **93%** |
| Pro (149€) | 149€ | 500 | 6.50€ | 5€ | **92%** |
| Enterprise (399€) | 399€ | 2000* | 26€ | 10€ | **91%** |

*Fair use, moyenne estimee

## 3. Projection par nombre de clients

| Clients | MRR | Cout LLM/mois | Cout infra/mois | Profit/mois |
|---------|-----|--------------|----------------|------------|
| 10 | 1 490€ | 65€ | 50€ | **1 375€** |
| 50 | 7 450€ | 325€ | 150€ | **6 975€** |
| 100 | 14 900€ | 650€ | 300€ | **13 950€** |
| 500 | 74 500€ | 3 250€ | 1 000€ | **70 250€** |
| 1 000 | 149 000€ | 6 500€ | 2 000€ | **140 500€** |

*Hypothese : tous en plan Pro (149€). Mix reel sera inferieur.*

## 4. Cout infrastructure mensuel

| Composant | 10 clients | 100 clients | 1000 clients |
|-----------|-----------|-------------|-------------|
| VPS (backend) | 20€ | 80€ | 300€ |
| VPS (frontend) | 10€ | 30€ | 100€ |
| PostgreSQL | 0€ (inclus) | 50€ (managed) | 200€ |
| Redis | 0€ (inclus) | 20€ | 50€ |
| Monitoring (Sentry) | 0€ | 26€ | 80€ |
| Domaine + DNS | 15€ | 15€ | 15€ |
| Backup storage | 5€ | 10€ | 50€ |
| **Total** | **50€** | **231€** | **795€** |

## 5. Break-even

- Couts fixes mensuels (1 dev, infra, outils) : ~3 000€ estime
- Break-even : **21 clients Pro** (21 x 149€ = 3 129€)
- Avec le routing Haiku/Sonnet : break-even a **19 clients**

## 6. Risques financiers

| Risque | Impact | Mitigation |
|--------|--------|-----------|
| Anthropic augmente ses prix de 50% | Marge passe de 92% a 88% | Fallback OpenAI |
| Usage excessif (1 client = 5000 req) | Cout LLM explose | Fair use policy + rate limiting |
| Peu de clients Premium | MRR plus bas | Focus acquisition Pro |
| Churn eleve | Perte revenus | Customer Success + valeur continue |

## Verdict

**Marge excellente (91-93%).** Le modele SaaS est viable des 20 clients.
Le routing intelligent Haiku/Sonnet reduit les couts de 50%.
L'infra est negligeable vs le revenu meme a 10 clients.
