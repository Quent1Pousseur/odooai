# OdooAI — OKRs (Objectives & Key Results)

## Principe

Chaque trimestre, l'equipe a des objectifs clairs et mesurables. Pas des voeux pieux — des chiffres. Si on ne peut pas le mesurer, ce n'est pas un objectif.

**Responsable OKRs** : CEO (01) definit, PM (04) suit, tout le monde execute.
**Cadence** : Revus chaque semaine au weekly recap, notes au trimestre.
**Grading** : 0.0 (rate) → 0.3 (progres) → 0.7 (objectif atteint) → 1.0 (depasse)

---

## Q2 2026 (Avril - Juin) — A DEFINIR AU KICK-OFF

### Template

```markdown
## OBJECTIF 1 : [Titre]
Owner : [Agent responsable]
Pourquoi : [Contexte]

| Key Result | Cible | Actuel | Score |
|-----------|-------|--------|-------|
| KR1 : [mesurable] | [chiffre] | [chiffre] | [0.0-1.0] |
| KR2 : [mesurable] | [chiffre] | [chiffre] | [0.0-1.0] |
| KR3 : [mesurable] | [chiffre] | [chiffre] | [0.0-1.0] |

Score moyen : [X.X]
```

### Exemples d'OKRs pour le kick-off (a valider par l'equipe)

```markdown
## OBJECTIF 1 : Prouver que le Code Analyst + BA Factory fonctionnent
Owner : AI Engineer (09) + Data Engineer (11)

| Key Result | Cible |
|-----------|-------|
| KR1 : Knowledge Graphs generes pour N modules Odoo 17 | 10 modules |
| KR2 : BA Profiles valides par l'Odoo Expert | 5 domaines |
| KR3 : Expert Profiles avec recettes executables testees | 20 recettes |

## OBJECTIF 2 : Avoir un MVP fonctionnel connecte a une instance Odoo
Owner : CTO (02) + Backend Architect (08)

| Key Result | Cible |
|-----------|-------|
| KR1 : Connexion Odoo (XML-RPC + JSON-RPC) fonctionnelle | 2 protocoles |
| KR2 : CRUD complet avec double validation | 4 operations |
| KR3 : Pipeline de securite (anonymisation + audit) operationnel | 100% |

## OBJECTIF 3 : Valider la proposition de valeur aupres de 10 PME
Owner : Sales (05) + CPO (03)

| Key Result | Cible |
|-----------|-------|
| KR1 : Interviews de decouverte avec des PME utilisatrices d'Odoo | 10 interviews |
| KR2 : Demo du MVP a des prospects | 5 demos |
| KR3 : Lettres d'intention ou pre-inscriptions | 3 LOI |

## OBJECTIF 4 : Infrastructure prete pour le lancement
Owner : Infra Engineer (12) + DevOps (22)

| Key Result | Cible |
|-----------|-------|
| KR1 : CI/CD pipeline complet (lint → test → deploy) | 100% |
| KR2 : Monitoring et alerting operationnel | 5 dashboards |
| KR3 : Temps de deploy staging < 5 minutes | < 5 min |
```

---

## Suivi

- **Chaque lundi** : le PM met a jour les chiffres "Actuel" dans ce document
- **Chaque weekly recap** : status des OKRs inclus dans le recap
- **Fin de trimestre** : scoring final, retrospective, nouveaux OKRs definis
