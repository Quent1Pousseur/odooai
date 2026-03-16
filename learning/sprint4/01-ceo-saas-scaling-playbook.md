# Learning — CEO (01) — SaaS Scaling Playbook : de 0 a 100 clients
## Date : 2026-03-21
## Duree : 3 heures

## Ce que j'ai appris

1. **Le "First 10" est fondamentalement different du "Next 90"** — Les 10 premiers clients
   se trouvent par contact direct (fondateur qui vend), les 90 suivants par un systeme
   repeatable. La transition est le moment le plus dangereux pour un SaaS B2B.

2. **Le concept de "Design Partner" accelere le PMF** — Signer 3-5 partenaires Odoo
   (integrateurs) comme design partners avec un tarif reduit en echange de feedback
   structure permet de valider le produit avant de scaler. Lattice et Figma ont
   utilise cette approche avec succes.

3. **Le Net Revenue Retention (NRR) > 100% est le signal de scaling** — Avant d'investir
   en acquisition, s'assurer que les clients existants upgraderont naturellement.
   Un NRR < 100% signifie qu'on remplit un seau perce.

4. **Le "land and expand" fonctionne mieux que le "big deal" en early stage** — Vendre
   un plan Starter a 49 EUR/mois puis upseller vers Pro (149 EUR) est plus predictible
   que de viser des Enterprise d'emblee.

5. **La regle du 40 (croissance + marge > 40%) reste le benchmark** — Meme en early stage,
   garder ce ratio en tete pour les decisions d'investissement marketing vs. produit.

## Comment ca s'applique a OdooAI

1. **Phase Design Partners (Sprint 8-10)** : Identifier 5 integrateurs Odoo francophones
   et leur proposer un acces gratuit 6 mois en echange de 2 sessions feedback/mois.
   Cible : integrateurs qui gerent 10-50 instances Odoo pour leurs clients.

2. **Land and Expand via le plan Starter** : Notre plan a 49 EUR doit resoudre un pain
   point unique (audit de configuration Odoo) suffisamment bien pour que le client
   veuille ensuite le plan Pro pour l'analyse continue.

3. **Metriques de scaling** : Tracker NRR des le premier client payant. Si un client
   Starter ne devient pas Pro en 3 mois, c'est un signal produit, pas un signal sales.

## Ce que je recommande

1. **Sprint 8** : Creer un programme "OdooAI Pioneers" — 5 slots, acces gratuit,
   engagement de feedback bi-mensuel. Livrable : landing page dediee + sequence email.

2. **Sprint 10** : Definir les 3 triggers d'upsell Starter -> Pro bases sur l'usage
   reel (nombre de requetes, modules analyses, users). Implementer le tracking
   dans notre backend FastAPI.

3. **Sprint 12** : Premier bilan NRR et decision go/no-go sur l'investissement
   en acquisition payante (Google Ads sur keywords Odoo).

## Sources

1. "The SaaS Playbook" — Rob Walling (2023) — Chapitres 3-5 sur le scaling early stage
2. "From Impossible to Inevitable" — Aaron Ross & Jason Lemkin — Modele de revenue predictible
3. OpenView Partners — "2025 SaaS Benchmarks Report" — Metriques NRR et CAC par segment
