# Learning — DevSecOps (24) — Rate Limiting FastAPI
## Date : 2026-03-21
## Duree : 3 heures

## Ce que j'ai appris

### Pourquoi c'est critique (challenge Security Auditor)
Sans rate limiting, un script peut :
- Spammer /api/chat → couts LLM explosent
- Bruteforcer des credentials Odoo via notre API
- DDoS le backend avec des requetes lourdes (tool calls)

### Solutions evaluees
| Solution | Complexite | Performance | Recommandation |
|----------|-----------|-------------|----------------|
| slowapi (leaky bucket) | Faible | Bonne | ✅ MVP |
| Redis rate limiter | Moyenne | Excellente | Sprint 6+ |
| Nginx rate limiting | Faible | Excellente | En prod derriere nginx |
| Cloudflare | Zero | Excellente | Si domaine configure |

### Implementation slowapi (recommandee pour Sprint 5)
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@router.post("/api/chat")
@limiter.limit("10/minute")
async def chat(request: Request, ...):
```

30 lignes de code. Rate limits recommandes :
- `/api/chat` : 10/minute (evite le spam LLM)
- `/api/waitlist` : 5/minute (evite le spam email)
- `/health` : 60/minute (monitoring OK)

## Comment ca s'applique a OdooAI
- Le finding #1 du Security Auditor est le rate limiting — c'est le fix le plus urgent
- slowapi est compatible FastAPI nativement
- En prod, combiner avec Nginx rate limiting (couche 2)

## Ce que je recommande
1. Sprint 5 : slowapi sur /api/chat (30 min)
2. Sprint 6 : Redis rate limiter pour le multi-instance
3. Prod : Nginx + Cloudflare en couche supplementaire

## Sources
- slowapi documentation
- OWASP Rate Limiting Cheat Sheet
