# Consultation BizDev (32) — Timing Integrateur
## Date : 2026-03-20
## Demandee par : Fondateur (00)
## Participants : BizDev (32), CEO (01), Sales (05), CPO (03), CTO (02)

---

## Question du fondateur

"Les reponses sont trop vagues, le design est prototype, et un integrateur voudra connecter PLUSIEURS bases de donnees clients. Est-ce qu'on est pas trop tot pour contacter le Gold Partner Bruxelles ?"

---

## BizDev (32)

"Le fondateur a raison sur les 3 points. Laissez-moi etre honnete :

**Ce qu'un integrateur Gold Partner attend :**
1. Des reponses PRECISES — pas du generique. Il connait Odoo mieux que l'IA. Si l'IA dit une betise sur stock.route, il le verra en 2 secondes.
2. Du multi-tenant — il a 20-50 clients PME. Il veut connecter TOUTES leurs bases, pas une par une en localhost.
3. Un dashboard partenaire — voir l'usage de ses clients, facturation groupee.
4. De la fiabilite — si ca crash pendant une demo client, c'est LUI qui perd sa reputation.

**Ou on en est :**
- Reponses a 6.8/10 pertinence → un integrateur tolere 8+ minimum
- Single tenant → il ne peut pas l'utiliser pour ses clients
- Pas de staging → tout tourne en localhost
- Pas d'auth → n'importe qui accede

**Mon verdict : on est trop tot. On a besoin de 4-6 semaines supplementaires.**

Mais je ne veux pas perdre le contact. Voici ce que je propose :"

## Proposition BizDev — approche en 2 temps

### Temps 1 — Maintenant (Sprint 4-5)
- **Ne PAS faire de demo produit** a l'integrateur
- **Envoyer un teaser** : le one-pager + les stats (1218 modules, 5514 modeles) + le pitch
- **Objectif** : planter la graine, susciter la curiosite, prendre un call informel de 15min
- **Message** : "On construit un outil IA pour Odoo. On cherche des partenaires beta pour co-construire. Interesse pour un call rapide ?"
- L'integrateur ne voit PAS le produit, juste la vision

### Temps 2 — Sprint 7-8 (dans 4-6 semaines)
- Multi-tenant fonctionnel
- Staging deploye avec HTTPS
- Reponses a 8+/10 de pertinence
- Dashboard partenaire basique
- **Demo live** avec l'instance de test de l'integrateur
- **Objectif** : signer un partenariat beta (5-10 clients PME connectes)

---

## Reactions

**CEO (01)** : "D'accord avec BizDev. On ne montre pas un prototype a un Gold Partner. Mais le teaser c'est malin — ca cree de l'anticipation."

**Sales (05)** : "Le one-pager de Product Marketing est parfait pour ca. Pas de screenshots du produit, juste la vision + les stats + le pricing. C'est vendeur sans rien montrer."

**CPO (03)** : "Ca me rassure. Ca nous donne le temps de faire la passe design et d'ameliorer les reponses. Le produit sera 10x meilleur dans 4 semaines."

**CTO (02)** : "Le multi-tenant c'est la priorite technique #1 pour les integrateurs. C'est prevu en Milestone 3 (Beta-Ready). Faisable en Sprint 6-7."

---

## Decisions

| # | Decision | Responsable | Quand |
|---|----------|-------------|-------|
| 1 | Reporter la demo live a Sprint 7-8 | CEO | Immediate |
| 2 | Envoyer un teaser (one-pager + vision) quand pret | BizDev + Sales | Sprint 5 |
| 3 | Multi-tenant = priorite #1 Sprint 6 | CTO + Backend Arch | Sprint 6 |
| 4 | Objectif pertinence : 8+/10 avant demo integrateur | Prompt Eng + Data Scientist | Sprint 5-6 |
| 5 | Issue #10 passe de "bloquant demo" a "Sprint 5" | PM | Immediate |

---

## Impact sur le Sprint 4

La demo du 24 mars est **annulee** en tant que demo integrateur.
A la place, le fondateur fait un **test interne** : poser 20 questions variees et noter la pertinence.

Les issues #10, #11, #12 sont **reportees** :
- #10 Contact integrateur → Sprint 5 (teaser only)
- #11 Instance Odoo demo → reste utile pour le test interne
- #12 Run through demo → reporte a Sprint 7

> "Mieux vaut un produit qui impressionne dans 6 semaines qu'un prototype qui decoie demain." — BizDev (32)
