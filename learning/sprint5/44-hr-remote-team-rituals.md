# Learning — HR Director (44) — Remote Team Rituals and Async Communication
## Date : 2026-03-21 (Sprint 5)
## Duree : 3 heures

## Ce que j'ai appris

1. **Les rituels async remplacent les reunions synchrones pour les equipes distribuees** : au lieu d'un standup quotidien en visio, un message structure dans un channel dedie (ce que j'ai fait, ce que je fais, blockers) a 9h locale suffit. Ca respecte les fuseaux horaires et cree un historique searchable.

2. **Le "working out loud" augmente la transparence** : chaque agent/membre partage ses avancees dans un channel public au lieu de travailler en silo. Pour OdooAI avec 44 agents, les EOD reports et les kick-off meetings remplissent deja ce role. La cle est que ces rapports soient consultables par tous, pas juste par le fondateur.

3. **Les rituels sociaux sont indispensables meme en remote** : sans les discussions de couloir, l'equipe perd en cohesion. Des rituels comme "coffee chat aleatoire" (2 personnes random, 15 min, pas de sujet impose), "show & tell" mensuel (chacun montre un truc cool), ou "learning friday" maintiennent le lien humain.

4. **La documentation-as-communication est le pilier de l'async** : chaque decision doit etre ecrite dans un document accessible. Les ADR (Architecture Decision Records), les specs ODAI-XXX, les meeting notes remplissent ce role. La regle : "si ce n'est pas ecrit, ca n'existe pas".

5. **Les outils doivent supporter l'async nativement** : Slack avec threads (pas de messages plats), Notion/GitHub Discussions pour les decisions longues, Loom pour les demos asynchrones. L'erreur classique est d'utiliser des outils synchrones (Zoom, appels) pour des sujets qui pourraient etre un document de 5 paragraphes.

## Comment ca s'applique a OdooAI

1. **Les 44 agents ont deja un bon framework de rituels** : daily meetings, kick-offs, retros, EOD reports. Ce qui manque : un index consultable de toutes les decisions prises. Les meeting notes dans `tasks/` sont un bon debut mais il faudrait un systeme de recherche (GitHub Discussions ou un wiki interne).

2. **Le "challenge actif" entre agents doit etre structure** : le feedback `agents_must_challenge` demande que les agents se challengent. Pour que ca fonctionne en async, chaque spec doit avoir une phase de review explicite ou 2-3 agents designes postent leurs objections dans un thread dedie avant le merge.

3. **L'onboarding d'un nouvel agent doit etre self-service** : quand on ajoute un agent (ou quand un contributeur humain rejoint), il doit pouvoir comprendre le projet en lisant les docs sans demander a personne. Le CLAUDE.md, les specs, et les meeting notes doivent suffire.

## Ce que je recommande

1. **Sprint 6** : Creer un template de "Decision Record" dans `tasks/decisions/` pour formaliser chaque decision architecturale ou business. Format : contexte, options, decision, consequences. Lier chaque decision aux specs ODAI-XXX concernees.

2. **Sprint 7** : Implementer un ritual "Sprint Review Async" : chaque agent poste un Loom de 3 minutes montrant son travail du sprint. Le fondateur review a son rythme au lieu d'une reunion de 2h. Gain : 1h30 par sprint pour le fondateur.

3. **Sprint 8** : Creer un "Onboarding Guide" auto-genere depuis les fichiers CLAUDE.md, les specs actives, et les decisions recentes. Un nouvel agent peut etre operationnel en lisant un seul document de 10 pages au lieu de parcourir 50 fichiers.

## Sources

1. GitLab — "The Remote Playbook" (2025) : https://about.gitlab.com/company/culture/all-remote/guide/
2. Basecamp — "Shape Up: Stop Running in Circles" (2024) : https://basecamp.com/shapeup
3. Loom — "Async Video Communication for Remote Teams" : https://www.loom.com/blog/async-communication
