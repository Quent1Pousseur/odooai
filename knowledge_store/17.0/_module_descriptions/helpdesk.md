# Module Odoo 17 : Helpdesk - Description Métier Complète

## Vue d'ensemble

Le module **Helpdesk** d'Odoo 17 est une solution complète de gestion de tickets de support client. Il permet de gérer les demandes d'assistance depuis leur création jusqu'à leur résolution, avec un système de SLA, d'assignation automatique, et d'intégrations diverses (email, website, live chat, etc.).

---

## USE CASE 1 : Configuration d'une équipe Helpdesk

### Modèle : `helpdesk.team`

**Champs clés :**
- `name` : Nom de l'équipe (requis, traduit)
- `active` : Statut actif/inactif
- `member_ids` : Membres de l'équipe (Many2many vers res.users)
- `stage_ids` : Étapes disponibles pour cette équipe
- `auto_assignment` : Assignation automatique activée/désactivée
- `assign_method` : Méthode d'assignation ('randomly' ou 'balanced')
- `privacy_visibility` : Visibilité ('invited_internal', 'internal', 'portal')
- `use_alias` : Utilisation d'alias email
- `use_website_helpdesk_form` : Formulaire web activé

**Workflow complet :**
1. **Création** : Aller dans Helpdesk → Configuration → Équipes
2. **Configuration de base** :
   - Saisir le nom de l'équipe
   - Ajouter les membres dans `member_ids`
   - Définir la séquence d'affichage
3. **Configuration des étapes** :
   - Les étapes par défaut sont créées automatiquement : "New", "In Progress", "Solved", "Cancelled"
   - Modifier via le champ `stage_ids`
4. **Assignation automatique** :
   - Activer `auto_assignment`
   - Choisir la méthode dans `assign_method`
5. **Configuration email** :
   - Activer `use_alias` pour recevoir les tickets par email
   - Configurer l'alias dans les paramètres

**Menu dans Odoo :** Helpdesk → Configuration → Équipes

**Pièges courants :**
- Oublier d'ajouter des membres à l'équipe → pas d'assignation possible
- Ne pas configurer l'alias email → les emails ne créent pas de tickets
- Mauvaise configuration de `privacy_visibility` → problèmes d'accès

**Bonnes pratiques :**
- Créer des équipes spécialisées par domaine (technique, commercial, etc.)
- Utiliser l'assignation équilibrée pour une répartition optimale
- Configurer les étapes selon le processus métier réel

---

## USE CASE 2 : Gestion des tickets de support

### Modèle : `helpdesk.ticket`

**Champs clés :**
- `name` : Sujet du ticket (requis, indexé)
- `team_id` : Équipe assignée
- `user_id` : Utilisateur assigné
- `stage_id` : Étape courante
- `priority` : Priorité (0=Low, 1=Medium, 2=High, 3=Urgent)
- `partner_id` : Client concerné
- `partner_email` : Email du client
- `description` : Description détaillée
- `ticket_type_id` : Type de ticket
- `tag_ids` : Tags/étiquettes
- `sla_ids` : SLA applicables
- `kanban_state` : État Kanban (normal, done, blocked)

**Workflow complet :**
1. **Création du ticket** :
   - Automatique par email (si alias configuré)
   - Manuel via Helpdesk → Tickets → Créer
   - Via formulaire web (si activé)
2. **Assignation** :
   - Automatique selon la configuration de l'équipe
   - Manuelle via le champ `user_id`
3. **Traitement** :
   - Changement d'étape dans `stage_id`
   - Ajout de notes/commentaires
   - Modification de la priorité si nécessaire
4. **Suivi SLA** :
   - Les SLA applicables sont automatiquement créés
   - Suivi des deadlines via `helpdesk.sla.status`
5. **Résolution** :
   - Passage à l'étape finale (fold=True)
   - Envoi automatique d'email si template configuré

**Menu dans Odoo :** Helpdesk → Tickets

**Pièges courants :**
- Ne pas remplir `partner_id` → perte du lien client
- Mauvaise configuration des étapes → workflow cassé
- Oublier de traiter les tickets urgents → non-respect SLA

**Bonnes pratiques :**
- Utiliser les priorités de manière cohérente
- Remplir systématiquement les informations client
- Suivre les SLA via le tableau de bord

---

## USE CASE 3 : Configuration et suivi des SLA

### Modèles : `helpdesk.sla` et `helpdesk.sla.status`

**Champs clés SLA :**
- `name` : Nom de la politique SLA
- `team_id` : Équipe concernée
- `time` : Temps limite en heures
- `stage_id` : Étape cible à atteindre
- `priority` : Priorité applicable
- `ticket_type_ids` : Types de tickets concernés
- `partner_ids` : Clients spécifiques
- `exclude_stage_ids` : Étapes exclues du calcul

