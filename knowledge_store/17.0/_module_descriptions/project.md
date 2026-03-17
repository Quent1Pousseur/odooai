# Module Odoo 17 : Project - Description métier complète

## Vue d'ensemble
Le module **project** est un système complet de gestion de projets et de tâches dans Odoo 17. Il permet de structurer le travail en projets, d'organiser les tâches avec des étapes (stages), de suivre l'avancement avec des jalons (milestones), et de communiquer via des mises à jour de projet.

---

## USE CASE 1 : Gestion des Projets

### Modèle : `project.project`

**Champs clés :**
- `name` : Nom du projet (requis, traduit)
- `description` : Description HTML du projet
- `active` : Statut actif/inactif
- `partner_id` : Client du projet
- `company_id` : Société propriétaire
- `analytic_account_id` : Compte analytique pour la comptabilité
- `stage_id` : Étape du projet
- `favorite_user_ids` : Utilisateurs ayant mis en favoris
- `task_count`, `open_task_count`, `closed_task_count` : Compteurs de tâches
- `doc_count` : Nombre de documents attachés

**Workflow complet :**
1. **Création** : Aller dans *Projet > Configuration > Projets* → Créer
2. **Configuration** : Remplir nom, description, client, compte analytique
3. **Étapes** : Définir les étapes du projet via `stage_id`
4. **Équipe** : Ajouter des utilisateurs aux favoris
5. **Suivi** : Les compteurs de tâches se mettent à jour automatiquement
6. **Archivage** : Désactiver via `active = False`

**Menu dans Odoo :** *Projet > Projets > Projets*

**Pièges courants :**
- Oublier de lier un compte analytique (nécessaire pour les feuilles de temps)
- Ne pas définir de client alors que la facturation est prévue
- Archiver un projet avec des tâches actives

**Bonnes pratiques :**
- Toujours créer un compte analytique pour le suivi financier
- Utiliser des noms de projets explicites et courts
- Configurer les étapes de projet dès le début

---

## USE CASE 2 : Gestion des Tâches

### Modèle : `project.task`

**Champs clés :**
- `name` : Titre de la tâche (requis)
- `description` : Description HTML
- `project_id` : Projet parent
- `stage_id` : Étape de la tâche
- `user_ids` : Utilisateurs assignés
- `partner_id` : Contact lié
- `priority` : Priorité ('0'=Basse, '1'=Haute)
- `state` : État ('01_in_progress', '02_changes_requested', '03_approved', '1_done', '1_canceled', '04_waiting_normal')
- `date_deadline` : Date d'échéance
- `date_assign` : Date d'assignation
- `parent_id`, `child_ids` : Relations parent/enfant pour sous-tâches
- `milestone_id` : Jalon associé
- `tag_ids` : Étiquettes

**Workflow complet :**
1. **Création** : *Projet > Tâches* → Créer
2. **Configuration** : Titre, description, projet, étape
3. **Assignation** : Définir `user_ids` et `date_assign`
4. **Planification** : Fixer `date_deadline` et `milestone_id`
5. **Progression** : Déplacer entre les étapes via `stage_id`
6. **État** : Le champ `state` se calcule automatiquement selon l'étape
7. **Finalisation** : État final '1_done' ou '1_canceled'

**Menu dans Odoo :** *Projet > Tâches*

**Pièges courants :**
- Créer des tâches sans les lier à un projet
- Ne pas définir d'échéance pour les tâches importantes  
- Oublier d'assigner les tâches aux bonnes personnes
- Confondre `stage_id` (étape) et `state` (état calculé)

**Bonnes pratiques :**
- Utiliser des titres de tâches descriptifs et actionnables
- Définir systématiquement une échéance et un assigné
- Utiliser les sous-tâches pour décomposer le travail complexe
- Maintenir les descriptions à jour pendant l'exécution

---

## USE CASE 3 : Configuration des Étapes de Tâches

### Modèle : `project.task.type`

**Champs clés :**
- `name` : Nom de l'étape (requis)
- `description` : Description de l'étape
- `sequence` : Ordre d'affichage
- `project_ids` : Projets utilisant cette étape
- `fold` : Plié dans la vue Kanban
- `mail_template_id` : Template email automatique
- `rating_template_id` : Template de demande d'évaluation
- `auto_validation_state` : Validation automatique via feedback client
- `user_id` : Propriétaire de l'étape (pour étapes personnelles)

**Workflow complet :**
1. **Accès** : *Projet > Configuration > Étapes de Tâches*
2. **Création** : Définir nom, description, séquence
3. **Association** : Lier aux projets via `project_ids`
4. **Emails** : Configurer `mail_template_id` pour notifications automatiques
5. **Évaluations** : Activer `rating_template_id` pour feedback client
6. **Kanban** : Organiser l'affichage avec `sequence` et `fold`

