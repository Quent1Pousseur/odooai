# Learning — SRE (23) — Uptime Monitoring Tools (Uptime Robot, Betteruptime)
## Date : 2026-03-21 (Sprint 5)
## Duree : 3 heures

## Ce que j'ai appris

1. **Uptime Robot (free tier) couvre les besoins de base** : 50 monitors, checks toutes les 5 minutes, alertes email/Slack/webhook. Pour un SaaS early-stage, c'est suffisant. Le plan Pro (7$/mois) descend a 1 minute d'intervalle et ajoute les status pages publiques.

2. **Better Stack (ex-Betteruptime) integre monitoring + incident management + logs** : c'est plus complet mais plus cher (25$/mois). L'avantage est la status page integree avec incident timeline, ce qui est important pour la confiance des clients SaaS. Les on-call rotations sont incluses.

3. **Les checks HTTP ne suffisent pas** : un endpoint `/health` qui retourne 200 ne garantit pas que le service fonctionne. Il faut des checks "deep health" : la DB repond, Redis est accessible, l'API Anthropic est joignable. Le `/health` d'OdooAI doit tester chaque dependance.

4. **Les SLO (Service Level Objectives) doivent etre definis AVANT le lancement** : pour un SaaS B2B, 99.5% uptime (3.65h de downtime/mois) est un minimum acceptable en early-stage. 99.9% est la cible a 6 mois. Les SLO guident les decisions d'architecture et de budget infrastructure.

5. **L'alerte multi-canal evite les incidents silencieux** : configurer au minimum 3 canaux d'alerte : email, Slack webhook, SMS pour les critiques. L'escalation automatique (si pas d'ack en 15 minutes, SMS au fondateur) evite que les incidents passent inapercus la nuit.

## Comment ca s'applique a OdooAI

1. **Le endpoint `/health` doit devenir un deep healthcheck** : actuellement il retourne juste un status. Il doit verifier : SQLite/PostgreSQL connectivity, Redis ping, et optionnellement un dry-run Anthropic API. Retourner un JSON avec le status de chaque composant et un status global.

2. **Status page publique pour la confiance client** : des le lancement beta, avoir une page `status.odooai.com` qui affiche l'uptime en temps reel. Ca differencie OdooAI des concurrents qui n'ont pas de transparence sur leur disponibilite. Better Stack ou Uptime Robot Pro fournissent ca out-of-the-box.

3. **Monitorer les metriques business en plus de l'infra** : temps de reponse moyen du Business Analyst, taux d'erreur LLM, nombre de connexions Odoo actives. Ces metriques detectent les degradations que le simple uptime HTTP ne voit pas.

## Ce que je recommande

1. **Sprint 6** : Enrichir `/health` avec les checks de dependances (DB, Redis). Creer un endpoint `/health/detailed` pour le monitoring externe. Ajouter le check dans `odooai/api/routers/health.py`. Cout : 1h.

2. **Sprint 7** : Configurer Uptime Robot (free tier) avec 5 monitors : health endpoint, API response time, frontend availability, status page, SSL certificate expiry. Webhook vers un channel Slack #alerts.

3. **Sprint 8** : Definir les SLO formels (99.5% uptime, < 2s response time p95, < 1% error rate). Creer un dashboard SLO dans Better Stack si le budget le permet, sinon un script qui calcule les SLO depuis les logs.

## Sources

1. Uptime Robot — "Features and Pricing" (2025) : https://uptimerobot.com/pricing/
2. Better Stack — "Uptime Monitoring for SaaS" (2025) : https://betterstack.com/uptime
3. Google SRE Book — "Service Level Objectives" : https://sre.google/sre-book/service-level-objectives/
