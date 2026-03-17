# Module hr_contract - Gestion des Contrats Employés

Le module `hr_contract` est un module fondamental d'Odoo qui gère les contrats de travail des employés. Il étend les fonctionnalités RH de base en ajoutant la dimension contractuelle complète.

## USE CASE 1 : Création et Gestion d'un Nouveau Contrat

### Modèle Principal
- **Modèle** : `hr.contract`
- **Description** : Contrat de travail d'un employé

### Champs Clés
- `name` : Référence du contrat (obligatoire)
- `employee_id` : Employé concerné (Many2one vers hr.employee)
- `date_start` : Date de début (obligatoire, par défaut aujourd'hui)
- `date_end` : Date de fin (optionnelle pour CDI)
- `trial_date_end` : Fin de période d'essai
- `wage` : Salaire mensuel brut (obligatoire, en devise)
- `state` : Statut ('draft', 'open', 'close', 'cancel')
- `contract_type_id` : Type de contrat (CDD, CDI, etc.)
- `structure_type_id` : Type de structure salariale (pour la paie)
- `resource_calendar_id` : Horaire de travail
- `kanban_state` : État Kanban ('normal', 'done', 'blocked')

### Workflow Complet

**Étape 1 : Création**
- Menu : *Employés > Contrats > Contrats*
- Cliquer "Créer"
- Renseigner : nom du contrat, employé, date de début, salaire
- État : "Nouveau" (draft)

**Étape 2 : Configuration**
- Le système copie automatiquement depuis l'employé :
  - Département (`department_id`)
  - Poste (`job_id`) 
  - Horaire (`resource_calendar_id`)
  - Entreprise (`company_id`)
- Définir type de contrat et structure salariale

**Étape 3 : Activation**
- Passer à "En cours" (open) manuellement ou automatiquement à la date de début
- Le contrat devient le contrat actuel de l'employé (`contract_id`)

**Étape 4 : Suivi**
- Kanban state "Vert" : contrat à venir activé
- Kanban state "Rouge" : problème ou expiration proche

**Étape 5 : Fermeture**
- À la date de fin : passage automatique à "Expiré" (close)
- Ou annulation manuelle : "Annulé" (cancel)

### Menu dans Odoo
- **Principal** : *Employés > Contrats > Contrats*
- **Employé** : Onglet "Contrats" sur la fiche employé
- **Reporting** : *Employés > Reporting > Contrats*

### Pièges Courants
1. **Chevauchement de contrats** : Deux contrats actifs simultanément
2. **Calendrier incohérent** : `calendar_mismatch = True` si différent de l'employé
3. **Structure salariale manquante** : Problèmes pour la paie
4. **Dates incohérentes** : Date fin < date début

### Bonnes Pratiques
- Toujours définir une référence unique (`name`)
- Vérifier la cohérence des dates
- Synchroniser les calendriers employé/contrat
- Définir la structure salariale dès la création

---

## USE CASE 2 : Gestion des Contrats Multiples et Historique

### Modèle Étendu
- **hr.employee** : Ajout des champs contractuels
- **hr.contract.history** : Historique des contrats (référencé mais non détaillé)

### Champs Clés Employé
- `contract_ids` : Tous les contrats (One2many)
- `contract_id` : Contrat actuel (Many2one)
- `contracts_count` : Nombre de contrats
- `first_contract_date` : Date du premier contrat
- `contract_warning` : Alerte contrat (booléen)
- `calendar_mismatch` : Incohérence calendrier

### Workflow Complet

**Étape 1 : Consultation Historique**
- Fiche employé > Onglet "Contrats"
- Vue liste de tous les contrats (`contract_ids`)
- Compteur visible : `contracts_count`

**Étape 2 : Détermination du Contrat Actuel**
- Calcul automatique du `contract_id` basé sur :
  - État 'open'
  - Dates de validité
  - Priorité au plus récent

**Étape 3 : Calcul de la Date de Premier Contrat**
- Méthode `_get_first_contract_date()`
- Ignore les contrats annulés
- Gère les écarts entre contrats (max 4 jours)
- Stocké dans `first_contract_date`

**Étape 4 : Gestion des Transitions**
- Renouvellement : nouveau contrat avec date_start = ancien date_end + 1
- Promotion : nouveau contrat avec nouveau salaire/poste
- Fin de période d'essai : passage automatic draft > open

### Menu dans Odoo
- **Employé** : Smart button "X Contrats" sur la fiche
- **Historique** : *Employés > Reporting > Historique des Contrats*
- **Analyse** : Graphiques et tableaux croisés dynamiques

### Pièges Courants
1. **Contrats orphelins** : Contrats sans date de fin qui traînent
2. **Mauvais contrat actuel** : Calcul incorrect du `contract_id`
3. **Écarts non gérés** : Périodes sans contrat non identifiées
4. **Performance** : Requêtes lourdes sur gros volumes

### Bonnes Pratiques
- Fermer explicitement les anciens contrats
- Utiliser les états Kanban pour le suivi
- Éviter les chevauchements de dates
- Monitorer les alertes `contract_warning`

---

## USE CASE 3 : Intégration avec les Calendriers et Planification

### Modèles Concernés
- **resource.resource** : Ressource (étendu)
- **resource.calendar** : Calendrier de travail
- **resource.calendar.leaves** : Congés du calendrier

### Champs Clés Calendrier
- `contracts_count` : Nombre de contrats utilisant ce calendrier
- Liaison avec `hr.contract.resource_calendar_id`

### Workflow Complet

**Étape 1 : Attribution du Calendrier**
- Lors de la création du contrat
- Copie depuis l'employé par défaut (`_compute_employee_contract`)
- Modifiable manuellement

**Étape 2 : Détection d'Incohérence**
- Calcul automatique `calendar_mismatch`
- Alerte si calendrier contrat ≠ calendrier employé
- Affichage d'un warning sur l'interface

**Étape 3 : Gestion des Périodes de Validité**
- Méthode `_get_calendars_validity_within_period()`
- Calcule les calendriers applicables sur une période
- Prend en compte les contrats successifs

**Étape 4 : Transfert de Congés**
- Méthode `transfer_leaves_to()` sur les calendriers
- Transfère les congés d'un calendrier à un autre
- Utile lors des changements de contrat

**Étape 5 : Planification des Ressources**
- Intégration avec le module resource
- Calcul des disponibilités par contrat
- Gestion des fuseaux horaires

### Menu dans Odoo
- **Calendriers** : *Employés > Configuration > Calendriers de Travail*
- **Ressources** : *Employés > Configuration > Ressources*
- **Action** : Smart button "Contrats" sur le calendrier

### Pièges Courants
1. **Fuseaux horaires** : Calculs erronés entre TZ différentes  
2. **Contrats chevauchants** : Calendriers multiples sur même période
3. **Congés perdus** : Non transférés lors changement calendrier
4. **Performance** : Calculs lourds sur longues périodes

### Bonnes Pratiques
- Synchroniser calendriers employé/contrat
- Planifier les changements de calendrier
- Transférer les congés lors des transitions
- Utiliser les bons fuseaux horaires

---

## USE CASE 4 : États et Suivi Kanban des Contrats

### Modèle de Gestion d'État
- **hr.contract** : Champs `state` et `kanban_state`

### États Disponibles
**state (Statut Principal)**
- `draft` : Nouveau
- `open` : En cours  
- `close` : Expiré
- `cancel` : Annulé

**kanban_state (État Kanban)**
- `normal` : Gris (normal)
- `done` : Vert (validé)
- `blocked` : Rouge (bloqué)

### Workflow Complet

**Étape 1 : Création en Draft**
- Nouveau contrat créé en état "draft"
- kanban_state = "normal" par défaut
- Pas encore actif

**Étape 2 : Validation Incoming**
- Passer kanban_state à "done" (vert)
- Signifie : "Sera activé à la date de début"
- Contrat futur validé

**Étape 3 : Activation Automatique**
- À la date_start : passage draft + vert → open
- Devient le contrat actuel de l'employé
- Visible dans les plannings

**Étape 4 : Alerte Expiration**
- Proche de date_end : kanban_state → "blocked" (rouge)
- Alerte sur vue Kanban employés
- `contract_warning = True` sur l'employé

**Étape 5 : Fermeture**
- À date_end : open → close automatiquement
- Ou annulation manuelle → cancel

### Menu dans Odoo
- **Vue Kanban** : *Employés > Employés* (colonnes par département)
- **Vue Contrats** : *Employés > Contrats > Contrats*
- **Filtres** : Par état, par statut Kanban

### Logique Métier des États
```python
# Combinaisons signification :
- draft + normal : Nouveau contrat en attente
- draft + done : Contrat futur validé (incoming)  
- open + normal : Contrat actif normal
- open + blocked : Contrat actif avec problème
- close + normal : Contrat terminé normalement
```

### Pièges Courants
1. **États incohérents** : draft + blocked sans raison
2. **Transitions ratées** : Contrat draft non activé automatiquement
3. **Alertes ignorées** : kanban_state rouge non traité
4. **Mauvaise interprétation** : Confondre state et kanban_state

### Bonnes Pratiques
- Valider les contrats futurs (draft → done)
- Surveiller les alertes rouges régulièrement  
- Automatiser les transitions par workflows
- Former les utilisateurs sur les états

---

## USE CASE 5 : Intégration Paie et Structure Salariale

### Modèles Liés
- **hr.payroll.structure.type** : Type de structure salariale
- **hr.contract** : Champ `structure_type_id`

### Champs Spécialisés
- `structure_type_id` : Type de structure salariale
- `wage` : Salaire de base
- `contract_wage` : Salaire calculé du contrat
- `currency_id` : Devise (liée à l'entreprise)
- `company_country_id` : Pays de l'entreprise
- `country_code` : Code pays

### Workflow Complet

**Étape 1 : Attribution Structure**
- Calcul automatique `_compute_structure_type_id()`
- Basé sur le pays de l'entreprise (`company_id.country_id`)
- Recherche de la première structure du pays
- Modifiable manuellement

**Étape 2 : Définition Salaire**
- Saisie du `wage` (salaire mensuel brut)
- Calcul du `contract_wage` selon le type
- Prise en compte de la devise

**Étape 3 : Facteur de Coût**
- Méthode `_get_salary_costs_factor()`
- Retourne 12.0 par défaut (annualisation)
- Utilisé pour calculs budgétaires

**Étape 4 : Génération Bulletins**
- Structure salariale détermine les rubriques
- Salaire de base pour calculs
- Intégration avec hr_payroll

### Menu dans Odoo
- **Structures** : *Paie > Configuration > Structures Salariales*
- **Contrats** : Champ "Type de Structure Salariale"
- **Paie** : Génération bulletins depuis contrat

### Calculs Automatiques
```python
# Logique structure par pays :
def _default_salary_structure(country_id):
    return self.env['hr.payroll.structure.type'].search([
        ('country_id', '=', country_id)
    ], limit=1)
```

### Pièges Courants
1. **Structure manquante** : Pas de structure pour le pays
2. **Devise incohérente** : Salaire dans mauvaise devise
3. **Facteur erroné** : Mauvais calcul annuel/mensuel
4. **Réglementations** : Non respect règles locales

### Bonnes Pratiques
- Configurer structures par pays en amont
- Vérifier cohérence devise/pays
- Tester calculs sur contrats pilotes
- Respecter réglementations locales

---

## CONFIGURATION RECOMMANDÉE

### Permissions et Groupes
- `hr.group_hr_user` : Accès lecture contrats
- `hr_contract.group_hr_contract_manager` : Gestion complète
- Responsable RH (`hr_responsible_id`) : Validation contrats

### Données de Base Essentielles
1. **Types de contrats** : CDI, CDD, Stage, etc.
2. **Structures salariales** : Par pays/région
3. **Calendriers de travail** : Temps plein, temps partiel
4. **Départements et postes** : Organisation RH

### Automatisations Recommandées
- Activation automatique des contrats à leur date de début
- Alerte avant expiration (workflow email)
- Calcul automatique du contrat actuel
- Synchronisation calendriers employé/contrat

Ce module est critique pour toute organisation avec des employés car il constitue la base légale et administrative de la relation de travail dans Odoo.