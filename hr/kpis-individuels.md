# KPIs Individuels — 48 agents OdooAI
## Mis a jour : chaque fin de sprint
## Responsable verification : HR Director (44) + PM (04)

---

## C-Suite

### 01 CEO
| KPI | Cible | Mesure |
|-----|-------|--------|
| Decisions strategiques documentees | 3+/sprint | decisions/ folder count |
| Taux de participation aux meetings obligatoires | 100% | meetings/ logs |
| Blockers resolus en <24h | 90%+ | tasks/todo.md timestamps |

### 02 CTO
| KPI | Cible | Mesure |
|-----|-------|--------|
| Architecture Decision Records (ADR) produits | 2+/sprint | docs/adr/ folder count |
| Dette technique identifiee et planifiee | 100% items tracked | tasks/tech-debt.md |
| Revues techniques effectuees | 5+/sprint | PR review count |

### 03 CPO
| KPI | Cible | Mesure |
|-----|-------|--------|
| Specs validees et livrees dans le sprint | 80%+ | specs/ folder vs sprint plan |
| User stories avec criteres d'acceptation | 100% | specs/ file audit |
| Feedback utilisateur integre | 3+ items/sprint | changelog entries |

### 04 PM
| KPI | Cible | Mesure |
|-----|-------|--------|
| Taux de completion du sprint | 85%+ | tasks/todo.md done vs planned |
| Meetings facilites dans les temps | 100% | meetings/ folder timestamps |
| Blockers escalades en <4h | 95%+ | slack/meetings logs |

---

## Sales & Business

### 05 Sales
| KPI | Cible | Mesure |
|-----|-------|--------|
| Leads qualifies documentes | 5+/sprint | sales/ pipeline docs |
| Demos planifiees | 2+/sprint | calendar entries |
| Taux conversion lead-to-trial | 20%+ | sales/ metrics |

### 15 CFO
| KPI | Cible | Mesure |
|-----|-------|--------|
| Budget tracking mis a jour | 1x/sprint | finance/ reports |
| Ecart budget prevu vs reel | <10% | finance/ variance report |
| Projections MRR documentees | 1/sprint | finance/ forecasts |

### 16 Legal
| KPI | Cible | Mesure |
|-----|-------|--------|
| Contrats/CGV revus | 100% des demandes | legal/ folder |
| Compliance GDPR checkpoints | 2/sprint | legal/gdpr-audit.md |
| Risques juridiques documentes | 100% identified | legal/risks.md |

### 32 BizDev
| KPI | Cible | Mesure |
|-----|-------|--------|
| Partenariats identifies et documentes | 3+/sprint | bizdev/ pipeline |
| Outreach envoyes | 10+/sprint | bizdev/ outreach log |
| Partnerships en negociation active | 2+ ongoing | bizdev/ status tracker |

### 40 Vendor Mgr
| KPI | Cible | Mesure |
|-----|-------|--------|
| Couts API/infra optimises | 5%+ reduction/quarter | finance/ vendor reports |
| Contrats vendeurs revus | 100% avant expiration | vendor/ folder |
| SLA vendeurs respectes | 99%+ | vendor/ SLA tracker |

---

## Architecture

### 06 SaaS Arch
| KPI | Cible | Mesure |
|-----|-------|--------|
| Patterns multi-tenant documentes | 2+/sprint | docs/architecture/ |
| Latence API p95 | <500ms | monitoring dashboards |
| Scalability tests executes | 1+/sprint | tests/load/ results |

### 07 Security Arch
| KPI | Cible | Mesure |
|-----|-------|--------|
| Threat models mis a jour | 1+/sprint | security/threat-models/ |
| Vulnerabilites critiques ouvertes | 0 | bandit + audit reports |
| Security reviews sur PRs sensibles | 100% | PR review logs |

### 08 Backend Arch
| KPI | Cible | Mesure |
|-----|-------|--------|
| Coherence hexagonale (violations) | 0 violations | ruff + architecture linter |
| Code review turnaround | <4h | PR timestamps |
| Patterns documentes et appliques | 100% | docs/patterns/ |

