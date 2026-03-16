# Learning — DevOps (22) — GitHub Actions for Continuous Deployment to VPS
## Date : 2026-03-21 (Sprint 5)
## Duree : 3 heures

## Ce que j'ai appris

1. **Le pattern SSH + Docker Compose est le plus adapte pour un VPS** : pas besoin de Kubernetes pour un SaaS early-stage. Un workflow GitHub Actions qui (a) build l'image Docker, (b) push vers GitHub Container Registry (ghcr.io), (c) SSH sur le VPS, (d) `docker compose pull && docker compose up -d` couvre 95% des besoins.

2. **Les secrets GitHub sont le bon endroit pour les credentials** : `SSH_PRIVATE_KEY`, `VPS_HOST`, `VPS_USER` dans les repository secrets. Jamais de credentials en clair dans le workflow YAML. Le SSH key doit etre une deploy key dediee, pas la cle personnelle du fondateur.

3. **Le zero-downtime deployment avec Docker Compose** : utiliser `docker compose up -d --no-deps --build backend` pour redemarrer uniquement le service modifie. Avec un healthcheck dans le Dockerfile et un reverse proxy (Caddy ou Traefik), le traffic bascule automatiquement quand le nouveau container est healthy.

4. **Les environnements GitHub (staging/production)** : on peut configurer des regles de protection — staging deploie automatiquement sur push to main, production necessite une approbation manuelle. Ca donne un workflow : PR merge > auto-deploy staging > test > approve > deploy prod.

5. **Le rollback doit etre instantane** : garder les 3 dernieres images Docker taguees (latest, previous, N-2). Le rollback = `docker compose pull` avec le tag previous + `docker compose up -d`. Pas besoin de re-build, c'est un pull de 30 secondes.

## Comment ca s'applique a OdooAI

1. **Pipeline CI/CD complete pour OdooAI** : le workflow combine les checks existants (`make check` = ruff + mypy + tests + bandit) avec le build Docker et le deploy. Si les checks echouent, pas de deploy. Ca garantit que seul du code valide arrive en production.

2. **Separation backend/frontend dans le pipeline** : le backend FastAPI et le frontend Next.js ont des Dockerfiles separes et des cycles de deploy independants. Modifier le frontend ne redploie pas le backend et vice versa. Ca reduit le risque et accelere les deploys.

3. **Les variables d'environnement sensibles (Anthropic API key, DB password, encryption key) sont injectees via Docker secrets** : jamais dans l'image, jamais dans le repo. Le `docker-compose.prod.yml` reference les secrets stockes sur le VPS dans `/opt/odooai/secrets/`.

## Ce que je recommande

1. **Sprint 6** : Creer le Dockerfile multi-stage pour le backend (`python:3.11-slim`, install deps, copy code, healthcheck). Tester le build localement. Cout : 2h.

2. **Sprint 7** : Ecrire `.github/workflows/deploy-staging.yml` avec les etapes : checkout > check > build > push ghcr.io > SSH deploy. Configurer le VPS staging avec Docker Compose + Caddy reverse proxy.

3. **Sprint 8** : Ajouter le workflow production avec environment protection rules et le mecanisme de rollback automatique si le healthcheck echoue dans les 60 secondes post-deploy.

## Sources

1. GitHub Docs — "Deploying with GitHub Actions" (2025) : https://docs.github.com/en/actions/deployment
2. Docker Docs — "Multi-stage builds best practices" (2025) : https://docs.docker.com/build/building/multi-stage/
3. Caddy Documentation — "Reverse Proxy with automatic HTTPS" : https://caddyserver.com/docs/caddyfile/directives/reverse_proxy
