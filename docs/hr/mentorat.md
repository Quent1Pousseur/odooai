# Programme de Mentorat — Senior Backend (19) → Junior Backend (20)
## Mis en place par : HR Director (44)
## Date : 2026-03-19
## Duree : Permanente

---

## Contexte

Le Junior Backend (20) a exprime au team building qu'il :
- N'ose pas parler pendant les dailys (rythme trop rapide)
- Se sent sous-utilise (CRUD et tests basiques uniquement)
- Considere le Senior Backend comme "le seul qui prend le temps de reviewer avec des commentaires constructifs"

Le Senior Backend (19) est identifie comme mentor naturel par l'equipe.

## Structure du mentorat

### Daily (15 min)
- **Quand** : 9h00, avant le daily equipe
- **Quoi** : Le Junior montre ce qu'il a fait, pose ses questions, le Senior oriente
- **Regle** : Pas de question bete. Si le Junior ne comprend pas, c'est que c'est mal documente.

### Code review (continu)
- Le Senior review TOUT le code du Junior avec des commentaires pedagogiques
- Pas juste "fix this" → "fix this PARCE QUE [explication du pattern]"
- Le Junior peut demander une review a tout moment (pas besoin d'attendre la PR)

### Pair programming (2x/semaine)
- Le Senior et le Junior codent ensemble sur une tache moyenne
- Objectif : transfert de connaissances sur les patterns, l'architecture, les decisions
- Le Junior code, le Senior guide

### Progression des taches
| Semaine | Type de taches | Autonomie |
|---------|---------------|-----------|
| 1-2 | Tests + schemas + CRUD | Review complete |
| 3-4 | Endpoints API + validation | Review legere |
| 5-8 | Features completes (spec → code → tests) | Autonome + spot check |
| 9+ | Contribution aux specs + review de ses propres PRs | Mentor = backup |

### Slot de parole dans les dailys
- Le Junior a un slot reserve de 2 minutes dans chaque daily
- Il presente ce qu'il a appris, pas juste ce qu'il a fait
- L'equipe encourage les questions (MANIFESTO : le silence est irresponsable)

## Taches assignees au Junior (Sprint 4 — stabilisation)

| # | Tache | Mentor check |
|---|-------|--------------|
| 1 | Ecrire les tests d'integration pour le health endpoint | Senior review |
| 2 | Ajouter des tests pour le domain_validator (edge cases) | Senior review |
| 3 | Documenter les schemas Pydantic avec des docstrings | Senior spot check |
| 4 | Creer des fixtures de test realistes (vrais modules Odoo) | Pair programming |

## Metriques de succes
- Le Junior pose au moins 1 question par daily → il se sent en confiance
- Le Junior soumet au moins 2 PRs par semaine → il contribue
- Le Senior donne du feedback positif + constructif → le Junior progresse
- En 4 semaines : le Junior peut prendre une spec simple de A a Z

## Engagement

**Senior Backend (19)** : "J'accepte ce role. J'aime transmettre et le Junior a du potentiel. Je m'engage a 30min/jour minimum + 2 sessions de pair programming par semaine."

**Junior Backend (20)** : "Merci. C'est exactement ce dont j'avais besoin. Je m'engage a preparer mes questions a l'avance et a ne plus avoir peur de poser des questions 'basiques'."

---

> **Premier check-in mentorat** : 21 mars (vendredi)
> **Review HR** : 2 avril (2 semaines)
