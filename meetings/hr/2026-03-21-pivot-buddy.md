# Meeting d'urgence — Pivot Vision Produit
## Date : 2026-03-21
## Declencheur : Feedback fondateur — "le produit n'est pas ce que je veux"
## Participants : Fondateur (00), CEO (01), CTO (02), CPO (03), AI Eng (09), Prompt Eng (25), UX Designer (27)

---

## Feedback fondateur (verbatim)

"Toutes les reponses sont vagues. L'outil est trop redirige sur le fait de montrer a l'utilisateur comment configurer alors que moi je veux juste que ca soit son buddy de travail et qu'il l'aide au quotidien pour faire tout ce dont il a besoin. Et le chat et l'interface pourraient etre beaucoup plus pousses."

---

## Analyse CPO (03)

"Le fondateur a raison. On a construit un **consultant de configuration** alors qu'il veut un **assistant de travail quotidien**. La difference est enorme :

| Ce qu'on a construit | Ce que le fondateur veut |
|---------------------|------------------------|
| 'Activez la reception 3 etapes' | 'Montre-moi mes commandes en retard' |
| 'Voici comment configurer les relances' | 'Relance les factures impayees de plus de 30 jours' |
| 'Vous n'utilisez pas X' | 'Combien j'ai fait de CA ce mois-ci ?' |
| Recommendations de configuration | Actions quotidiennes concretes |
| Un consultant qu'on consulte | Un collegue qui travaille avec vous |

C'est un **buddy** — pas un consultant. Il aide a FAIRE, pas a CONFIGURER."

## CTO (02)

"Techniquement, le pipeline le supporte deja. Le tool-use peut faire des search_read et read_group sur n'importe quel modele. Le probleme c'est le **prompt** — il est oriente 'recommandation de configuration'. Il suffit de le pivoter vers 'assistant operationnel'."

## AI Eng (09)

"Le system prompt actuel dit 'Presente un DIAGNOSTIC' et 'Pour chaque recommandation...'. C'est le language d'un consultant. Il faut le remplacer par :
- 'Aide l'utilisateur a accomplir sa tache'
- 'Si il pose une question sur ses donnees, reponds avec les donnees'
- 'Si il demande de faire quelque chose, fais-le (en lecture)'
- 'Sois direct, conversationnel, utile'"

## Prompt Eng (25)

"Le few-shot example qu'on a ajoute montre un diagnostic de configuration. C'est contre-productif. Il faut des examples de conversations quotidiennes :
- 'Mes commandes du jour ?' → liste des commandes
- 'Combien de factures impayees ?' → chiffre + liste
- 'Quels produits sont en rupture ?' → liste avec quantites
- 'Resume-moi la semaine' → KPIs cles"

## UX Designer (27)

"L'interface est un chat basique. Pour un buddy de travail, il faudrait :
- Des **quick actions** cliquables (pas juste du texte)
- Un **dashboard** avec les KPIs du jour en entree
- Des **cartes de donnees** au lieu de texte brut
- Un design **chaleureux et professionnel**, pas clinique
- De la **personnalite** — le buddy a un ton, pas un robot"

---

## DECISIONS

| # | Decision | Impact |
|---|----------|--------|
| 1 | **Pivoter le prompt** de consultant → buddy operationnel | Prompt Eng — immediat |
| 2 | **Changer le few-shot** : exemples de taches quotidiennes | Prompt Eng — immediat |
| 3 | **Refondre l'UI** : dashboard + quick actions + cartes | UX + Frontend — Sprint 6 |
| 4 | **Donner une personnalite** au buddy : ton conversationnel, emoji leger, direct | Prompt Eng |
| 5 | **Les BA Profiles restent** — mais comme connaissance interne, pas comme reponse | AI Eng |

---

## Nouvelle vision produit

> **OdooAI n'est pas un consultant. C'est votre collegue le plus competent sur Odoo.**
>
> Il connait votre configuration, vos donnees, vos habitudes. Vous lui parlez comme a un collegue. Il vous aide a faire votre travail, pas a configurer un logiciel.

---

## Actions immediates

| # | Action | Responsable | Quand |
|---|--------|-------------|-------|
| 1 | Recrire le system prompt "buddy mode" | Prompt Eng (25) | Maintenant |
| 2 | Nouveaux few-shot (taches quotidiennes) | Prompt Eng (25) | Maintenant |
| 3 | Maquette nouvelle UI (dashboard + cartes) | UX Designer (27) | Sprint 6 |
| 4 | Tester avec le fondateur | Fondateur | Apres fix prompt |
