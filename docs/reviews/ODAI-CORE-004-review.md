# Review — ODAI-CORE-004 (Connexion Live Odoo dans Chat)

## Reviewer : Security Architect (07)
## Date : 2026-03-17
## Status : APPROVED — 1 LOW corrige

---

## Verdict
**Go.** Credentials securisees, Guardian sur toutes les donnees live, fallback gracieux.

## Points verifies

### Credentials
- API key via getpass (pas visible) ✅
- En memoire seulement (pas de persistance) ✅
- Jamais dans les logs ✅
- Jamais en argument CLI ✅

### Guardian sur donnees live
- `fetch_live_context()` appelle `guarded_odoo_read()` pour chaque requete ✅
- sale.order, stock.picking, account.move — tous guardes ✅
- Hidden fields filtres, SENSITIVE anonymises ✅

### Fallback
- Connexion echoue → chat continue en mode BA Profiles ✅
- Donnees live non-dispo → contexte vide, pas d'erreur ✅

### Error handling
- Exception type leakage corrige → utilise user_message ✅

## Issue corrigee

### LOW-1 : Exception type name dans stderr (CORRIGE)
- **Fichier** : `_cli_odoo.py` ligne 53
- **Avant** : `print(f"Erreur : {type(exc).__name__}")`
- **Apres** : `print(f"Erreur : {exc.user_message}")` avec fallback generique
