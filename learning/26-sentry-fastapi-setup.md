# Learning — SOC Analyst (26) — Sentry + FastAPI Setup (approfondissement)
## Date : 2026-03-21
## Duree : 3 heures (jour 2)

## Ce que j'ai appris (approfondissement)

### Setup concret Sentry + FastAPI
```bash
pip install sentry-sdk[fastapi]
```

```python
import sentry_sdk
sentry_sdk.init(
    dsn="https://xxx@sentry.io/xxx",
    traces_sample_rate=0.1,  # 10% des requetes tracees
    profiles_sample_rate=0.1,
)
```

C'est tout. 3 lignes dans main.py. Sentry capture automatiquement :
- Exceptions non gerees
- Slow transactions (> 2s)
- Performance par endpoint

### Alertes recommandees
1. Toute erreur 500 → Slack/email immediat
2. Error rate > 1% sur 5 min → alerte
3. Latence p95 > 15s sur /api/chat → alerte

### Cout
- Free tier : 5K errors/mois, 10K transactions → suffisant pour la beta
- Team : $26/mois si on depasse

## Ce que je recommande
Sprint 5 : 3 lignes dans main.py + creer le projet Sentry. 15 minutes.

## Sources
- Sentry FastAPI documentation
- sentry-sdk changelog
