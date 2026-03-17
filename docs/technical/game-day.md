# Game Day #1 — Plan d'execution
## Chaos Engineer (31) + SRE (23) + AI Engineer (09)
## Date prevue : Sprint 5, semaine 2
## Duree : 2 heures

---

## Prerequis
- [ ] Sentry installe et DSN configure ✅
- [ ] /metrics endpoint fonctionnel ✅
- [ ] Backup SQLite recente
- [ ] Environnement de dev (PAS de prod)

## Scenarios

### Scenario 1 — API Anthropic indisponible (30 min)

**Comment simuler :** mettre une fausse API key dans .env

**Comportement attendu :**
- Le chat affiche un message d'erreur clair
- Sentry capture l'erreur
- Le /metrics incremente un compteur d'erreurs
- Le serveur ne crash PAS

**Comportement cible (apres fix) :**
- Fallback sur reponse BA Profile only
- Message : "Service IA temporairement indisponible. Voici ce que nous savons..."

**Verification :**
- [ ] Erreur visible dans les logs
- [ ] Sentry alert recue
- [ ] Serveur toujours debout apres 10 tentatives

### Scenario 2 — Base de donnees supprimee (30 min)

**Comment simuler :** renommer odooai.db en odooai.db.backup

**Comportement attendu :**
- Le serveur demarre avec une DB vide (create_all)
- Les conversations sont perdues
- Le chat fonctionne (nouvelles conversations)

**Verification :**
- [ ] Serveur demarre sans crash
- [ ] Le chat fonctionne
- [ ] Restaurer : renommer .backup → .db, redemarrer

### Scenario 3 — Odoo instance down (20 min)

**Comment simuler :** couper l'instance Odoo ou mettre une fausse URL

**Comportement attendu (deja OK) :**
- Message "Cannot connect to your Odoo instance"
- Fallback BA Profiles only
- Le chat continue

**Verification :**
- [ ] Message affiche correctement
- [ ] Reponses basees sur BA Profiles

### Scenario 4 — Latence elevee (20 min)

**Comment simuler :** ajouter `await asyncio.sleep(5)` dans le chat endpoint

**Comportement attendu :**
- Le streaming commence apres 5s
- Le loading indicator s'affiche
- L'utilisateur ne voit pas de timeout

**Verification :**
- [ ] Pas de timeout cote frontend
- [ ] Streaming fonctionne apres le delai

## Post-mortem

Apres chaque scenario :
1. Documenter ce qui s'est passe
2. Identifier les ameliorations
3. Creer des issues pour les fixes

## Resultats

*A remplir apres execution*

| Scenario | Resultat | Issues creees |
|----------|---------|---------------|
| 1 — Anthropic down | — | — |
| 2 — DB supprimee | — | — |
| 3 — Odoo down | — | — |
| 4 — Latence | — | — |
