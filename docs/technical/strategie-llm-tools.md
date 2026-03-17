# Strategie LLM + Tools — OdooAI

## Vision

Meilleur resultat, moins de tokens. Pre-macher le travail en Python,
le LLM ne fait que le raisonnement final.

---

## Architecture cible

```
User question
  ↓
COUCHE 1 — Pre-traitement Python (0 tokens)
  → Classification de l'intention (lire, creer, modifier, configurer, diagnostiquer)
  → RAG retrieval (3 chunks les plus pertinents)
  → Detection des modeles Odoo concernes (depuis le RAG + keywords)
  → Si connecte : pre-fetch des champs disponibles (cache fields_get)
  ↓
COUCHE 2 — Context assembly (0 tokens)
  → Construire LE BON contexte minimal pour le LLM :
    - Chunks RAG pertinents
    - Champs disponibles sur les modeles detectes
    - Historique conversation (resume si > 6 messages)
    - Modules installes sur l'instance
  ↓
COUCHE 3 — LLM (seul cout en tokens)
  → Prompt minimal (2 lignes)
  → Contexte pre-mache (pas du bruit, juste ce qu'il faut)
  → Tools generiques mais avec descriptions RICHES
  → Le LLM raisonne, pose des questions, execute
  ↓
COUCHE 4 — Post-traitement Python (0 tokens)
  → Formatage de la reponse
  → Detection dashboard/tableaux
  → Mise a jour des metriques
```

## Strategie Tools

### Principe : peu de tools, tres bien decrits

Prodooctivity a 15 tools. On peut faire mieux avec 7 :

| Tool | Couvre | Description riche |
|------|--------|------------------|
| `odoo_schema` | Introspection modeles + champs | 3 modes : list, compact, detailed |
| `odoo_search_read` | Lire des records | Avec pagination, auto-select champs |
| `odoo_read_group` | Stats groupees | Agregation, date grouping |
| `odoo_execute` | TOUT le reste | Create, write, copy, workflow, wizards |
| `odoo_search_count` | Compter | Simple et rapide |
| `odoo_onchange` | Preview sans sauver | Simuler un changement de champ |
| `odoo_inspect` | Snapshot instance | Modules, warehouses, config |

### Les descriptions de tools = le vrai levier

La description du tool `odoo_execute` doit etre un PLAYBOOK complet :
- Comment creer un record (avec exemple)
- Comment modifier (avec exemple)
- Comment faire une transition de workflow (action_confirm, etc.)
- Comment executer un wizard (4 etapes)
- Les pieges a eviter
- Les methodes bloquees

Le LLM n'a PAS besoin d'instructions dans le system prompt.
Il a besoin de BONNES DESCRIPTIONS DE TOOLS.

## Strategie RAG

### Principe : pre-macher le contexte, pas juste retriever

Aujourd'hui : RAG retourne 3 chunks bruts → injectes au LLM.

Demain : RAG retourne 3 chunks → Python les ENRICHIT avec :
- Les champs reels de l'instance (cache fields_get)
- Les modules installes
- Le contexte de la conversation
→ Le LLM recoit un contexte PARFAIT, pas du bruit.

### Pre-processing intelligent

Avant d'envoyer au LLM, Python peut :
1. Detecter si la question concerne des DONNEES ou de la CONFIG
2. Si DONNEES + connecte → pre-identifier le modele + champs
3. Si CONFIG → pre-identifier le menu + les etapes
4. Assembler un contexte minimal et precis

Ca reduit les tokens ET ameliore la precision.

## Strategie Prompt

### 2 lignes. Pas plus.

```
Tu es un assistant Odoo expert. Francais.
Confirme avant toute ecriture.
```

TOUT le reste est dans :
- Les descriptions de tools (comment agir)
- Le contexte RAG (quoi savoir)
- L'historique de conversation (ce qui a ete dit)

### Pourquoi ca marche

Le LLM (Claude Sonnet/Opus) est DEJA expert en :
- Comprendre les questions en francais
- Raisonner sur des donnees structurees
- Utiliser des tools de maniere intelligente
- Poser des questions quand il manque des infos

Il n'a PAS besoin qu'on lui dise COMMENT faire.
Il a besoin qu'on lui donne les OUTILS et la CONNAISSANCE.

## Strategie Tokens

### Objectif : < 0.01€ par question

| Composant | Tokens | Cout |
|-----------|--------|------|
| System prompt | ~50 | negligeable |
| RAG context (3 chunks) | ~300 | negligeable |
| Historique (4 messages) | ~400 | negligeable |
| User question | ~30 | negligeable |
| Tool descriptions (7 tools) | ~2000 | ~$0.006 |
| LLM response | ~500 | ~$0.008 |
| **Total** | **~3300** | **~$0.014** |

Avec le routing Haiku/Sonnet :
- Questions simples (Haiku) : ~$0.003
- Questions complexes (Sonnet) : ~$0.014
- **Moyenne : ~$0.008 par question**

### Optimisations futures

1. **Cache fields_get** — ne pas re-demander les champs a chaque question
2. **Cache RAG** — si la meme question revient, meme contexte
3. **Tool descriptions lazy** — ne charger que les tools pertinents
4. **Resume conversation** — au lieu de 4 messages complets, un resume de 100 tokens

## Plan d'implementation

### Phase 1 — Tools riches (priorite)
Recrire les 7 tools avec des descriptions playbook.
C'est le changement qui a le plus d'impact sur la qualite.

### Phase 2 — Pre-processing intelligent
Ajouter la couche Python qui pre-mache le contexte.
Cache fields_get, detection de modele, enrichissement RAG.

### Phase 3 — Routing Haiku/Sonnet
Activer le routing intelligent deja code.
Questions simples → Haiku (6x moins cher).

### Phase 4 — Optimisation continue
Cache, resume, lazy loading tools.
Monitoring des tokens par question.

---

## Ce qu'on a appris de prodooctivity

1. Les descriptions de tools sont le VRAI levier (pas le prompt)
2. Un seul tool `execute` pour toutes les ecritures
3. Les exemples concrets dans les descriptions changent tout
4. Les pieges documentes evitent 80% des erreurs
5. Le prompt est MINIMAL — 2-3 lignes max
6. Le RAG fournit la connaissance, les tools fournissent les capacites