**Menu dans Odoo :** *Projet > Configuration > Étapes de Tâches*

**Pièges courants :**
- Créer trop d'étapes (complexité excessive)
- Ne pas définir de séquence logique
- Oublier de lier les étapes aux bons projets
- Supprimer une étape avec des tâches actives

**Bonnes pratiques :**
- Limiter à 4-6 étapes maximum par projet
- Noms d'étapes clairs et orientés action ("À faire", "En cours", "En test", "Terminé")
- Utiliser les templates email pour automatiser les notifications
- Tester le workflow complet avant déploiement

---

## USE CASE 4 : Gestion des Jalons (Milestones)

### Modèle : `project.milestone`

**Champs clés :**
- `name` : Nom du jalon (requis)
- `project_id` : Projet parent (requis)
- `deadline` : Date limite
- `is_reached` : Jalon atteint ou non
- `reached_date` : Date d'atteinte (calculé)
- `task_ids` : Tâches associées
- `task_count`, `done_task_count` : Compteurs de tâches
- `is_deadline_exceeded` : Échéance dépassée (calculé)
- `can_be_marked_as_done` : Peut être marqué terminé (calculé)

**Workflow complet :**
1. **Activation** : Activer les jalons sur le projet
2. **Création** : *Projet > [Projet] > Jalons* → Créer
3. **Configuration** : Nom, échéance, tâches associées
4. **Suivi** : Contrôle automatique des échéances et du pourcentage d'avancement
5. **Validation** : Marquer `is_reached = True` manuellement ou automatiquement
6. **Reporting** : Suivi dans les mises à jour de projet

**Menu dans Odoo :** Dans la vue projet → Onglet "Jalons"

**Pièges courants :**
- Oublier d'activer les jalons sur le projet
- Définir des jalons trop ambitieux ou trop fréquents
- Ne pas associer de tâches aux jalons
- Marquer manuellement sans vérifier l'avancement réel

**Bonnes pratiques :**
- Jalons alignés sur des livrables concrets
- Échéances réalistes avec marge de sécurité
- Révision régulière et ajustement si nécessaire
- Célébrer l'atteinte des jalons importants

---

## USE CASE 5 : Mises à jour de Projet

### Modèle : `project.update`

**Champs clés :**
- `name` : Titre de la mise à jour (requis)
- `status` : Statut ('on_track', 'at_risk', 'off_track', 'on_hold', 'done')
- `progress` : Pourcentage d'avancement (0-100)
- `user_id` : Auteur de la mise à jour
- `description` : Description HTML détaillée
- `date` : Date de la mise à jour
- `project_id` : Projet concerné (requis)
- `task_count`, `closed_task_count` : Compteurs de tâches au moment de la mise à jour
- `color` : Couleur selon le statut (calculé)

**Workflow complet :**
1. **Accès** : *Projet > [Projet]* → "Créer une mise à jour"
2. **Rédaction** : Titre, statut, pourcentage, description
3. **Génération** : Description automatique basée sur les jalons et tâches
4. **Publication** : Validation et envoi aux abonnés
5. **Archivage** : La mise à jour devient `last_update_id` du projet
6. **Historique** : Toutes les mises à jour restent consultables

**Menu dans Odoo :** Dans la vue projet → Bouton "Mises à jour"

**Pièges courants :**
- Mises à jour trop rares ou trop fréquentes
- Statuts incohérents avec la réalité du projet
- Descriptions trop techniques ou pas assez détaillées
- Oubli de mise à jour du pourcentage d'avancement

**Bonnes pratiques :**
- Fréquence régulière (hebdomadaire/bi-hebdomadaire)
- Statuts honnêtes et justifiés
- Description équilibrée : réalisations, problèmes, prochaines étapes
- Utilisation des templates automatiques comme base

---

## Intégrations et fonctionnalités transverses

### Héritages importants :
- **`portal.mixin`** : Accès portail client
- **`mail.thread`** : Suivi des messages et notifications
- **`mail.activity.mixin`** : Activités et rappels
- **`rating.mixin`** : Évaluations clients

### Champs calculés critiques :
- **Compteurs de tâches** : Mise à jour temps réel via `_compute_task_count`
- **États des tâches** : Calcul automatique via `_compute_state` 
- **Indicateurs de jalons** : Surveillance des échéances et avancement

### Sécurité et droits :
- Champs en lecture : `PROJECT_TASK_READABLE_FIELDS`
- Champs en écriture : `PROJECT_TASK_WRITABLE_FIELDS`
- Contrôles d'accès via groupes utilisateurs

Cette architecture modulaire permet une gestion complète du cycle de vie des projets, de la planification initiale jusqu'à la clôture, avec un suivi précis de l'avancement et une communication efficace avec les parties prenantes.