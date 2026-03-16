# OdooAI — Checklist Pre-Code

> A suivre AVANT chaque session de developpement. ZERO exception.

## Avant de coder

- [ ] **Daily fait** — standup documente dans `meetings/daily/`
- [ ] **Spec ecrite** — dans `specs/ODAI-XXX-nom.md`, format template
- [ ] **Spec reviewee** — par les reviewers designes
- [ ] **Dependances identifiees** — quelles specs bloquent celle-ci ?
- [ ] **Plan d'action clair** — chaque agent sait quoi faire

## Pendant le dev

- [ ] **Reference spec** — chaque commit commence par `[ODAI-XXX]`
- [ ] **Max 300 lignes/fichier** — splitter si necessaire
- [ ] **Tests ecrits** — pour chaque nouveau composant
- [ ] **mypy --strict** — aucune regression

## Avant de commit

- [ ] **Review documentee** — dans `reviews/ODAI-XXX-review.md`
- [ ] **Issues corrigees** — les high/critical fixes avant commit
- [ ] **make check passe** — ruff + mypy + tests + bandit
- [ ] **Fondateur peut tester** — commande fournie si applicable

## Apres le dev

- [ ] **Daily fin de session** — documente dans `meetings/daily/`
- [ ] **tasks/todo.md mis a jour** — progression visible
- [ ] **Push sur GitHub** — CI verte
