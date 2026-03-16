# OdooAI — Lessons Learned

## Format
```
### [DATE] Titre
**Contexte** : Que s'est-il passe
**Erreur** : Ce qui a mal tourne
**Fix** : Ce qu'on a fait
**Regle** : Ce qu'on fait desormais pour eviter ca
```

## Lessons

### [2026-03-16] Split > Monolithe
**Contexte** : Le client Odoo prodooctivity fait 1553 lignes dans un seul fichier.
**Erreur** : Monolithique = dur a naviguer, tester, reviewer.
**Fix** : Split en 6 fichiers avec responsabilite unique (max 200 lignes chacun).
**Regle** : Si un fichier depasse 200 lignes, chercher un split naturel avant de continuer.

### [2026-03-16] Reference ≠ Copie
**Contexte** : On a etudie prodooctivity en profondeur pour construire OdooAI.
**Erreur** : Copier sans comprendre = heriter des problemes sans les solutions.
**Fix** : On a ameliore le error handling, ajoute le rejet portal, simplifie la signature.
**Regle** : Toujours se demander "comment faire mieux ?" en lisant du code de reference.

### [2026-03-16] mypy --strict des le jour 1
**Contexte** : On a active mypy --strict des le premier commit de code.
**Erreur** : Ajouter mypy apres coup est douloureux et cree du bruit.
**Fix** : L'avoir des le depart force des decisions de typage propres.
**Regle** : Jamais de regression mypy — c'est un cliquet, on ne revient pas en arriere.

### [2026-03-16] Review interne AVANT le commit, pas apres
**Contexte** : SEC-001 livree sans review. Le fondateur a demande une review manuelle.
**Erreur** : 5 failles critiques/high decouvertes apres commit (email domain expose, hidden fields incomplets, M2O name leak, SQL patterns manquants, res.partner pas SENSITIVE).
**Fix** : Corrige dans un commit de hardening separe.
**Regle** : Apres chaque spec implementee, TOUJOURS lancer une review interne (subagent Explore) AVANT le commit final. Ne jamais livrer sans review.

### [2026-03-16] Les agents "en veille" doivent parler
**Contexte** : Le daily v1 etait consensuel. 50% des agents n'ont rien dit.
**Erreur** : Legal n'a pas souleve la question LGPL. AI Safety n'a pas mentionne les disclaimers. i18n n'a pas alerte sur la langue des KG. DBA n'a pas challenge le stockage JSON.
**Fix** : Daily v2 avec 30+ challenges de tous les agents. 14 actions generees. 2 VETOs identifies.
**Regle** : TOUS les agents participent a chaque meeting. Le silence est interdit. Chaque agent avec un VETO pose au minimum 1 question critique.

### [2026-03-16] Validation marche en parallele du dev
**Contexte** : 5 specs techniques livrees, 0 contact PME, 0 interview utilisateur.
**Erreur** : 100% technique, 0% business. On construit sans savoir si le marche veut ce qu'on construit.
**Fix** : Sprint 1 inclut des livrables business (interviews PME, matrice concurrentielle, modele de cout).
**Regle** : Chaque sprint a des objectifs business ET techniques. Jamais l'un sans l'autre.

### [2026-03-16] Kick-off obligatoire a chaque phase/sprint
**Contexte** : Le kick-off general etait bien, mais Sprint 1 a demarre sans kick-off formel.
**Erreur** : Pas de cadrage collectif = pas de visibilite sur les risques et les engagements.
**Fix** : Kick-off Sprint 1 formel avec tous les agents, VETOs identifies, risques documentes.
**Regle** : Chaque phase et chaque sprint commence par un kick-off. C'est ajoute dans WORKFLOW.md.

### [2026-03-17] Les meetings ne sont PAS optionnels
**Contexte** : Le fondateur a du rappeler 3 fois que les meetings etaient oublies.
**Erreur** : L'empressement de coder fait sauter les meetings. On perd le cadrage, les challenges, et les decisions collectives.
**Fix** : Regle absolue ajoutee au workflow.
**Regle** : Jamais de code sans daily avant. Jamais de fin de session sans daily apres. Non-negociable.

### [2026-03-17] RIEN ne se code sans spec — ZERO exception
**Contexte** : ODAI-DATA-002 et ODAI-AGENT-001 ont ete codes sans spec. Les reviews ont ete faites par subagent et sont invisibles au fondateur.
**Erreur** : La regle d'or du WORKFLOW ("RIEN ne se code sans spec") a ete violee 2 fois. Les reviews etaient cachees dans les subagents, le fondateur ne pouvait pas les voir ni remonter une mauvaise decision.
**Fix** : Specs retroactives ecrites pour DATA-002 et AGENT-001 (avec mention de l'erreur). Reviews documentees dans `reviews/`. Memoire permanente ajoutee.
**Regle** : 1) Spec dans `specs/` AVANT de coder. 2) Review dans `reviews/` (fichier, pas subagent invisible). 3) Le fondateur peut tout tracer. ZERO exception, ZERO raccourci.
