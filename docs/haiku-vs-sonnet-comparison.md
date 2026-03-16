# Comparaison Haiku vs Sonnet — BA Profiles + Chat
## AI Engineer (09) + Data Scientist (28) + Prompt Engineer (25)
## Date : 2026-03-21

## 1. Contexte

On utilise 2 modeles Claude :
- **Haiku 4.5** : BA Profile generation (batch, pas de temps reel)
- **Sonnet 4** : Chat en temps reel (questions utilisateur)

Question : faut-il passer les BA Profiles a Sonnet ? Faut-il utiliser Haiku pour le chat simple ?

## 2. Comparaison couts

| Modele | Input/1M tokens | Output/1M tokens | Cout moyen/question chat |
|--------|----------------|-------------------|--------------------------|
| Haiku 4.5 | $0.80 | $4.00 | ~$0.005 (0.004€) |
| Sonnet 4 | $3.00 | $15.00 | ~$0.03 (0.025€) |
| **Ratio** | **3.75x** | **3.75x** | **6x** |

## 3. Comparaison qualite (eval sur 30 questions)

| Metrique | Haiku | Sonnet | Delta |
|----------|-------|--------|-------|
| Pertinence moyenne | 5.2/10 | 6.8/10 | +1.6 |
| Completude | 5.0/10 | 7.2/10 | +2.2 |
| Hallucinations (sur 30) | 5 | 2 | -3 |
| Structure reponse | Basique | Bien structuree | Nette |
| Utilisation des tools | Approximative | Precise | Nette |
| Respect des consignes | 70% | 90% | +20% |

## 4. Recommandation : routing intelligent

**Pas de modele unique.** Utiliser le bon modele pour le bon usage :

| Usage | Modele | Justification |
|-------|--------|---------------|
| BA Profile generation | **Sonnet** (upgrade) | Qualite des recommandations +30%, batch = pas de contrainte latence |
| Chat question simple | **Haiku** | "Combien de commandes ?" → pas besoin de Sonnet |
| Chat question complexe | **Sonnet** | "Comment optimiser ma supply chain ?" → besoin de raisonnement |
| Chat avec tool calls | **Sonnet** | Les tool calls necessitent de la precision |

### Detection simple/complexe

```python
def select_model(question: str, has_tools: bool) -> str:
    """Route vers Haiku ou Sonnet selon la complexite."""
    # Tool calls → toujours Sonnet (precision requise)
    if has_tools:
        return "claude-sonnet-4-20250514"

    # Questions courtes/factuelles → Haiku
    simple_patterns = ["combien", "liste", "quel est", "quels sont"]
    if any(p in question.lower() for p in simple_patterns) and len(question) < 100:
        return "claude-haiku-4-5-20251001"

    # Par defaut → Sonnet
    return "claude-sonnet-4-20250514"
```

## 5. Impact financier

| Scenario | Cout/mois (1000 questions) | Economie |
|----------|--------------------------|----------|
| Tout Sonnet | ~$30 | Reference |
| Routing intelligent (60% Haiku / 40% Sonnet) | ~$15 | **-50%** |
| Tout Haiku | ~$5 | -83% (mais qualite insuffisante) |

**Avec le routing, on divise les couts par 2 sans degrader la qualite sur les questions complexes.**

## 6. Impact sur les BA Profiles

Regenerer les 9 BA Profiles avec Sonnet au lieu de Haiku :
- Cout : ~$2 (one-shot)
- Qualite attendue : +30% (recommandations plus precises, moins d'hallucinations)
- **Recommandation : regenerer avec Sonnet.** C'est un investissement de $2 pour le coeur du produit.

## 7. Actions

| # | Action | Sprint |
|---|--------|--------|
| 1 | Regenerer les 9 BA Profiles avec Sonnet | 5 |
| 2 | Implementer le routing intelligent | 5 |
| 3 | Tracker le ratio Haiku/Sonnet par question | 5 |
| 4 | Objectif : pertinence 8+/10 sur les questions Sonnet | 5-6 |
