# Tests de Resilience — Scenarios et Resultats
## Chaos Engineer (31) + AI Engineer (09) + DBA (30)
## Date : 2026-03-21

---

## Test 1 — Anthropic API indisponible (#29)

### Scenario
L'API Anthropic retourne 529 (Overloaded) ou timeout.

### Comportement actuel
- `_call_with_retry` : 2 retries avec backoff (2s, 4s)
- Si echec apres 3 tentatives : `OverloadedError` remonte
- Le chat affiche "Erreur (OverloadedError)" — pas user-friendly

### Comportement cible (Sprint 5)
- Apres 3 echecs : basculer en mode "BA Profile only"
- Message : "Le service IA est temporairement indisponible. Voici ce que nous savons de votre domaine basé sur notre analyse du code source Odoo :"
- Afficher les feature_discoveries du BA Profile pertinent
- L'utilisateur a quand meme de la valeur (degraded mais pas mort)

### Implementation (estimee 2h)
```python
except anthropic.APIStatusError:
    # Fallback: BA Profile only response
    return AgentResponse(
        answer=_build_fallback_response(profile),
        domain=profile.domain_id,
        sources=profile.modules_covered,
    )
```

---

## Test 2 — Base de donnees corrompue (#30)

### Scenario
Le fichier SQLite est corrompu ou supprime.

### Comportement actuel
- `init_db()` cree les tables si elles n'existent pas
- Si le fichier est corrompu : `OperationalError` au demarrage → crash

### Comportement cible (Sprint 5)
- Detecter la corruption : `PRAGMA integrity_check`
- Si corrompu : renommer le fichier en `.corrupted`, creer une nouvelle DB vide
- Logger l'incident
- Le chat fonctionne (conversations perdues mais service actif)

### Implementation (estimee 1h)
```python
async def init_db():
    try:
        # Test integrity
        async with engine.begin() as conn:
            await conn.execute(text("PRAGMA integrity_check"))
    except Exception:
        logger.error("Database corrupted, creating fresh DB")
        Path("odooai.db").rename("odooai.db.corrupted")
        # Recreate
```

---

## Test 3 — Odoo instance down

### Scenario
L'instance Odoo du client ne repond pas.

### Comportement actuel
- Timeout apres 10s → `ConnectionError`
- Le chat affiche "Cannot connect to your Odoo instance"
- Puis continue en mode BA Profiles only ✅

### Verdict : **OK.** Le fallback fonctionne deja.

---

## Test 4 — Redis down (futur)

### Scenario
Redis est indisponible.

### Comportement actuel
Redis n'est pas encore utilise en production. Pas de risque.

### Comportement cible
Quand Redis sera deploye : fallback en memoire (cache local).

---

## Resume

| Test | Status | Fix necessaire | Sprint |
|------|--------|---------------|--------|
| Anthropic down | ⚠️ Partiel (retry OK, fallback manquant) | Fallback BA Profile only | 5 |
| DB corrompue | ❌ Crash | Detect + recreate | 5 |
| Odoo down | ✅ OK | — | — |
| Redis down | N/A | Fallback cache local | Futur |
