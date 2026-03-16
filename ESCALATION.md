# OdooAI — Matrice d'Escalade

## Principe

Quand quelque chose va mal, chaque seconde compte. Cette matrice definit QUI appeler, QUAND, et dans QUEL ORDRE. Pas de flou, pas d'hesitation.

---

## Par Type de Probleme

### 🔴 SECURITE — Breach ou vulnerabilite suspectee
```
Detecte par : n'importe qui
  ↓ IMMEDIATE (< 5 min)
SOC Analyst (26) — evalue la menace
  ↓
Security Architect (07) — decide les contre-mesures applicatives
DevSecOps (24) — applique les contre-mesures infrastructure
  ↓ SI CONFIRME (< 15 min)
CTO (02) — informe, decide la communication
CEO (01) — decide la communication externe
Legal (16) — evalue les obligations GDPR (notification 72h)
  ↓
FONDATEUR — informe immediatement
```

### 🔴 INCIDENT PRODUCTION — Service down ou degrade
```
Detecte par : SRE (23) via monitoring / SOC (26) / Support (41) via client
  ↓ IMMEDIATE (< 5 min)
SRE (23) — incident commander, diagnostique
DevOps (22) — rollback si lie au deploy
  ↓ SI PAS RESOLU EN 15 MIN
Backend Architect (08) — aide au diagnostic
Senior Backend Dev (19) — hotfix si necessaire
  ↓ SI PAS RESOLU EN 30 MIN
CTO (02) — informe, mobilise des ressources supplementaires
  ↓ SI IMPACT CLIENT
Support Engineer (41) — communication aux clients affectes
Customer Success (17) — communication aux clients Enterprise
  ↓
FONDATEUR — informe si > 30 min de downtime
```

### 🟠 BUG CRITIQUE — Fonctionnalite cassee, donnees corrompues
```
Detecte par : Support (41) / QA (13) / n'importe qui
  ↓ RAPIDE (< 1h)
Senior Backend Dev (19) — diagnostic et fix
QA Lead (13) — reproduit et confirme
  ↓ SI IMPACT SECURITE
Security Architect (07) — evalue le risque donnees
  ↓ SI IMPACT CLIENT
Support Engineer (41) — workaround communique aux clients
  ↓
PM (04) — informe l'equipe au prochain standup
```

### 🟠 COUT LLM ANORMAL — Depassement budget
```
Detecte par : Observability (38) / CFO (15) via dashboard
  ↓ RAPIDE (< 2h)
AI Engineer (09) — identifie la cause (prompt, routing, abus)
Data Scientist (28) — analyse le pattern
  ↓ SI ABUS UTILISATEUR
Support Engineer (41) — contacte le client
SaaS Architect (06) — evalue les limites du plan
  ↓ SI PROBLEME SYSTEME
Prompt Engineer (25) — optimise les prompts
  ↓
CFO (15) — ajuste les projections
CEO (01) — informe si impact significatif sur la marge
```

### 🟡 VETO — Un agent bloque une decision
```
Emis par : n'importe quel agent dans son domaine
  ↓ DOCUMENTE
PM (04) — documente le VETO, organise la discussion
  ↓ DISCUSSION (< 24h)
Les parties concernees presentent leurs arguments
  ↓ SI PAS DE CONSENSUS
CTO (02) — arbitre si technique
CEO (01) — arbitre si business/strategie
  ↓
FONDATEUR — tranche si les C-levels ne s'accordent pas
```

### 🟡 FOURNISSEUR — Probleme avec un fournisseur critique
```
Detecte par : n'importe qui / Vendor Manager (40) via monitoring
  ↓ IMMEDIATE SI CRITIQUE (Anthropic down, cloud down)
SRE (23) — active le mode degrade
Vendor Manager (40) — contacte le fournisseur
  ↓ SI PROLONGE (> 1h)
CTO (02) — decide l'activation du plan B
CFO (15) — evalue l'impact financier
  ↓ SI CHANGEMENT DE FOURNISSEUR NECESSAIRE
CEO (01) + CTO (02) + CFO (15) — decision strategique
```

### 🟡 CLIENT ENTERPRISE MECONTENT
```
Detecte par : Support (41) / Customer Success (17)
  ↓ RAPIDE (< 2h)
Customer Success (17) — prend en charge, evalue la situation
  ↓ SI PROBLEME TECHNIQUE
Senior Backend Dev (19) — fix prioritaire
  ↓ SI PROBLEME PRODUIT
CPO (03) — evalue, priorise
  ↓ SI RISQUE DE CHURN
Sales (05) — intervention commerciale (offre, extension, call)
CEO (01) — appel personnel si client strategique
  ↓
FONDATEUR — informe si client > 10% du MRR
```

---

## Regles Generales

1. **Toujours escalader VERS LE HAUT** — jamais lateralement sans informer la hierarchie
2. **Documenter CHAQUE escalade** — dans `incidents/` ou `meetings/daily/`
3. **Le PM est TOUJOURS informe** — il maintient la vue globale
4. **Le fondateur est informe** pour : breach securite, downtime > 30min, perte de client Enterprise, VETO non resolu
5. **Pas de heroisme silencieux** — si tu geres un incident seul sans le dire, c'est un probleme
