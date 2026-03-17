# Learning — SaaS Architect (06) — Usage-Based Pricing Models for AI SaaS

## Date : 2026-03-22 (Sprint 5, session 3)
## Duree : 3 heures

## Ce que j'ai appris

1. **Token-based metering est le standard AI SaaS** : Les plateformes comme OpenAI, Anthropic et Cohere facturent au token consomme. Pour OdooAI, chaque requete agent consomme des tokens Claude (Haiku/Sonnet/Opus) avec des couts tres differents. Le metering doit capturer le modele utilise, pas juste le volume brut.

2. **Hybrid pricing surpasse le pure usage-based** : Les SaaS les plus performants (Snowflake, Datadog) combinent un abonnement de base (acces plateforme, connexions Odoo) avec une couche usage-based (tokens LLM, analyses). Cela garantit un MRR previsible tout en capturant la valeur des gros utilisateurs.

3. **Credit systems simplifient la facturation** : Plutot que de facturer les tokens bruts (incomprehensible pour un CFO), on abstrait en "credits OdooAI". 1 credit = 1 analyse simple (Haiku). Une analyse complexe (Opus) = 10 credits. Le client achete des packs de credits ou un quota mensuel.

4. **Rate limiting et cost capping sont critiques** : Sans plafond, un utilisateur peut generer des milliers d'euros de tokens en une journee. Il faut implementer des soft limits (alerte a 80%) et hard limits (blocage a 100%) par tenant.

5. **Granularite du metering impacte la confiance** : Les clients enterprise exigent un detail par conversation, par agent, par connexion Odoo. Le systeme de metering doit logger chaque appel LLM avec son cout reel pour permettre un billing transparent.

## Comment ca s'applique a OdooAI

1. **Architecture de metering dans le middleware** : Chaque appel a `ILLMProvider` doit emettre un evenement de metering (tenant_id, model, input_tokens, output_tokens, timestamp). Ce flux alimente a la fois le billing et le dashboard usage du client.

2. **Plans alignes sur les decisions fondateur** : Le plan Free (1 connexion, Haiku only, 100 credits/mois), Pro (3 connexions, Sonnet, 1000 credits), Enterprise (illimite, Opus, credits custom) respecte la strategie de gate pricing deja validee.

3. **Cost control par agent** : Chaque agent (Code Analyst, Business Advisor) a un budget token configurable. Le Security Guardian (zero LLM) ne consomme aucun credit, ce qui est un argument commercial fort.

## Ce que je recommande

1. **Sprint 6** : Implementer un `MeteringService` dans `odooai/services/` qui intercepte tous les appels LLM et persiste les events dans une table `usage_events` (async, non-bloquant).

2. **Sprint 7** : Creer un endpoint `/api/v1/usage` exposant la consommation par periode, par agent, par connexion. Le frontend affichera un dashboard usage temps reel.

3. **Sprint 8** : Integrer Stripe Billing avec metered subscriptions pour automatiser la facturation usage-based sans code custom de billing.

## Sources

1. OpenAI Platform — Usage-based pricing documentation (2025)
2. Kyle Poyar, "The Guide to Usage-Based Pricing" — OpenView Partners (2024)
3. Stripe Documentation — Metered Billing with Subscriptions (2025)