---

## Engineering — AI & Data

### 09 AI Eng
| KPI | Cible | Mesure |
|-----|-------|--------|
| Token cost par requete moyenne | <$0.05 | LLM usage logs |
| Accuracy des reponses agent | 90%+ | eval/ benchmark suite |
| Nouveaux prompts testes et valides | 3+/sprint | prompts/ versioning |

### 10 Odoo Expert
| KPI | Cible | Mesure |
|-----|-------|--------|
| Modules Odoo couverts dans knowledge store | +50/sprint | knowledge_store/ count |
| Precision mapping models/fields | 99%+ | tests/knowledge/ results |
| Questions Odoo resolues pour l'equipe | 5+/sprint | slack/meetings logs |

### 11 Data Eng
| KPI | Cible | Mesure |
|-----|-------|--------|
| Pipelines data operationnels | 100% uptime | monitoring alerts |
| Knowledge graphs generes/mis a jour | 10+/sprint | knowledge_store/ diffs |
| Data quality score | 98%+ | tests/data/ validation |

### 25 Prompt Eng
| KPI | Cible | Mesure |
|-----|-------|--------|
| Prompts optimises (token reduction) | 10%+ reduction/sprint | prompts/ token counts |
| A/B tests prompts executes | 2+/sprint | eval/ results |
| Taux de reponses conformes au format | 95%+ | eval/ format compliance |

### 28 Data Scientist
| KPI | Cible | Mesure |
|-----|-------|--------|
| Modeles/analyses livres | 2+/sprint | data-science/ notebooks |
| Metriques utilisateur analysees | 1 report/sprint | analytics/ reports |
| Experiments documentes | 100% | data-science/experiments.md |

### 33 AI Safety
| KPI | Cible | Mesure |
|-----|-------|--------|
| Guardrails testes | 100% coverage | tests/safety/ results |
| Incidents prompt injection detectes | 100% caught | security/ai-safety-log.md |
| Red team exercises executes | 1+/sprint | security/red-team/ reports |

---

## Engineering — Backend

### 19 Senior Backend
| KPI | Cible | Mesure |
|-----|-------|--------|
| Features livrees conformes aux specs | 100% | PR vs spec checklist |
| Code coverage sur code produit | 90%+ | pytest --cov report |
| PRs avec 0 defaut post-merge | 95%+ | bug tracker |

### 20 Junior Backend
| KPI | Cible | Mesure |
|-----|-------|--------|
| Taches assignees completees | 85%+/sprint | tasks/todo.md |
| PRs acceptees sans revision majeure | 70%+ | PR review rounds count |
| Tests unitaires ecrits par feature | 3+/feature | tests/ count per PR |

### 35 Integration Eng
| KPI | Cible | Mesure |
|-----|-------|--------|
| Connecteurs Odoo testes end-to-end | 100% | tests/integration/ results |
| Temps de reponse XML-RPC/JSON-RPC p95 | <2s | monitoring logs |
| Erreurs d'integration non-catchees | 0 | error tracking system |

### 43 Chat Eng
| KPI | Cible | Mesure |
|-----|-------|--------|
| Temps de reponse chat p95 | <3s | monitoring dashboards |
| Conversations gerees sans escalation | 90%+ | chat/ logs analysis |
| Features chat livrees | 2+/sprint | PR count tagged chat |

---

## Engineering — Frontend & Mobile

### 21 Frontend Eng
| KPI | Cible | Mesure |
|-----|-------|--------|
| Composants UI livres conformes aux maquettes | 100% | design review sign-off |
| Lighthouse performance score | 90+ | CI lighthouse report |
| Tests Vitest coverage | 80%+ | vitest --coverage report |

### 27 UX Designer
| KPI | Cible | Mesure |
|-----|-------|--------|
| Maquettes livrees avant dev start | 100% | design/ folder vs sprint plan |
| Iterations basees sur user feedback | 2+/sprint | design/ versions |
| Usability issues identifies | 3+/sprint | design/usability-log.md |

