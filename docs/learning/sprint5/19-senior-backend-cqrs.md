# Learning — Senior Backend (19) — CQRS Pattern for Read/Write Separation

## Date : 2026-03-22 (Sprint 5, session 3)
## Duree : 3 heures

## Ce que j'ai appris

1. **CQRS separe les modeles de lecture et d'ecriture** : Command Query Responsibility Segregation utilise des modeles distincts pour les commandes (write) et les queries (read). Les commandes modifient l'etat (CreateConversation, SendMessage), les queries le lisent (GetConversationHistory, ListConnections) sans effet de bord.

2. **Le pattern n'exige pas deux bases de donnees** : La version simple de CQRS utilise une seule base avec des repositories separes. Les write repositories valident les invariants metier et persistent les aggregats. Les read repositories executent des queries optimisees (joins, projections) sans logique metier.

3. **Les commands passent par des handlers dedies** : Chaque commande a un handler qui orchestre la logique : validation, appel au domaine, persistence, emission d'events. Cela rend le code testable unitairement sans toucher a la base. En Python, on peut utiliser un simple dispatcher dict ou une lib comme mediatr-py.

4. **Les read models peuvent etre des vues materialisees** : Pour les queries complexes (dashboard, historique de conversations avec metadata), on peut creer des vues SQL materialisees ou des tables de projection pre-calculees, rafraichies par les events de commande.

5. **CQRS se combine naturellement avec l'architecture hexagonale** : Les ports definissent deja les interfaces. On peut splitter `IConversationRepository` en `IConversationCommandRepo` (save, delete) et `IConversationQueryRepo` (find_by_id, list_by_user, search). Les adapters implementent chaque cote independamment.

## Comment ca s'applique a OdooAI

1. **Separation des flux conversation** : Les commandes (creer conversation, envoyer message, connecter Odoo) passent par un pipeline de validation strict (Security Guardian, sanitization). Les queries (lister conversations, afficher historique) bypasse cette validation et lisent directement des projections optimisees pour le frontend.

2. **Scaling des lectures vs ecritures** : OdooAI aura beaucoup plus de lectures (afficher conversations, consulter analyses) que d'ecritures (envoyer un message, creer une connexion). CQRS permet de scaler les read replicas PostgreSQL independamment sans toucher au write path.

3. **Integration avec le metering** : Les command handlers emettent des events (MessageSent, AnalysisCompleted) qui alimentent le MeteringService. Le flux est unidirectionnel : commande > handler > event > metering. Pas de couplage entre le billing et la logique metier.

## Ce que je recommande

1. **Sprint 6** : Refactorer les services existants en separant commands et queries. Creer `odooai/domain/commands/` et `odooai/domain/queries/` avec des dataclasses typees pour chaque operation.

2. **Sprint 7** : Implementer un `CommandBus` simple (dict de handlers) dans `odooai/services/bus.py`. Chaque handler recoit une commande, execute la logique, retourne un result. Pas de lib externe, le pattern est simple a implementer en Python.

3. **Sprint 8** : Creer des read models optimises pour les endpoints les plus sollicites (liste conversations, dashboard usage). Utiliser des vues SQL ou des projections en cache Redis pour des reponses sub-10ms.

## Sources

1. Martin Fowler, "CQRS" — martinfowler.com (2011, updated 2024)
2. Greg Young, "CQRS and Event Sourcing" — CQRS.nu Documentation (2023)
3. Cosmic Python, "Architecture Patterns with Python" — Harry Percival & Bob Gregory (O'Reilly, 2024)
