# Learning — Chaos Engineer (31) — Failure Mode Analysis for Distributed AI Systems
## Date : 2026-03-22 (Sprint 5, session 4)
## Duree : 3 heures

## Ce que j'ai appris

1. **Les systemes AI distribues ont des failure modes uniques** : au-dela des pannes reseau et disque classiques, un SaaS qui depend d'un LLM externe a des modes de defaillance specifiques : latence API Anthropic (p99 > 30s), rate limiting provider (429), reponses degradees (hallucinations sous charge), et couts explosifs (une boucle de retry peut bruler le budget mensuel en minutes).

2. **FMEA (Failure Mode and Effects Analysis) structure l'analyse** : pour chaque composant, on identifie (a) le mode de defaillance, (b) l'effet sur le systeme, (c) la severite (1-10), (d) la probabilite d'occurrence, (e) la detectabilite. Le Risk Priority Number (RPN = severite x probabilite x detectabilite) priorise les actions. Pour OdooAI, le composant avec le RPN le plus eleve est l'appel Anthropic API : severite 8, probabilite 5, detectabilite 3 → RPN 120.

3. **Le "blast radius" doit etre contenu par design** : Netflix utilise le concept de "bulkhead pattern" — chaque tenant a ses propres limites de ressources. Si un utilisateur OdooAI lance 50 analyses en parallele, ca ne doit pas impacter les autres. Le circuit breaker sur l'API Anthropic doit etre per-tenant, pas global.

4. **Les LLM ont un failure mode "silencieux"** : contrairement a une DB qui retourne une erreur claire, un LLM peut retourner une reponse plausible mais fausse (hallucination). C'est le pire mode de defaillance car il n'est pas detecte par le monitoring classique. Il faut des health checks semantiques, pas juste des HTTP 200.

5. **Chaos Engineering pour les dependances LLM** : injecter des fautes specifiques — (a) latence artificielle sur l'API Anthropic (tester le timeout), (b) reponses tronquees (tester le parsing), (c) erreurs 429 repetees (tester le backoff), (d) reponses valides mais semantiquement incorrectes (tester la validation). Gremlin et Litmus supportent l'injection de fautes HTTP.

## Comment ca s'applique a OdooAI

1. **Construire une matrice FMEA pour les 6 composants critiques** : (a) API Anthropic, (b) connexion Odoo XML-RPC, (c) PostgreSQL, (d) Redis cache, (e) Security Guardian, (f) crypto AES-256-GCM. Chaque composant a 2-3 failure modes avec RPN. Ca donne une roadmap priorisee de resilience.

2. **Implementer le circuit breaker pattern sur l'API Anthropic** : utiliser `tenacity` avec un circuit breaker qui s'ouvre apres 3 erreurs consecutives, half-open apres 60s. Le fallback : retourner un message "L'analyse est temporairement indisponible" plutot que de retry indefiniment et bruler du budget.

3. **Creer un "failure injection framework" leger** : un decorator Python qui simule les pannes en dev/staging. Pas besoin de Gremlin pour le MVP — un simple middleware FastAPI qui intercepte les appels sortants et injecte des fautes selon un fichier de config.

## Ce que je recommande

1. **Sprint 6** : Documenter la matrice FMEA complete des 6 composants dans `docs/reliability/fmea-v1.md`. Identifier les 5 failure modes avec le RPN le plus eleve. Cout : 3h.

2. **Sprint 7** : Implementer le circuit breaker sur `odooai/infrastructure/llm/anthropic_provider.py` avec `tenacity`. Ajouter le fallback gracieux et les metriques (compteur d'ouvertures du circuit). Cout : 4h.

3. **Sprint 8** : Premier "Game Day" interne — simuler une panne Anthropic API pendant 10 minutes en staging. Mesurer le temps de detection, le comportement du circuit breaker, et l'experience utilisateur degradee.

## Sources

1. Netflix — "Chaos Engineering: System Resiliency in Practice" (O'Reilly, 2020) — chapitres 5-6 sur le blast radius
2. Google — "Reliable Machine Learning" (O'Reilly, 2022) — chapitre 8 sur les failure modes des systemes ML
3. AWS — "Building resilient AI/ML workloads" (2025) : https://docs.aws.amazon.com/wellarchitected/latest/machine-learning-lens/resilience.html