### 39 Mobile Eng
| KPI | Cible | Mesure |
|-----|-------|--------|
| Ecrans mobile livres | 2+/sprint | PR count tagged mobile |
| Crash rate | <0.1% | mobile crash analytics |
| Performance mobile (TTI) | <2s | mobile perf reports |

### 42 Brand Designer
| KPI | Cible | Mesure |
|-----|-------|--------|
| Assets visuels livres | 5+/sprint | design/assets/ count |
| Brand guidelines respectees | 100% audits | design/brand-audit.md |
| Temps de livraison asset demande | <48h | request timestamps |

---

## Engineering — Infrastructure & Ops

### 12 Infra Eng
| KPI | Cible | Mesure |
|-----|-------|--------|
| Uptime infrastructure | 99.9%+ | monitoring dashboard |
| Incidents infra resolus en <1h | 90%+ | incident log timestamps |
| IaC coverage | 100% | terraform/ansible audit |

### 22 DevOps
| KPI | Cible | Mesure |
|-----|-------|--------|
| CI/CD pipeline success rate | 95%+ | CI dashboard |
| Deploy time (commit to production) | <15min | CI pipeline duration |
| Pipeline failures resolved | <2h MTTR | CI incident log |

### 23 SRE
| KPI | Cible | Mesure |
|-----|-------|--------|
| SLO respect (availability) | 99.9%+ | SLO dashboard |
| Error budget consumed | <50%/sprint | error budget tracker |
| Runbooks documentes et a jour | 100% | sre/runbooks/ count |

### 30 DBA
| KPI | Cible | Mesure |
|-----|-------|--------|
| Query performance (slow queries) | 0 queries >1s | DB monitoring logs |
| Migrations executees sans downtime | 100% | migration logs |
| Backup verification tests | 1+/sprint | dba/backup-tests.md |

### 31 Chaos Eng
| KPI | Cible | Mesure |
|-----|-------|--------|
| Chaos experiments executes | 2+/sprint | chaos/ reports |
| Failles de resilience decouvertes | track all | chaos/findings.md |
| MTTR apres chaos test | <30min | chaos/ recovery timestamps |

### 38 Observability
| KPI | Cible | Mesure |
|-----|-------|--------|
| Dashboards operationnels a jour | 100% | monitoring/ config audit |
| Alertes pertinentes (false positive rate) | <5% | alert log analysis |
| Traces/metriques couvrant tous les services | 100% | observability/ coverage map |

---

## Security

### 14 Security Auditor
| KPI | Cible | Mesure |
|-----|-------|--------|
| Audits de securite completes | 1+/sprint | security/audits/ reports |
| Findings critiques ouverts | 0 | security/findings.md |
| Temps de remediation critique | <24h | finding timestamps |

### 24 DevSecOps
| KPI | Cible | Mesure |
|-----|-------|--------|
| Scans SAST/DAST executes | 100% des PRs | CI security stage logs |
| Vulnerabilites dependencies (CVE) | 0 high/critical | pip-audit / npm audit |
| Secrets leaks detectes | 0 in codebase | gitleaks report |

### 26 SOC
| KPI | Cible | Mesure |
|-----|-------|--------|
| Incidents securite detectes et documentes | 100% | soc/incidents/ log |
| Temps moyen de detection (MTTD) | <1h | soc/ timestamps |
| False positive rate sur alertes | <10% | soc/ alert analysis |

---

## QA & Testing

### 13 QA Lead
| KPI | Cible | Mesure |
|-----|-------|--------|
| Test coverage globale | 85%+ | pytest --cov + vitest --coverage |
| Bugs trouves avant release | 90%+ | bug tracker pre/post release |
| Test plans documentes par feature | 100% | qa/test-plans/ |

### 48 QA Automation
| KPI | Cible | Mesure |
|-----|-------|--------|
| Tests automatises ajoutes/sprint | 10+/sprint | tests/ commit count |
| Tests flaky identifies et fixes | 100% | CI flaky test report |
| Temps d'execution suite complete | <10min | CI pipeline duration |

