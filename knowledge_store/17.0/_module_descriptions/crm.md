# Module CRM Odoo 17 - Description Métier Complète

## Vue d'ensemble
Le module CRM d'Odoo 17 est un système complet de gestion de la relation client qui gère les leads, opportunités, équipes commerciales et l'assignation automatique. Il permet de suivre le pipeline commercial depuis la génération de prospects jusqu'à la conversion en clients.

---

## USE CASE 1 : Gestion des Leads et Opportunités

### Modèle principal : `crm.lead`
**Menu Odoo :** CRM > Leads ou CRM > Pipeline

### Champs clés :
- **name** : Nom de l'opportunité (obligatoire, indexé avec trigram)
- **type** : 'lead' ou 'opportunity' (détermine le type d'enregistrement)
- **partner_id** : Client lié (Many2one vers res.partner)
- **user_id** : Commercial responsable (Many2one vers res.users)
- **team_id** : Équipe commerciale (Many2one vers crm.team)
- **stage_id** : Étape du pipeline (Many2one vers crm.stage)
- **expected_revenue** : Chiffre d'affaires prévisionnel
- **probability** : Probabilité de succès (0-100%)
- **email_from** : Email du prospect
- **phone**, **mobile** : Coordonnées téléphoniques

### Workflow complet :

1. **Création du Lead**
   - Via formulaire web, email, import ou API
   - Type = 'lead' par défaut si groupe crm.group_use_lead actif
   - Assignation automatique possible selon règles d'équipe

2. **Qualification du Lead**
   - Enrichissement des informations (coordonnées, entreprise)
   - Validation de l'intérêt commercial
   - Possibilité d'utiliser l'enrichissement automatique IAP

3. **Conversion en Opportunité**
   - Changement du type de 'lead' à 'opportunity'
   - Création du partenaire si nécessaire
   - Passage au pipeline de vente

4. **Gestion du Pipeline**
   - Progression à travers les étapes (crm.stage)
   - Mise à jour des probabilités et revenus
   - Suivi des activités et communications

5. **Clôture**
   - Gagné (probability = 100%) ou Perdu (active = False)
   - Synchronisation avec le partenaire créé

### Pièges courants :
- **Fusion de leads** : Attention aux champs dans CRM_LEAD_FIELDS_TO_MERGE
- **Synchronisation partenaire** : Les champs PARTNER_FIELDS_TO_SYNC et PARTNER_ADDRESS_FIELDS_TO_SYNC doivent être cohérents
- **Calcul du revenu proratisé** : Dépend de la date limite et de la probabilité
- **Gestion des doublons** : Vérifier email_from et partner_id avant création

### Bonnes pratiques :
- Utiliser les propriétés (lead_properties) pour des champs métier spécifiques
- Configurer les étapes par équipe pour un meilleur suivi
- Activer l'enrichissement automatique pour gagner du temps
- Utiliser les tags pour catégoriser les leads

---

## USE CASE 2 : Gestion des Équipes Commerciales

### Modèle principal : `crm.team`
**Menu Odoo :** CRM > Configuration > Équipes commerciales

### Champs clés :
- **use_leads** : Utilisation des leads (qualification avant opportunité)
- **use_opportunities** : Utilisation du pipeline d'opportunités
- **assignment_enabled** : Assignation automatique activée
- **assignment_domain** : Domaine de filtre pour l'assignation
- **assignment_max** : Capacité moyenne mensuelle de l'équipe
- **lead_properties_definition** : Définition des propriétés personnalisées

### Workflow complet :

1. **Configuration de l'équipe**
   - Création de l'équipe avec nom et responsable
   - Définition des options : leads et/ou opportunités
   - Configuration du domaine d'assignation si nécessaire

2. **Ajout des membres**
   - Ajout des commerciaux via crm.team.member
   - Définition de la capacité individuelle (assignment_max)
   - Paramétrage des domaines spécifiques par membre

3. **Configuration de l'assignation automatique**
   - Activation globale dans Paramètres CRM
   - Configuration du cron si assignation répétée
   - Test et ajustement des domaines

4. **Suivi des performances**
   - Monitoring des leads non assignés
   - Suivi du dépassement de capacité
   - Analyse des revenus d'opportunités

### Pièges courants :
- **Domaine d'assignation invalide** : Tester le domaine avant sauvegarde
- **Capacité mal calibrée** : Surveiller lead_all_assigned_month_exceeded
- **Conflit de domaines** : Attention aux chevauchements entre membres
- **Cron d'assignation** : Vérifier qu'il est actif pour l'auto-assignation

### Bonnes pratiques :
- Commencer avec des domaines simples puis affiner
- Calibrer les capacités sur données historiques
- Utiliser les propriétés pour des besoins métier spécifiques
- Surveiller régulièrement les statistiques d'équipe

---

## USE CASE 3 : Assignation Automatique des Leads

### Modèles impliqués : `crm.team.member`, `crm.lead`
**Menu Odoo :** CRM > Configuration > Paramètres > Attribution de leads

### Champs clés :
- **assignment_optout** : Exclusion de l'assignation automatique
- **assignment_max** : Capacité individuelle (défaut: 30 leads/30 jours)
- **assignment_domain** : Domaine spécifique au membre
- **lead_month_count** : Nombre de leads assignés ce mois

### Workflow complet :

1. **Configuration globale**
   - Activation dans res.config.settings : crm_use_auto_assignment
   - Choix entre assignation manuelle ou automatique (cron)
   - Configuration de la fréquence si automatique

2. **Paramétrage par membre**
   - Définition de la capacité mensuelle
   - Configuration du domaine de spécialisation
   - Option d'opt-out si nécessaire

3. **Processus d'assignation** (méthode _assign_and_convert_leads)
   - Préparation des domaines (AND entre équipe et membre)
   - Calcul des quotas basés sur work_days et capacité
   - Assignation pondérée aléatoire pour équité
   - Conversion automatique lead → opportunité

4. **Suivi et ajustement**
   - Monitoring des dépassements de capacité
   - Ajustement des paramètres selon performances
   - Analyse de la répartition de charge

### Pièges courants :
- **Domaines trop restrictifs** : Peut laisser des leads non assignés
- **Capacités mal équilibrées** : Risque de surcharge/sous-charge
- **Cron mal configuré** : Vérifier nextcall et interval
- **Work_days invalide** : Doit être entre 0.2 et 30 jours

### Bonnes pratiques :
- Tester l'assignation manuellement avant automatisation
- Commencer avec des capacités conservatives
- Utiliser des domaines complémentaires plutôt qu'exclusifs
- Surveiller les métriques d'assignation régulièrement

---

## USE CASE 4 : Intégration Partenaires

### Modèle : `res.partner` (extension CRM)
**Menu Odoo :** Contacts ou CRM > Clients

### Champs ajoutés :
- **team_id** : Équipe commerciale du partenaire
- **opportunity_ids** : Liste des opportunités
- **opportunity_count** : Nombre d'opportunités (calculé)

### Workflow complet :

1. **Création depuis lead/opportunité**
   - Conversion automatique avec données du lead
   - Synchronisation des champs d'adresse (PARTNER_ADDRESS_FIELDS_TO_SYNC)
   - Héritage de l'équipe commerciale

2. **Synchronisation bidirectionnelle**
   - Modification partenaire → mise à jour des leads/opportunités
   - Modification lead → synchronisation vers partenaire
   - Gestion des conflits de données

3. **Suivi commercial**
   - Vue des opportunités depuis la fiche partenaire
   - Comptage automatique incluant les filiales
   - Action pour accéder au pipeline client

### Pièges courants :
- **Synchronisation partielle** : Vérifier les listes de champs à synchroniser
- **Équipe héritée** : L'équipe vient du parent si contact d'entreprise
- **Comptage récursif** : Inclut les opportunités des contacts liés
- **Performance** : Attention aux calculs sur gros volumes

### Bonnes pratiques :
- Maintenir la cohérence des données de contact
- Utiliser la hiérarchie partenaire pour l'organisation
- Vérifier l'équipe assignée pour le bon suivi commercial
- Nettoyer régulièrement les doublons partenaires

---

## USE CASE 5 : Configuration et Paramétrage

### Modèle : `res.config.settings`
**Menu Odoo :** CRM > Configuration > Paramètres

### Paramètres principaux :

#### Fonctionnalités de base
- **group_use_lead** : Active la distinction leads/opportunités
- **group_use_recurring_revenues** : Revenus récurrents
- **is_membership_multi** : Appartenance multi-équipes

#### Assignation automatique
- **crm_use_auto_assignment** : Active l'assignation règle-based
- **crm_auto_assignment_action** : Manuel ou automatique
- **crm_auto_assignment_interval_*** : Fréquence du cron

#### Modules IAP (Intelligence Artificielle)
- **module_crm_iap_mine** : Génération de leads via IAP
- **module_crm_iap_enrich** : Enrichissement automatique
- **lead_enrich_auto** : Mode d'enrichissement (manuel/auto)

#### Scoring prédictif
- **predictive_lead_scoring_*** : Configuration du scoring IA

### Workflow de configuration :

1. **Configuration initiale**
   - Choix leads vs opportunités directes
   - Activation des fonctionnalités avancées
   - Configuration des modules IAP

2. **Paramétrage assignation**
   - Activation du système d'assignation
   - Configuration du mode et fréquence
   - Test sur équipes pilotes

3. **Optimisation continue**
   - Ajustement des paramètres selon usage
   - Activation progressive des fonctionnalités IA
   - Monitoring des performances

### Bonnes pratiques de configuration :
- Commencer simple puis ajouter progressivement les fonctionnalités
- Tester l'assignation automatique sur une équipe avant généralisation
- Calibrer les paramètres IAP sur échantillon avant activation globale
- Documenter les choix de configuration pour l'équipe

Ce module CRM offre une flexibilité remarquable pour s'adapter aux processus commerciaux variés tout en fournissant des outils d'automatisation et d'intelligence artificielle pour améliorer l'efficacité commerciale.