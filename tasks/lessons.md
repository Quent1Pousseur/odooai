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
