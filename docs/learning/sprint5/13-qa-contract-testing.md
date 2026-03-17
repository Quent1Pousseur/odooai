# Learning — QA Lead (13) — Contract Testing for API Endpoints

## Date : 2026-03-22 (Sprint 5, session 3)
## Duree : 3 heures

## Ce que j'ai appris

1. **Contract testing verifie les interfaces, pas l'implementation** : Contrairement aux tests d'integration qui testent le comportement complet, le contract testing valide que le producer (backend FastAPI) et le consumer (frontend Next.js) s'accordent sur la forme des requetes et reponses (schemas, status codes, headers).

2. **Pact est le standard open-source** : Pact permet au consumer de definir ses attentes (un "pact"), puis le producer verifie qu'il les respecte. En Python, pact-python s'integre avec pytest. Cote Next.js, pact-js genere les contrats depuis les tests Vitest.

3. **Schema-first avec OpenAPI comme source de verite** : FastAPI genere automatiquement un schema OpenAPI depuis les modeles Pydantic. Ce schema peut servir de contrat. Des outils comme Schemathesis generent automatiquement des tests fuzz depuis ce schema pour detecter les violations.

4. **Les breaking changes sont detectes avant le merge** : En CI, on compare le schema OpenAPI du PR avec celui de main. Toute suppression de champ, changement de type ou modification de status code est flaggee comme breaking change. Cela empeche les regressions API.

5. **Contract testing pour les providers externes** : OdooAI depend de l'API Anthropic et du XML-RPC Odoo. On peut creer des contrats pour ces providers externes, verifies contre des stubs, pour detecter si un changement upstream casse notre integration.

## Comment ca s'applique a OdooAI

1. **Consumer-driven contracts frontend/backend** : Le frontend Next.js definit exactement ce qu'il attend de chaque endpoint (`/api/v1/conversations`, `/api/v1/connections`). Le backend verifie ces contrats a chaque PR. Si le backend change un champ, le test echoue avant le deploy.

2. **Protection de l'interface ILLMProvider** : Le port `domain/ports/ILLMProvider` definit un contrat interne. Les contract tests verifient que `infrastructure/llm/anthropic_provider.py` respecte ce contrat, et que tout nouveau provider (OpenAI, Mistral) le respecte aussi.

3. **Schema OpenAPI comme artefact CI** : FastAPI genere deja le schema. On ajoute un step CI qui exporte `/openapi.json`, le compare au schema commit precedent, et bloque si breaking change sans bump de version.

## Ce que je recommande

1. **Sprint 6** : Installer Schemathesis et ajouter un job CI qui fuzz tous les endpoints FastAPI depuis le schema OpenAPI genere. Objectif : 0 violation de schema, 0 crash sur input aleatoire.

2. **Sprint 7** : Implementer pact-python cote backend et pact-js cote frontend pour les 5 endpoints principaux (health, conversations, connections, messages, usage). Les contrats sont versionnes dans `tests/contracts/`.

3. **Sprint 8** : Ajouter un diff OpenAPI automatique dans le pipeline CI (outil oasdiff) qui bloque les PR avec breaking changes non-intentionnels et genere un changelog API.

## Sources

1. Pact Documentation — Contract Testing for Microservices (2025)
2. Schemathesis — Property-Based Testing for OpenAPI (GitHub, 2025)
3. SmartBear, "Consumer-Driven Contract Testing in Practice" (2024)
