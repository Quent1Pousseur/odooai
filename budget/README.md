# OdooAI — Suivi Budgetaire

## Responsable : CFO (15)
## Mise a jour : Hebdomadaire

## Structure

```
budget/
  README.md              ← Ce fichier
  YYYY-MM-budget.md      ← Budget mensuel (previsionnel + reel)
  cost-model.md          ← Modele de couts LLM detaille
  pricing-analysis.md    ← Analyse de pricing et marges par plan
```

## Template Budget Mensuel

```markdown
# Budget — [Mois YYYY]

## Revenus
| Source | Prevu | Reel | Delta |
|--------|-------|------|-------|
| Starter (n clients) | €X | €X | +/-X |
| Professional (n clients) | €X | €X | +/-X |
| Enterprise (n clients) | €X | €X | +/-X |
| **MRR Total** | **€X** | **€X** | **+/-X** |

## Couts Variables
| Poste | Prevu | Reel | Delta |
|-------|-------|------|-------|
| LLM tokens (Anthropic) | $X | $X | +/-X |
| Infra (cloud) | $X | $X | +/-X |
| Redis (managed) | $X | $X | +/-X |
| Database (managed) | $X | $X | +/-X |
| CDN / bandwidth | $X | $X | +/-X |
| **Total variable** | **$X** | **$X** | **+/-X** |

## Couts Fixes
| Poste | Montant |
|-------|---------|
| Domaine + DNS | $X |
| Email (Resend) | $X |
| Monitoring (Grafana/etc) | $X |
| GitHub (Team) | $X |
| Outils divers | $X |
| **Total fixe** | **$X** |

## Marges
| Metrique | Valeur |
|----------|--------|
| Marge brute | X% |
| Marge par Starter | X% |
| Marge par Professional | X% |
| Marge par Enterprise | X% |
| Cout moyen par requete IA | $X.XXX |
| Cout moyen par client | €X/mois |

## Alertes
[Si un poste depasse le previsionnel de > 20%]

## Projection M+1
[Estimation basee sur la tendance actuelle]
```