**Champs clés Status :**
- `ticket_id` : Ticket concerné
- `sla_id` : Politique SLA
- `deadline` : Date limite calculée
- `reached_datetime` : Date d'atteinte de l'objectif
- `status` : Statut (failed, reached, ongoing)
- `exceeded_hours` : Heures de dépassement

**Workflow complet :**
1. **Configuration SLA** :
   - Aller dans Helpdesk → Configuration → SLA Policies
   - Créer une politique avec :
     - Temps limite dans `time`
     - Étape cible dans `stage_id`
     - Critères d'application (priorité, type, client)
2. **Application automatique** :
   - À la création du ticket, les SLA applicables sont identifiés
   - Création automatique des `helpdesk.sla.status`
   - Calcul de la deadline selon le calendrier de travail
3. **Suivi en temps réel** :
   - Statut mis à jour automatiquement
   - Alertes visuelles selon le statut
   - Rapports de performance SLA

**Menu dans Odoo :** Helpdesk → Configuration → SLA Policies

**Pièges courants :**
- Calendrier de travail mal configuré → deadlines incorrectes
- Oublier les étapes d'exclusion → calculs faussés
- SLA trop ambitieux → stress inutile

**Bonnes pratiques :**
- Commencer par des SLA réalistes
- Exclure les étapes d'attente client
- Monitorer régulièrement les performances

---

## USE CASE 4 : Gestion des étapes (stages)

### Modèle : `helpdesk.stage`

**Champs clés :**
- `name` : Nom de l'étape (requis, traduit)
- `sequence` : Ordre d'affichage
- `fold` : Étape fermée (tickets considérés comme clos)
- `team_ids` : Équipes utilisant cette étape
- `template_id` : Template email automatique
- `legend_blocked/done/normal` : Légendes Kanban

**Workflow complet :**
1. **Création d'étapes** :
   - Aller dans Helpdesk → Configuration → Stages
   - Créer avec nom et séquence
   - Définir si l'étape est fermée (`fold`)
2. **Association aux équipes** :
   - Lier dans `team_ids`
   - Configurer l'ordre via `sequence`
3. **Automatisation email** :
   - Créer template dans Email → Templates
   - Associer dans `template_id`
4. **Configuration Kanban** :
   - Personnaliser les légendes selon l'état

**Menu dans Odoo :** Helpdesk → Configuration → Stages

**Pièges courants :**
- Trop d'étapes → confusion
- Pas d'étape fermée → tickets jamais "finis"
- Mauvais ordre des étapes → workflow illogique

**Bonnes pratiques :**
- Maximum 5-6 étapes par équipe
- Une étape finale avec `fold=True`
- Templates email pour informer le client

---

## USE CASE 5 : Intégration email et alias

**Configuration dans l'équipe :**
- `use_alias` : Active la réception par email
- `alias_name` : Nom de l'alias (ex: support@monentreprise.com)
- `alias_defaults` : Valeurs par défaut pour les tickets créés

**Workflow complet :**
1. **Configuration serveur** :
   - Paramètres → Technique → Email → Serveurs entrants
   - Configurer IMAP/POP
2. **Configuration alias** :
   - Dans l'équipe Helpdesk
   - Activer `use_alias`
   - Définir l'alias email
3. **Traitement automatique** :
   - Emails reçus → tickets créés automatiquement
   - Expéditeur → `partner_email` et `partner_id` si trouvé
   - Sujet → `name` du ticket
   - Corps → `description`

**Pièges courants :**
- Serveur email mal configuré → emails perdus
- Alias en conflit → création impossible
- Pas de nettoyage des emails → spam dans les tickets

**Bonnes pratiques :**
- Tester la configuration avec des emails de test
- Utiliser des alias dédiés par équipe
- Configurer des filtres anti-spam

---

## Menus principaux dans Odoo :

- **Helpdesk** (menu racine)
  - **Tickets** → Vue des tickets
  - **Rapports** → Analyses SLA et performance
  - **Configuration**
    - **Équipes** → Gestion des équipes
    - **Stages** → Gestion des étapes  
    - **SLA Policies** → Politiques SLA
    - **Types** → Types de tickets
    - **Tags** → Étiquettes

## Intégrations availables :

- **Website Form** : Formulaire web public
- **Live Chat** : Chat en direct
- **Knowledge** : Base de connaissances
- **Timesheets** : Feuilles de temps sur tickets
- **Forum** : Forum communautaire d'entraide

Cette architecture modulaire permet une adaptation fine selon les besoins de chaque organisation.