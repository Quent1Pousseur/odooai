# Learning — Observability Engineer (38) — OpenTelemetry + FastAPI
## Date : 2026-03-20
## Duree : 4 heures

## Ce que j'ai appris

### OpenTelemetry pour FastAPI
- OTEL est le standard open pour traces, metriques, logs
- `opentelemetry-instrumentation-fastapi` auto-instrumente les endpoints
- Chaque requete genere un trace ID → suivi bout en bout
- Export vers Jaeger (self-hosted) ou Grafana Tempo (managed)

### Les 3 piliers d'observabilite
1. **Logs** : on a structlog — c'est bien mais pas centralise
2. **Traces** : zero actuellement — on ne peut pas suivre une requete de bout en bout
3. **Metriques** : zero actuellement — pas de latence p50/p95/p99

### Architecture recommandee pour OdooAI
```
FastAPI → OTEL SDK → OTEL Collector → {
  Traces → Jaeger ou Tempo
  Metriques → Prometheus → Grafana
  Logs → Loki → Grafana
}
```

### Metriques cles a instrumenter
- `odooai_chat_latency_seconds` — histogram par domaine
- `odooai_tool_calls_total` — counter par outil
- `odooai_tokens_total` — counter par modele LLM
- `odooai_guardian_blocks_total` — counter de blocages securite
- `odooai_active_conversations` — gauge

## Comment ca s'applique a OdooAI
- Structlog est une bonne base — on peut exporter vers Loki sans refactoring
- OTEL FastAPI middleware = 5 lignes de code pour les traces
- Les metriques LLM (tokens, latence) sont critiques pour le CFO

## Ce que je recommande
1. Sprint 5 : installer `opentelemetry-instrumentation-fastapi`
2. Sprint 5 : ajouter les 5 metriques custom
3. Sprint 6 : deployer Grafana + Prometheus + Loki sur staging

## Sources
- opentelemetry.io/docs/instrumentation/python
- FastAPI + OTEL cookbook
