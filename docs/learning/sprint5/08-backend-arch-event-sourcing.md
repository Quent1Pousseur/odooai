# Learning — Backend Arch (08) — Event Sourcing for Action Flow Tracking

## Date : 2026-03-22 (Sprint 5, session 3)
## Duree : 3 heures

## Ce que j'ai appris

1. **Event sourcing stocke les faits, pas l'etat courant** : Au lieu de persister l'etat final d'une entite (ex. `conversation.status = "closed"`), on stocke la sequence ordonnee d'events : ConversationCreated, MessageSent, AnalysisRequested, ConversationClosed. L'etat courant se reconstruit en rejouant les events (fold/reduce).

2. **L'event store est append-only et immutable** : Chaque event a un `sequence_number`, un `timestamp`, un `aggregate_id` et un `payload` JSON. On n'update jamais, on n'efface jamais. Cela donne un audit trail complet gratuitement. En PostgreSQL, une table `events` avec un index sur `(aggregate_id, sequence_number)` suffit.

3. **Les snapshots evitent le replay complet** : Pour les aggregats avec beaucoup d'events (conversations longues avec 200+ messages), on persiste un snapshot de l'etat tous les N events. Au chargement, on part du dernier snapshot + events suivants. Cela garantit des temps de reconstruction sub-50ms meme pour les gros aggregats.

4. **Les projections construisent des vues optimisees** : Des processeurs ecoutent le stream d'events et maintiennent des tables de lecture. Par exemple, une projection `conversation_summary` aggrege les events pour fournir une vue avec nombre de messages, derniere activite, statut — sans rejouer l'historique a chaque requete.

5. **Event sourcing se combine avec CQRS** : Les commandes produisent des events (write side), les projections les consomment pour alimenter des read models (read side). Le decoupage est naturel : le domain emet, les projections reagissent.

## Comment ca s'applique a OdooAI

1. **Tracking complet des actions utilisateur** : Chaque interaction avec l'assistant (message envoye, outil appele, analyse Odoo lancee, champ explore) devient un event. On peut reconstruire exactement ce que l'utilisateur a fait, dans quel ordre, et pourquoi. C'est critique pour le debugging des conversations complexes et le metering.

2. **Replay pour analyse et optimisation** : En rejouant les events d'une conversation, on peut analyser les patterns d'usage : quels modules sont explores en premier, combien de tool calls par question, quels champs sont les plus demandes. Ces donnees alimentent le scoring de pertinence des Knowledge Graphs.

3. **Audit trail pour la securite** : Le Security Guardian a besoin de tracer chaque acces aux donnees Odoo du client. L'event store fournit un log immutable et complet de toutes les operations, sans ajouter de code d'audit dans chaque service.

## Ce que je recommande

1. **Sprint 7** : Implementer un event store minimal dans `odooai/infrastructure/db/event_store.py`. Table `domain_events` avec colonnes `id`, `aggregate_type`, `aggregate_id`, `event_type`, `payload`, `sequence`, `created_at`. Interface `IEventStore` dans les ports.

2. **Sprint 8** : Creer les events du domaine conversation : `ConversationCreated`, `MessageSent`, `ToolCallExecuted`, `AnalysisCompleted`. Les emettre depuis les command handlers existants. Ajouter une projection basique pour le dashboard.

3. **Sprint 9** : Ajouter le mecanisme de snapshots pour les conversations longues. Seuil a 100 events par aggregat. Benchmark replay vs snapshot pour valider les gains de performance.

## Sources

1. Greg Young, "Event Sourcing" — eventstoredb.com Documentation (2024)
2. Martin Fowler, "Event Sourcing" — martinfowler.com (2005, updated 2023)
3. Cosmic Python, "Architecture Patterns with Python" — Harry Percival & Bob Gregory, Chapters 8-11 (O'Reilly, 2024)
