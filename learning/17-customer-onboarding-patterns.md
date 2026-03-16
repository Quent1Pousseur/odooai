# Learning — Customer Success (17) — SaaS Onboarding Best Practices
## Date : 2026-03-21
## Duree : 3 heures

## Ce que j'ai appris

1. **Le "Time-to-Value" (TTV) est la metrique #1 de l'onboarding** — Le moment ou
   l'utilisateur percoit la valeur pour la premiere fois determine s'il reste. Pour
   les SaaS B2B, le TTV cible est < 5 minutes. Pour OdooAI, ca signifie : connecter
   son Odoo et recevoir un premier insight utile en moins de 5 minutes.

2. **Le pattern "Setup Wizard + First Win" bat le "Feature Tour"** — Les tours guides
   qui montrent chaque bouton ont un taux de completion de 15%. Un wizard qui aide
   a faire UNE action concrete (connecter Odoo, lancer un audit) atteint 65%.
   Slack, Notion et Linear utilisent tous ce pattern.

3. **Les emails d'onboarding "behavior-based" surpassent les "time-based"** — Au lieu
   d'envoyer un email a J1, J3, J7, envoyer un email quand l'utilisateur n'a pas
   complete une etape cle. Ex : "Vous avez connecte Odoo mais n'avez pas encore
   lance votre premier audit. Voici comment en 2 clics."

4. **Le "Aha Moment" doit etre identifie et mesure** — Pour Dropbox c'etait "upload
   1 fichier", pour Slack "envoyer 2000 messages en equipe". Pour OdooAI, hypothese :
   "recevoir une recommandation de configuration actionnee" = le moment ou l'utilisateur
   comprend la valeur. A valider avec les design partners.

5. **Le checklist d'onboarding visible augmente la completion de 40%** — Afficher une
   barre de progression avec les etapes restantes (connecter Odoo, choisir un module,
   poser une question, inviter un collegue) cree un effet de completion psychologique.
   Intercom et HubSpot utilisent ce pattern avec succes.

## Comment ca s'applique a OdooAI

1. **Wizard de connexion en 3 etapes** : Etape 1 — Entrer l'URL Odoo + credentials
   (formulaire ODAI-UI-003 deja fait). Etape 2 — Selection du premier module a
   analyser (liste auto-detectee). Etape 3 — Premiere question suggeree par l'IA
   ("Quels sont les risques de securite sur ce module ?"). TTV cible : 4 minutes.

2. **Emails behavior-based** : Tracker 4 evenements cles — signup, connexion_odoo,
   premier_audit, premiere_action. Envoyer un email de relance uniquement si
   l'etape suivante n'est pas completee dans les 24h. Pas de spam time-based.

3. **Checklist dans le dashboard** : Afficher une checklist persistante dans la sidebar
   jusqu'a completion : "Connecter Odoo", "Lancer un audit", "Explorer une recommandation",
   "Inviter un collegue". Disparait apres completion, reapparait si nouvelle connexion.

## Ce que je recommande

1. **Sprint 8** : Designer et implementer le wizard d'onboarding post-signup.
   3 ecrans, progression visuelle, bouton "Skip" discret. Le wizard doit aboutir
   a la premiere reponse IA en < 4 minutes. Fichier : `web/app/onboarding/`.

2. **Sprint 9** : Implementer le tracking des evenements d'onboarding dans le backend.
   Table `onboarding_events` avec `user_id`, `event_type`, `completed_at`.
   Service : `odooai/services/onboarding_tracker.py`. Emails via Resend API.

3. **Sprint 10** : Mesurer le TTV reel sur les 5 premiers design partners.
   Objectif : identifier le "Aha Moment" avec des donnees reelles. Si TTV > 5 min,
   prioriser la simplification du flow de connexion Odoo.

## Sources

1. Wes Bush — "Product-Led Growth" (2019) — Chapitres sur le TTV et l'onboarding
2. Userpilot Blog — "SaaS Onboarding Benchmarks 2025" — Taux de completion par pattern
3. Reforge — "The Aha Moment Framework" — Identification et optimisation du moment cle
