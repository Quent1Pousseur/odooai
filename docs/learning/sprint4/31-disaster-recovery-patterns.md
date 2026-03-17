# Learning — Chaos Engineer (31) — Disaster Recovery Patterns
## Date : 2026-03-20
## Duree : 4 heures

## Ce que j'ai appris

### Backup strategies pour SaaS
- **3-2-1 Rule** : 3 copies, 2 supports differents, 1 off-site
- SQLite : simple `cp` du fichier DB suffit en dev, mais en prod avec PostgreSQL il faut `pg_dump` + WAL archiving
- Les conversations sont la donnee critique — les KG sont regenerables

### Point-in-Time Recovery (PITR)
- PostgreSQL supporte PITR via WAL (Write-Ahead Log)
- Permet de restaurer a n'importe quel point dans le temps
- Essentiel pour un SaaS multi-tenant : si un client demande la suppression, on doit pouvoir restaurer ses donnees avant la suppression

### Chaos Engineering principles (Netflix)
- **Steady state hypothesis** : definir ce que "normal" veut dire avant de casser
- **Vary real-world events** : pas juste "server down" mais aussi "latence +500ms", "disk full", "DNS failure"
- **Run in production** (quand on sera prets) : les bugs de staging != les bugs de prod
- **Minimize blast radius** : commencer par des experiences petites et controlees

## Comment ca s'applique a OdooAI

- **Backup quotidien** de la DB conversations — priorite #1
- **PITR** pour PostgreSQL en prod — permet de restaurer a la minute pres
- **Tester la perte d'Anthropic** : le chat doit afficher un message clair, pas un crash
- **Tester la corruption DB** : le serveur doit demarrer meme si la DB est vide
- **Game day Sprint 5** : simuler API Anthropic down + DB corrompue + reseau instable

## Ce que je recommande

1. Avant deploiement staging : backup automatique de la DB toutes les 6h
2. Runbook "Anthropic down" : message utilisateur + bascule sur reponses BA Profile only
3. Premier game day en Sprint 5 — 2h max, scope limite (1 scenario)

## Sources
- Netflix Chaos Engineering (principlesofchaos.org)
- PostgreSQL PITR Documentation
- AWS Well-Architected Framework — Reliability Pillar
