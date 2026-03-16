# ODAI-INFRA-003 — Stripe Integration

## Status
SPEC READY

## Auteur
Integration Engineer (35) + CFO (15) + SaaS Architect (06)

## Date
2026-03-21

## Contexte
Pas de paiement = pas de revenus. Stripe est le standard pour le SaaS.

## Scope Sprint 6

### 3 plans
| Plan | Prix | Stripe Price ID |
|------|------|----------------|
| Starter | 49€/mois | price_starter_monthly |
| Professional | 149€/mois | price_pro_monthly |
| Enterprise | 399€/mois | price_enterprise_monthly |

### Endpoints
- `POST /api/billing/checkout` — cree une Stripe Checkout Session
- `POST /api/billing/portal` — redirige vers le Stripe Customer Portal
- `POST /api/webhooks/stripe` — recoit les events Stripe

### Webhooks a gerer
- `checkout.session.completed` → activer le plan
- `customer.subscription.updated` → changer le plan
- `customer.subscription.deleted` → desactiver le plan
- `invoice.payment_failed` → notifier l'utilisateur

### Modele DB
```sql
CREATE TABLE subscriptions (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    stripe_customer_id VARCHAR(255),
    stripe_subscription_id VARCHAR(255),
    plan VARCHAR(50),  -- 'starter', 'pro', 'enterprise'
    status VARCHAR(20),  -- 'active', 'past_due', 'canceled'
    current_period_end TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT now()
);
```

### Quota enforcement
- Compteur `api_calls_today` dans Redis (TTL 24h)
- Avant chaque /api/chat : verifier quota du plan
- Si depasse : 429 Too Many Requests + message "Quota atteint"

## Fichiers impactes
- `odooai/api/routers/billing.py` — nouveau
- `odooai/infrastructure/stripe_client.py` — nouveau
- `odooai/domain/entities/subscription.py` — nouveau

## Estimation
M (3-4 jours)

## Pre-requis
- Auth utilisateur (JWT) — doit etre fait avant
- PostgreSQL — pour la table subscriptions
