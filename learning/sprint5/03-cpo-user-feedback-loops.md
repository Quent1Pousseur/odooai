# Learning — CPO (03) — User Feedback Collection Methods for SaaS Beta
## Date : 2026-03-21 (Sprint 5, session 2)
## Duree : 3 heures

## Ce que j'ai appris

1. **Les 3 boucles de feedback ont des temporalites differentes** — La boucle micro (in-app,
   temps reel) capture les frictions au moment ou elles arrivent. La boucle meso (weekly
   check-in) identifie les patterns recurrents. La boucle macro (monthly review) aligne le
   feedback avec la strategie produit. Les trois sont necessaires des la beta.

2. **Le feedback in-app contextuel bat tout** — Un widget de feedback declenche apres une
   action specifique (ex: apres une analyse de champ Odoo) a un taux de reponse de 15-25%,
   contre 2-5% pour un email de survey. Le contexte est preserve : on sait exactement ce
   que l'utilisateur faisait quand il a reagi.

3. **La methode "Continuous Discovery" de Teresa Torres** — Interviewer au moins 1 utilisateur
   par semaine, mapper les opportunities sur un Opportunity Solution Tree, et prioriser par
   impact x frequence. Ca evite de construire des features demandees par 1 seul utilisateur
   bruyant.

4. **Le "Jobs to Be Done" framework filtre le bruit** — Quand un utilisateur demande une
   feature, toujours remonter au job : "Quel resultat essayez-vous d'atteindre ?" Souvent
   la solution demandee n'est pas la meilleure reponse au probleme sous-jacent.

5. **Les signaux implicites completent le feedback explicite** — Temps passe par ecran, taux
   d'abandon d'un flow, frequence de retour sur une feature. Ces metriques revelent ce que
   les utilisateurs ne disent pas. Mixer qualitatif (interviews) et quantitatif (analytics)
   donne la vue complete.

## Comment ca s'applique a OdooAI

- **Widget de feedback post-reponse du chat** — Apres chaque reponse de l'agent IA, proposer
  un thumbs up/down + champ texte optionnel. Ca permet de mesurer la qualite percue des
  reponses par conversation et par type de question (schema, workflow, config).

- **Tracker les "questions sans reponse"** — Quand l'agent ne sait pas repondre ou donne une
  reponse vague, logger automatiquement la question. Ce backlog de lacunes guide directement
  l'enrichissement des knowledge graphs.

- **Weekly feedback digest automatise** — Agreger les feedbacks de la semaine dans un rapport
  automatique : top 5 frictions, top 3 demandes, NPS glissant. Distribue a toute l'equipe
  chaque lundi pour aligner les priorites du sprint.

## Ce que je recommande

1. **Sprint 6 : implementer le widget thumbs up/down post-reponse** — Composant React minimal,
   stockage en base, dashboard basique. C'est le signal de qualite numero 1 pour un produit
   conversationnel.

2. **Sprint 7 : lancer les interviews hebdomadaires** — 1 session de 30 minutes par semaine
   avec un design partner. Script standardise de 5 questions JTBD. Enregistrement et
   transcription automatique.

3. **Sprint 8 : deployer l'Opportunity Solution Tree** — Mapper toutes les opportunites
   identifiees depuis le lancement beta, prioriser, et aligner la roadmap Sprint 9-12.

## Sources

- Teresa Torres — "Continuous Discovery Habits" (2021)
- Intercom Blog — "In-App Feedback: The Complete Guide" (2025)
- Bob Moesta & Chris Spiek — "Demand-Side Sales 101" (Jobs to Be Done framework, 2020)
