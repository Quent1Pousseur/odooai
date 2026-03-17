# Meeting Urgence — Qualite des Reponses
## Date : 2026-03-22
## Participants : Fondateur (00), AI Eng (09), Prompt Eng (25), Odoo Expert (10), Data Eng (11)
## Declencheur : "Les reponses ne sont pas convaincantes"

---

## Feedback fondateur

"Les prompts et les resultats ne sont pas convaincants. Le probleme vient peut-etre de l'input — les BA Profiles et les KG ne sont pas assez riches. On doit ameliorer le scrapping du code source ET les prompts."

---

## Diagnostic AI Eng (09)

"Le pipeline a 3 maillons. Le probleme peut venir de chacun :

```
KG (input) → BA Profile (contexte) → Prompt + LLM (output)
```

Analysons chaque maillon :"

### Maillon 1 — Knowledge Graphs (Data Eng 11)

**Ce qu'on capture :**
- Noms de modeles, champs, types ✅
- Contraintes SQL et Python ✅
- Vues XML (form, tree, kanban) ✅
- Menus et actions ✅
- ACLs et record rules ✅

**Ce qu'on NE capture PAS :**
- Les **workflows/transitions** (draft → confirmed → done) ❌
- Les **methodes compute** (la logique business) ❌
- Les **onchange** (ce qui se passe quand on change un champ) ❌
- Les **actions serveur** et automatisations ❌
- Les **rapports** (QWeb templates) ❌
- Les **relations entre modules** (comment sale depend de stock) ❌
- Les **valeurs par defaut** des champs ❌
- Les **groupes de securite** et qui a acces a quoi ❌

**Impact** : le LLM sait ce qui EXISTE mais pas comment ca FONCTIONNE.

### Maillon 2 — BA Profiles (Prompt Eng 25)

**Ce qu'on genere :**
- Summary du domaine ✅
- Capabilities (ce que le domaine peut faire) ✅
- Feature discoveries (fonctionnalites peu connues) ✅
- Gotchas (pieges) ✅

**Ce qu'on NE genere PAS :**
- Les **workflows typiques** (comment un devis devient une facture) ❌
- Les **best practices** par taille d'entreprise ❌
- Les **interdependances** entre modules ❌
- Les **questions frequentes** avec reponses types ❌
- Les **configurations recommandees** par secteur ❌

**Impact** : le contexte est generique, pas actionnable.

### Maillon 3 — Prompt + LLM (AI Eng 09)

**Problemes identifies :**
- Le LLM genere du faux XML au lieu d'utiliser les tools ❌ (fixe mais revient)
- Sans connexion Odoo, les reponses sont vagues car le contexte BA est generique
- Avec connexion, les tool calls sont parfois sur les mauvais modeles
- Le LLM ne sait pas quels champs demander — il tire au hasard

---

## Odoo Expert (10)

"Le vrai probleme c'est le Maillon 1. Les KG sont des listes de champs. C'est comme avoir un dictionnaire sans grammaire. Le LLM sait que `sale.order` a un champ `state` mais il ne sait pas que :

- `state` passe par draft → sent → sale → done
- Quand on confirme, ca cree un `stock.picking`
- Le `stock.picking` genere un `account.move` a la livraison
- Les conditions de paiement determinent la date d'echeance

C'est cette connaissance qui rend les reponses utiles. Sans ca, le LLM ne peut que lister des champs."

---

## Plan d'action — 2 pistes

### Piste A — Enrichir les KG (Maillon 1)

**A ajouter au Code Analyst :**

| Element | Comment le parser | Impact |
|---------|------------------|--------|
| Workflows (state transitions) | Chercher `state = fields.Selection` + methodes `action_*` qui changent le state | Le LLM comprend le cycle de vie |
| Methodes compute | Parser le corps des `@api.depends` + `_compute_*` | Le LLM sait comment les champs sont calcules |
| Onchange | Parser `@api.onchange` | Le LLM sait les effets de bord |
| Relations inter-modules | Analyser les `_inherit` cross-module + les champs relationnels | Le LLM voit le systeme complet |
| Valeurs par defaut | Parser `default=` dans les champs | Le LLM connait la config initiale |
| Groupes de securite | Parser les `groups=` dans les vues et champs | Le LLM sait qui peut faire quoi |

**Effort** : M (3-5 jours) — c'est du parsing Python AST supplementaire
**Responsable** : Data Eng (11) + Odoo Expert (10)

### Piste B — Enrichir les BA Profiles (Maillon 2)

**Nouveau prompt pour la generation BA :**

Au lieu de generer un resume generique, generer :
1. **Workflows detailles** : "Un devis suit ce parcours : draft → envoi → confirmation → livraison → facturation"
2. **Questions/Reponses types** : "Q: Comment voir mes commandes en retard ? R: sale.order avec commitment_date < aujourd'hui"
3. **Configurations recommandees** : "Pour une PME de 20-50 employes, activer : reception 3 etapes, relances auto, pricelists"
4. **Interdependances** : "Le module sale cree des stock.picking qui generent des account.move"
5. **Champs cles par use case** : "Pour le reporting ventes : amount_total, date_order, partner_id, state, user_id"

**Effort** : S (1-2 jours) — c'est un changement de prompt de generation
**Responsable** : Prompt Eng (25) + AI Eng (09)

---

## Decisions

| # | Decision | Prio | Responsable | Sprint |
|---|----------|------|-------------|--------|
| 1 | **Piste B d'abord** — enrichir les BA Profiles (rapide, gros impact) | P0 | Prompt Eng + AI Eng | Maintenant |
| 2 | **Piste A ensuite** — enrichir les KG (plus long mais fondamental) | P1 | Data Eng + Odoo Expert | Sprint 6 |
| 3 | **Regenerer les BA** apres chaque amelioration et eval sur 10 questions | P0 | Data Scientist | Apres chaque fix |
| 4 | **Le prompt chat reste** — le probleme n'est pas le prompt de chat mais l'input | — | AI Eng | — |

---

## Fondateur

"On commence par la Piste B. Si les BA Profiles sont meilleurs, les reponses seront meilleures meme sans toucher au code du parseur. Ensuite Sprint 6 on enrichit les KG pour la couche fondamentale."

---

> "Le LLM n'est aussi bon que ce qu'on lui donne. Garbage in, garbage out." — AI Eng (09)
