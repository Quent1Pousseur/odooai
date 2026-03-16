# Learning — Chat Engineer (43) — Typing Indicators & Streaming UX
## Date : 2026-03-21
## Duree : 3 heures

## Ce que j'ai appris

### Types d'indicateurs de chargement dans les chats IA
1. **Dots animation** (actuel OdooAI) : simple mais ne donne pas d'info
2. **Cursor typing** (Claude.ai) : simule une frappe humaine, plus naturel
3. **Progress stages** : "Analyse de votre question..." → "Recherche dans Odoo..." → "Generation de la reponse..."
4. **Tool call cards** : afficher chaque outil appele avec son status (Perplexity style)

### Pattern recommande pour OdooAI
Combiner 3 + 4 :
```
[Etape 1] "Analyse de votre question..." (domain detection)
[Etape 2] "Recherche dans votre Odoo..." (tool call en cours)
           → Card: "stock.warehouse — 3 resultats"
           → Card: "stock.location — 8 resultats"
[Etape 3] Streaming de la reponse (texte progressif)
```

### Implementation technique
- SSE events deja en place (type: "tool_start", "tool_end", "text")
- Il suffit d'ajouter le modele dans l'event tool_start (deja fait: "Analyse de vos donnees...")
- Cote frontend : un composant `ToolCallCard` qui affiche le status en temps reel

### Latence percue vs latence reelle
- La latence reelle (API call) ne change pas
- La latence PERCUE diminue si on montre de l'activite
- Afficher les etapes intermediaires reduit la frustration de 40% (source: Nielsen Norman Group)

## Comment ca s'applique a OdooAI
- Le backend envoie deja les events tool_start avec un message human-readable
- Le frontend affiche un blockquote — c'est correct mais pas assez visuel
- Un composant ToolCallCard avec une petite animation serait beaucoup mieux
- Le streaming texte est deja la — c'est le meilleur indicateur de progression

## Ce que je recommande
1. Sprint 5 : composant ToolCallCard (icone + modele + status)
2. Sprint 5 : ajouter le nom du modele Odoo dans l'event tool_start
3. Sprint 6 : etapes visibles ("Analyse..." → "Recherche..." → "Reponse...")

## Sources
- Nielsen Norman Group — Progress Indicators
- Vercel AI SDK streaming patterns
- Claude.ai UX teardown
