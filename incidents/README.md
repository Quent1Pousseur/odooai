# OdooAI — Incident Post-Mortems

## Principe

Chaque incident de production est documente ici. Sans exception. On ne blame personne — on corrige le systeme pour que ca n'arrive plus.

## Format

Chaque post-mortem : `INC-XXX-YYYY-MM-DD-titre.md`

```markdown
# INC-XXX — [Titre]

## Severite : SEV1 (critique) | SEV2 (majeur) | SEV3 (mineur)
## Date : [YYYY-MM-DD HH:MM - HH:MM] (debut - fin)
## Duree : [X heures Y minutes]
## Impact : [nombre de clients affectes, fonctionnalites impactees]

## Timeline
| Heure | Evenement |
|-------|-----------|
| HH:MM | [premier signal] |
| HH:MM | [detection] |
| HH:MM | [premiere action] |
| HH:MM | [resolution] |
| HH:MM | [confirmation retour a la normale] |

## Root Cause
[Explication technique de la cause racine]

## Impact
[Details de l'impact : clients, revenue, reputation]

## Resolution
[Ce qui a ete fait pour resoudre]

## Actions Correctives (pour que ca n'arrive plus)
| Action | Owner | Deadline | Status |
|--------|-------|----------|--------|
| [action] | [agent] | [date] | OUVERT/FERME |

## Lecons Apprises
[Ce qu'on a appris de cet incident]
```

## Index

| INC | Date | Severite | Titre | Duree | Status |
|-----|------|----------|-------|-------|--------|
| (a remplir) | | | | | |
