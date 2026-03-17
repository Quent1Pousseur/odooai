# Learning — PM (04) — GitHub Projects Workflow for Sprint Tracking
## Date : 2026-03-21 (Sprint 5)
## Duree : 3 heures

## Ce que j'ai appris

1. **GitHub Projects V2 utilise des champs custom typees** : on peut creer des champs "Sprint", "Story Points", "Priority" directement dans le board. Les vues (Board, Table, Roadmap) filtrent sur ces champs, ce qui remplace Jira pour les equipes < 20 personnes.

2. **Les automations natives sont limitees mais suffisantes** : auto-move quand un PR est merged, auto-archive apres 14 jours done, auto-assign quand un issue passe "In Progress". Pour le reste, GitHub Actions + l'API GraphQL Projects V2 couvrent les gaps.

3. **Le workflow ideal pour un SaaS early-stage** : Backlog > Sprint Ready > In Progress > In Review > Done. Pas de colonne "QA" separee — les checks CI remplacent le QA manuel. Les labels ODAI-XXX s'integrent directement comme filtre de vue.

4. **Les iterations (sprints) sont un type de champ natif** : on definit la duree (1 semaine pour nous), et GitHub genere automatiquement les sprints suivants. Le burndown chart est disponible via Insights sans config supplementaire.

5. **L'API GraphQL permet de scripter la creation d'issues** : on peut generer les tickets de sprint depuis un fichier YAML ou depuis les specs ODAI, ce qui automatise le kick-off meeting.

## Comment ca s'applique a OdooAI

1. **Migration du tracking depuis tasks/todo.md vers GitHub Projects** : aujourd'hui on track dans des fichiers markdown. Migrer vers Projects V2 donne de la visibilite au fondateur sans qu'il lise le repo. Les specs ODAI-XXX deviennent des issues liees aux PRs.

2. **Sprint ceremonies automatisees** : un workflow GitHub Actions peut generer le sprint report (velocity, burndown) et le poster dans un issue "Sprint 6 Retro" automatiquement. Ca s'aligne avec la regle meetings_mandatory.

3. **Tracking multi-domaine** : avec les labels CORE, SEC, AGENT, API, UI, DATA, INFRA, BIZ, chaque agent voit son scope filtre. Le PM a la vue globale cross-domaine.

## Ce que je recommande

1. **Sprint 6** : Creer le GitHub Project OdooAI avec les champs Sprint, Domain (ODAI-XXX), Story Points. Migrer les 10 specs actives en issues. Cout : 2h de setup.

2. **Sprint 7** : Ajouter un workflow GitHub Actions qui genere le sprint summary automatiquement a chaque fin de sprint (dimanche soir). Template dans `.github/workflows/sprint-report.yml`.

3. **Sprint 8** : Scripter la creation d'issues depuis les fichiers de specs agents/ pour que chaque kick-off genere automatiquement le board du sprint.

## Sources

1. GitHub Docs — "Planning and tracking with Projects" (2025) : https://docs.github.com/en/issues/planning-and-tracking-with-projects
2. GitHub Blog — "Projects V2 API and Automations" (2025) : https://github.blog/changelog/label/projects/
3. Martin Fowler — "Agile Project Management for Small Teams" (2024) : https://martinfowler.com/articles/agile-small-teams.html
