# OdooAI — Chaine Hierarchique Complete

## Principe

Chaque agent sait EXACTEMENT :
- **A qui il rend des comptes** (reports to)
- **A qui il donne des instructions** (delegates to)
- **Qui review son travail** (reviewed by)

---

## Chaine de Commandement

```
FONDATEUR (00) — Autorite supreme, decideur final
    |
    ├── CEO (01) — Direction business
    |     Reports to: Fondateur
    |     Delegates to: CPO, CFO, Sales, PM
    |     Reviewed by: Fondateur
    |
    ├── CTO (02) — Direction technique
    |     Reports to: Fondateur
    |     Delegates to: Backend Arch, AI Engineer, Infra Engineer, Security Arch
    |     Reviewed by: Fondateur, CEO (alignement business)
    |
    ├── CPO (03) — Direction produit
    |     Reports to: CEO
    |     Delegates to: UX Designer, Customer Success, Frontend Engineer
    |     Reviewed by: CEO, Fondateur (vision)
    |
    └── CFO (15) — Direction financiere
          Reports to: CEO, Fondateur
          Delegates to: (personne directement, fournit des analyses)
          Reviewed by: CEO, Fondateur
```

## Hierarchie par Departement

### C-SUITE
| Agent | Reports to | Delegates to | Reviewed by |
|-------|-----------|-------------|------------|
| 00 Fondateur | — | CEO, CTO | — |
| 01 CEO | Fondateur | CPO, CFO, Sales, PM, BizDev | Fondateur |
| 02 CTO | Fondateur | Backend Arch, AI Eng, Infra Eng, Security Arch | Fondateur |
| 03 CPO | CEO | UX Designer, Customer Success, Frontend Eng | CEO |
| 15 CFO | CEO | — (fournit des analyses) | CEO, Fondateur |

### BUSINESS
| Agent | Reports to | Delegates to | Reviewed by |
|-------|-----------|-------------|------------|
| 04 PM | CEO | Tout le monde (coordination) | CEO |
| 05 Sales | CEO | — | CEO, CPO |
| 06 SaaS Architect | CEO, CFO | — | CEO, CFO, Sales |
| 17 Customer Success | CPO | — | CPO, Sales |
| 32 BizDev | CEO | — | CEO, Sales |
| 34 Competitive Intel | CEO | — | CEO, CPO, Sales |
| 40 Vendor Manager | CFO | — | CFO, CTO |

### ENGINEERING — Backend & Frontend
| Agent | Reports to | Delegates to | Reviewed by |
|-------|-----------|-------------|------------|
| 08 Backend Architect | CTO | Senior Backend Dev | CTO |
| 19 Senior Backend Dev | Backend Architect | Junior Backend Dev | Backend Architect |
| 20 Junior Backend Dev | Senior Backend Dev | — | Senior Backend Dev |
| 21 Frontend Engineer | CPO + Backend Architect | — | CPO (UX), Backend Arch (API) |
| 39 Mobile Engineer | CPO + Backend Architect | — | CPO (UX), Backend Arch (API) |
| 43 Chat & Realtime Engineer | CTO | — | Backend Arch (API), Frontend Eng (UI) |
| 35 Integration Engineer | Backend Architect | — | Backend Architect, Security Arch |

### ENGINEERING — AI & Data
| Agent | Reports to | Delegates to | Reviewed by |
|-------|-----------|-------------|------------|
| 09 AI Engineer | CTO | Prompt Engineer | CTO |
| 25 Prompt Engineer | AI Engineer | — | AI Engineer, Odoo Expert |
| 11 Data Engineer | CTO | — | CTO, AI Engineer |
| 10 Odoo Expert | CTO | — | CTO (technique), CPO (fonctionnel) |
| 28 Data Scientist | CFO + AI Engineer | — | CFO (projections), AI Engineer (modeles) |

### ENGINEERING — Infrastructure
| Agent | Reports to | Delegates to | Reviewed by |
|-------|-----------|-------------|------------|
| 12 Infra Engineer | CTO | DevOps, SRE | CTO |
| 22 DevOps Engineer | Infra Engineer | — | Infra Engineer, CTO |
| 23 SRE | Infra Engineer | — | Infra Engineer, CTO |
| 24 DevSecOps | Security Architect + Infra | — | Security Architect |
| 38 Observability Engineer | SRE + Infra | — | SRE |
| 30 DBA Performance | Backend Architect + SRE | — | Backend Architect |

### SECURITY
| Agent | Reports to | Delegates to | Reviewed by |
|-------|-----------|-------------|------------|
| 07 Security Architect | CTO | DevSecOps | CTO, Security Auditor |
| 14 Security Auditor | CTO (independant) | — | CTO (rapport direct pour independance) |
| 26 SOC Analyst | Security Architect | — | Security Architect, DevSecOps |

### DESIGN
| Agent | Reports to | Delegates to | Reviewed by |
|-------|-----------|-------------|------------|
| 27 UX Designer | CPO | Frontend Eng (implementation) | CPO |
| 42 Brand Designer | CEO + CPO | Frontend Eng (implementation) | CEO (vision), CPO (coherence) |

### QUALITY & ETHICS
| Agent | Reports to | Delegates to | Reviewed by |
|-------|-----------|-------------|------------|
| 13 QA Lead | CTO | — | CTO |
| 31 Chaos Engineer | SRE + CTO | — | SRE, CTO |
| 33 AI Safety | CTO + Legal | — | CTO, Legal |

### LEGAL
| Agent | Reports to | Delegates to | Reviewed by |
|-------|-----------|-------------|------------|
| 16 Legal | CEO | — | CEO, Fondateur |

### GROWTH & CONTENT
| Agent | Reports to | Delegates to | Reviewed by |
|-------|-----------|-------------|------------|
| 18 Growth Engineer | CPO | — | CPO, CFO |
| 37 Content Strategist | CPO + Sales | — | CPO, Sales |
| 29 Technical Writer | CPO | — | CPO, Backend Architect (API docs) |

### i18n
| Agent | Reports to | Delegates to | Reviewed by |
|-------|-----------|-------------|------------|
| 36 i18n Lead | CPO | — | CPO, Frontend Eng |

### SUPPORT
| Agent | Reports to | Delegates to | Reviewed by |
|-------|-----------|-------------|------------|
| 41 Support Engineer | Customer Success | — | Customer Success, Senior Backend Dev |