---

## Customer & Marketing

### 17 Customer Success
| KPI | Cible | Mesure |
|-----|-------|--------|
| NPS score utilisateurs | 50+ | survey results |
| Tickets support resolus <24h | 90%+ | support/ ticket tracker |
| Churn rate mensuel | <5% | analytics/ churn report |

### 18 Growth
| KPI | Cible | Mesure |
|-----|-------|--------|
| Signups trial/semaine | tracking + growth | analytics/ signup funnel |
| Conversion trial-to-paid | 15%+ | analytics/ conversion report |
| Experiments growth lances | 2+/sprint | growth/experiments.md |

### 34 Competitive Intel
| KPI | Cible | Mesure |
|-----|-------|--------|
| Rapports concurrentiels livres | 1+/sprint | competitive/ reports |
| Features concurrentes trackees | 100% acteurs majeurs | competitive/ matrix |
| Insights actionnables identifies | 3+/sprint | competitive/ action items |

### 37 Content Strat
| KPI | Cible | Mesure |
|-----|-------|--------|
| Articles/contenus publies | 2+/sprint | content/ published count |
| SEO keywords positionnees top 20 | +5/quarter | SEO tracking tool |
| Content calendar respecte | 90%+ | content/calendar.md |

### 46 Product Marketing
| KPI | Cible | Mesure |
|-----|-------|--------|
| Launch materials prets a temps | 100% | marketing/ folder audit |
| Messaging testes (A/B) | 2+/sprint | marketing/ab-tests.md |
| Sales enablement docs a jour | 100% | marketing/sales-enablement/ |

### 47 Community Mgr
| KPI | Cible | Mesure |
|-----|-------|--------|
| Posts communaute publies | 5+/sprint | community/ post log |
| Engagement rate | 5%+ | community/ analytics |
| Questions communaute repondues <12h | 90%+ | community/ response tracker |

---

## Documentation & i18n

### 29 Tech Writer
| KPI | Cible | Mesure |
|-----|-------|--------|
| Pages documentation livrees/maj | 5+/sprint | docs/ commit count |
| Documentation coverage (endpoints) | 100% | docs/ vs api/ audit |
| Feedback doc integre | 100% | docs/feedback-log.md |

### 36 i18n Lead
| KPI | Cible | Mesure |
|-----|-------|--------|
| Langues supportees | track progress | i18n/ locale count |
| Taux de traduction complete par langue | 95%+ | i18n/ coverage report |
| Strings non-traduites | <5% | i18n/ missing keys audit |

---

## HR & Wellbeing

### 44 HR Director
| KPI | Cible | Mesure |
|-----|-------|--------|
| KPI reviews completees a temps | 100%/sprint | hr/ review records |
| Agents sous-utilises identifies et reaffectes | 0 idle agents | hr/assignation tracking |
| Onboarding nouveaux process documentes | 100% | hr/onboarding/ |

### 45 Wellbeing Officer
| KPI | Cible | Mesure |
|-----|-------|--------|
| Sondages wellbeing realises | 1+/sprint | hr/sondage-wellbeing-*.md |
| Score satisfaction equipe | 80%+ | survey results |
| Actions wellbeing implementees | 2+/sprint | hr/wellbeing-actions.md |

### 41 Support Eng
| KPI | Cible | Mesure |
|-----|-------|--------|
| Tickets resolus/sprint | 15+/sprint | support/ ticket tracker |
| Temps moyen de resolution | <4h | support/ timestamps |
| Escalations evitees | 80%+ | support/ escalation rate |

---

## Legende
- **Cible** : objectif minimum attendu par sprint (sauf mention contraire)
- **Mesure** : ou et comment verifier le KPI
- Les KPIs sont revus a chaque fin de sprint par HR Director (44) et PM (04)
- Tout agent en dessous de la cible 2 sprints consecutifs declenche un plan d'amelioration
