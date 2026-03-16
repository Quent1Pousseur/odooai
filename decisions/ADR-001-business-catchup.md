# ADR-001 — Business Catch-Up Before More Code

## Date
2026-03-16

## Status
ACCEPTED

## Context
Sprint 1 a 7 pistes paralleles. Apres 3 sessions, seule la Piste 1 (DATA-001, technique) est terminee. Les pistes business (4-7) n'ont pas avance du tout. Le projet est desequilibre : 100% technique, 0% business.

Le Code Analyst a ete valide sur 1218 modules Odoo (0 echecs) — la tech fonctionne. Mais on n'a :
- Zero contact PME
- Zero modele de cout reel
- Zero validation marche
- Zero matrice concurrentielle finalisee
- Zero question juridique LGPL redigee

## Decision
**On arrete de coder tant que les pistes business n'ont pas rattrape.**

Prochains livrables :
1. Pitch OdooAI en 10 mots — Sales (05) + CEO (01)
2. 3 personas finalisees — CPO (03)
3. Liste 10 PME cibles — Sales (05)
4. Modele de cout LLM v1 — CFO (15)
5. Question juridique LGPL — Legal (16)
6. Matrice concurrentielle — Competitive Intel (34)
7. Definition aha moment — SaaS Architect (06)

## Consequences
- Pas de nouvelle spec technique tant que les livrables business ne sont pas produits
- Le code existant est gele (correction de bugs OK, nouvelles features non)
- Les agents techniques (Backend Arch, AI Eng, Data Eng) participent aux livrables business quand necessaire (estimations tokens, validation technique des personas)

## Auteur
Fondateur (00)
