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
