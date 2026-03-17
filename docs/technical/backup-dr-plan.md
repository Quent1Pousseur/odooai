# OdooAI — Backup & Disaster Recovery Plan
## Chaos Engineer (31)
## Date : 2026-03-21

## 1. Donnees critiques

| Donnee | Criticite | Regenerable ? | Backup necessaire ? |
|--------|----------|---------------|-------------------|
| Conversations (DB) | Haute | Non | **OUI** |
| Knowledge Graphs (JSON) | Moyenne | Oui (re-parse) | Non — regenerable |
| BA Profiles (JSON) | Moyenne | Oui (re-generate) | Non — regenerable |
| .env (secrets) | Critique | Non | **OUI** (hors du repo) |
| Code source | Critique | Oui (Git) | Non — GitHub est le backup |
| waitlist.json | Basse | Non | Oui (mais peu critique) |

## 2. Strategie de backup

### Dev (actuel — SQLite)
```bash
# Cron toutes les 6h
cp odooai.db backups/odooai-$(date +%Y%m%d-%H%M).db

# Retention : 7 jours
find backups/ -name "*.db" -mtime +7 -delete
```

### Staging/Prod (PostgreSQL)
```bash
# pg_dump quotidien (2:00 AM)
pg_dump -Fc odooai > backups/odooai-$(date +%Y%m%d).dump

# WAL archiving pour PITR (continu)
archive_command = 'cp %p /backups/wal/%f'

# Retention : 30 jours dumps, 7 jours WAL
```

## 3. Scenarios de disaster et reponse

### Scenario A : API Anthropic indisponible
- **Detection** : OverloadedError ou timeout > 10s
- **Impact** : Chat inutilisable
- **Reponse immediate** : message utilisateur "Service temporairement indisponible"
- **Fallback** : repondre avec BA Profiles only (sans LLM) — donnees statiques mais utiles
- **Recovery** : retry automatique (deja implemente avec backoff)

### Scenario B : Base de donnees corrompue
- **Detection** : erreur SQLAlchemy au demarrage
- **Impact** : perte des conversations
- **Reponse** : restaurer le dernier backup
- **Recovery time** : < 5 minutes (cp du backup)
- **Data loss** : maximum 6h (intervalle backup)

### Scenario C : Serveur tombe
- **Detection** : Uptime Robot alerte en < 1 min
- **Impact** : service down
- **Reponse** : restart automatique (docker restart policy: unless-stopped)
- **Si echec** : redeploy depuis la derniere image Docker
- **Recovery time** : < 5 minutes

### Scenario D : Fuite de credentials
- **Detection** : audit logs, monitoring connexions Odoo
- **Impact** : acces non-autorise a l'instance Odoo du client
- **Reponse** : revoquer la cle API Odoo cote client, notifier l'utilisateur
- **Note** : les credentials ne sont pas stockes — session only. Risque = interception en transit (sans HTTPS)

## 4. Single Points of Failure (SPOF)

| SPOF | Impact | Mitigation | Sprint |
|------|--------|-----------|--------|
| API Anthropic | Chat mort | Fallback BA Profile only | 5 |
| SQLite/PostgreSQL | Perte conversations | Backup 6h + PITR | 5 |
| Serveur unique | Service down | Docker restart + monitoring | 5 |
| DNS/domaine | Site inaccessible | Monitoring Uptime Robot | 5 |
| Cle API fondateur | Plus de LLM calls | Cle de secours en .env.backup | Immediat |

## 5. Objectifs de recovery

| Metrique | Cible dev | Cible staging | Cible prod |
|----------|----------|--------------|-----------|
| RPO (data loss max) | 6h | 1h | 15 min (PITR) |
| RTO (recovery time) | 30 min | 10 min | 5 min |
| Uptime cible | — | 99% | 99.9% |

## 6. Actions immediates

- [x] Ce document
- [ ] Script backup SQLite (cron 6h) — Sprint 5
- [ ] Uptime Robot sur /health — Sprint 5
- [ ] Fallback "BA Profile only" quand LLM down — Sprint 5
- [ ] pg_dump automatique en staging — Sprint 6
