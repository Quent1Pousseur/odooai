# Learning — SOC Analyst (26) — Monitoring SaaS Security
## Date : 2026-03-20
## Duree : 4 heures

## Ce que j'ai appris

### Monitoring security pour un SaaS IA
- **Couche 1 — Application** : rate limiting, auth failures, credential abuse
- **Couche 2 — Infrastructure** : CPU/RAM/disk, container health, network anomalies
- **Couche 3 — IA specifique** : prompt injection attempts, token abuse, data exfiltration

### Outils recommandes pour un SaaS en demarrage
| Outil | Usage | Cout |
|-------|-------|------|
| Sentry | Error tracking, crash reports | Free tier |
| Grafana + Loki | Dashboards + log aggregation | Self-hosted = free |
| Uptime Robot | Uptime monitoring, alertes | Free tier |
| Fail2ban | Rate limiting IP, brute force protection | Open source |

### Alertes prioritaires pour OdooAI
1. **Auth failures > 5/min** par IP → possible brute force
2. **Token usage > 50K** par requete → possible prompt injection/abuse
3. **Erreur 500 rate > 1%** → bug en production
4. **Latence p99 > 30s** → degradation de service
5. **Credentials Odoo echec > 3/user** → erreur config ou attaque

## Comment ca s'applique a OdooAI
- Zero monitoring en place actuellement — c'est un risque
- Sentry + Uptime Robot = 0€ et couvre 80% des besoins
- Le challenge du Security Auditor sur le rate limiting est pertinent

## Ce que je recommande
1. Sprint 5 : Sentry integration (backend + frontend)
2. Sprint 5 : Uptime Robot sur /health
3. Sprint 6 : Grafana + Loki quand on a du staging

## Sources
- OWASP Logging Cheat Sheet
- Sentry FastAPI integration guide
