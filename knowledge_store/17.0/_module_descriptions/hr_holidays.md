# Module Odoo 17 : hr_holidays - Gestion des Congés et Absences

## Vue d'ensemble

Le module `hr_holidays` est le système complet de gestion des congés et absences d'Odoo 17. Il permet de gérer les demandes de congés, les allocations de jours de congés, les différents types d'absences et les plans d'accumulation automatique.

---

## USE CASE 1 : Gestion des demandes de congés (hr.leave)

### Description métier
Ce use case couvre la création, validation et suivi des demandes de congés des employés.

### Modèle principal : hr.leave

#### Champs clés :
- **employee_id** : Employé demandeur (Many2one 'hr.employee')
- **holiday_status_id** : Type de congé (Many2one 'hr.leave.type')
- **request_date_from/request_date_to** : Dates de début/fin demandées
- **date_from/date_to** : Dates UTC calculées pour le système
- **number_of_days** : Nombre de jours demandés
- **state** : Statut de la demande (draft/confirm/validate1/validate/refuse/cancel)
- **name/private_name** : Description publique/privée de la demande
- **manager_id** : Responsable validateur
- **validation_type** : Type de validation requis

#### Workflow complet :

1. **Création de la demande**
   - L'employé accède à : **Congés > Mes Congés > Nouvelle Demande**
   - Sélection du type de congé via `holiday_status_id`
   - Saisie des dates via `request_date_from` et `request_date_to`
   - Le système calcule automatiquement `number_of_days`
   - État initial : `draft` ou `confirm` selon le type

2. **Soumission et validation**
   - Passage en état `confirm` si validation requise
   - Si validation par manager : état `validate1` puis `validate`
   - Si validation RH uniquement : direct en `validate`
   - Possibilité de refus : état `refuse`

3. **Calculs automatiques**
   - `_compute_date_from_to()` : Conversion des dates selon le planning
   - `_compute_number_of_days()` : Calcul des jours ouvrés
   - Vérification des soldes disponibles

### Menu Odoo :
- **Congés > Mes Congés > Mes Demandes de Congés**
- **Congés > Congés > Demandes de Congés** (pour les RH)
- **Congés > Rapports > Congés par Employé**

### Pièges courants :
- Les dates `date_from/date_to` sont en UTC, utiliser `request_date_from/request_date_to` pour l'interface
- La validation des soldes se fait via `holiday_status_id.requires_allocation`
- Les permissions dépendent du rôle (Employee/Officer/Manager)

### Bonnes pratiques :
- Toujours vérifier `can_approve` avant validation
- Utiliser `_compute_can_reset` pour les annulations
- Respecter les droits d'accès selon `_mail_post_access = 'read'`

---

## USE CASE 2 : Allocation des congés (hr.leave.allocation)

### Description métier
Gestion des allocations de jours de congés attribués aux employés, soit manuellement soit automatiquement via des plans d'accumulation.

### Modèle principal : hr.leave.allocation

#### Champs clés :
- **employee_id** : Employé bénéficiaire
- **holiday_status_id** : Type de congé alloué
- **number_of_days** : Nombre de jours alloués
- **date_from/date_to** : Période de validité
- **state** : Statut (confirm/validate/refuse)
- **holiday_type** : Mode d'allocation (employee/company/department/category)
- **accrual_plan_id** : Plan d'accumulation lié (si applicable)
- **allocation_type** : Type d'allocation (regular/accrual)

#### Workflow complet :

1. **Allocation manuelle**
   - RH accède à : **Congés > Allocations > Allocations**
   - Création via bouton "Nouveau"
   - Sélection de l'employé et du type de congé
   - Saisie du nombre de jours dans `number_of_days`
   - Définition de la période de validité

2. **Allocation par lots**
   - Sélection `holiday_type = 'company'` ou `'department'`
   - Le système crée automatiquement une allocation par employé concerné
   - Champ `parent_id` pour traçabilité

3. **Validation**
   - Selon `allocation_validation_type` du type de congé
   - Passage en état `validate` après approbation
   - Mise à jour automatique des soldes employés

### Menu Odoo :
- **Congés > Allocations > Allocations**
- **Congés > Allocations > Demandes d'Allocation** (pour les demandes employés)

### Pièges courants :
- Vérifier `requires_allocation = 'yes'` sur le type de congé
- Les allocations en état `draft` ne sont pas comptabilisées
- Attention aux droits sur `employee_requests`

### Bonnes pratiques :
- Utiliser les dates de validité pour les allocations annuelles
- Grouper les allocations par `parent_id` pour faciliter le suivi
- Vérifier `can_approve` pour les validations

---

## USE CASE 3 : Configuration des types de congés (hr.leave.type)

### Description métier
Définition et paramétrage des différents types d'absences et congés disponibles dans l'organisation.

### Modèle principal : hr.leave.type

#### Champs clés :
- **name** : Nom du type de congé
- **requires_allocation** : Nécessite une allocation (yes/no)
- **leave_validation_type** : Type de validation (no_validation/hr/manager/both)
- **allocation_validation_type** : Validation pour les allocations
- **employee_requests** : Demandes d'allocation autorisées (yes/no)
- **request_unit** : Unité de demande (day/half_day/hour)
- **time_type** : Nature du temps (leave/other)
- **unpaid** : Congé non payé
- **responsible_ids** : Responsables RH notifiés
- **sequence** : Ordre d'affichage

#### Workflow de configuration :

1. **Création du type**
   - RH accède à : **Congés > Configuration > Types de Congés**
   - Définition du nom et de la séquence
   - Choix de l'unité de prise (`request_unit`)

2. **Paramétrage des validations**
   - `leave_validation_type` : Qui valide les demandes
   - `allocation_validation_type` : Qui valide les allocations
   - Configuration des `responsible_ids`

3. **Gestion des allocations**
   - `requires_allocation = 'yes'` : Nécessite un solde
   - `requires_allocation = 'no'` : Congés illimités
   - `employee_requests` : Auto-demande d'allocation

4. **Personnalisation avancée**
   - Couleur pour l'affichage calendrier
   - Icône personnalisée via `icon_id`
   - Documents justificatifs avec `support_document`

### Menu Odoo :
- **Congés > Configuration > Types de Congés**

### Champs calculés importants :
- **max_leaves** : Maximum alloué à l'employé connecté
- **leaves_taken** : Jours déjà pris
- **virtual_remaining_leaves** : Solde virtuel (incluant les demandes en attente)

### Pièges courants :
- Un type inactif (`active=False`) reste utilisable sur les enregistrements existants
- `virtual_remaining_leaves` inclut les congés en attente de validation
- La `sequence` détermine l'ordre de sélection par défaut

### Bonnes pratiques :
- Utiliser des séquences logiques (10, 20, 30...)
- Configurer les `responsible_ids` pour les notifications
- Tester la validation avec différents profils utilisateur

---

## USE CASE 4 : Plans d'accumulation automatique (hr.leave.accrual.plan)

### Description métier
Système d'accumulation automatique de jours de congés selon des règles prédéfinies (mensuelle, annuelle, etc.).

### Modèles principaux :
- **hr.leave.accrual.plan** : Plan principal
- **hr.leave.accrual.level** : Niveaux du plan

#### Champs clés hr.leave.accrual.plan :
- **name** : Nom du plan
- **time_off_type_id** : Type de congé concerné
- **accrued_gain_time** : Moment de gain (start_of_period/end_of_period)
- **level_ids** : Niveaux d'accumulation
- **transition_mode** : Mode de transition (immediately/after_period)

#### Champs clés hr.leave.accrual.level :
- **start_count/start_type** : Délai avant activation (X jours/mois/années)
- **added_value** : Nombre de jours/heures ajoutés
- **frequency** : Fréquence (daily/weekly/monthly/yearly)
- **maximum_leave** : Plafond d'accumulation
- **action_with_unused_accruals** : Gestion du report annuel

#### Workflow de configuration :

1. **Création du plan**
   - Accès : **Congés > Configuration > Plans d'Accumulation**
   - Définition du nom et du type de congé lié
   - Choix du moment de gain (`accrued_gain_time`)

2. **Configuration des niveaux**
   - Niveau 1 : Période d'essai (ex: 6 mois, 1.5 jours/mois)
   - Niveau 2 : Employé confirmé (ex: après 1 an, 2.5 jours/mois)
   - Paramétrage des plafonds et reports

3. **Attribution aux employés**
   - Création d'allocation avec `allocation_type = 'accrual'`
   - Le système calcule automatiquement selon le plan
   - Génération d'historique dans les allocations

### Exemple concret :
```python
# Plan "Congés Payés Standards"
# Niveau 1 : Après 6 mois, 2 jours/mois, max 25 jours
# Niveau 2 : Après 3 ans, 2.5 jours/mois, max 30 jours
```

### Menu Odoo :
- **Congés > Configuration > Plans d'Accumulation**

### Pièges courants :
- L'accumulation démarre selon `start_count` et `start_type`
- Les plafonds (`maximum_leave`) bloquent l'accumulation
- Le report annuel dépend de `action_with_unused_accruals`

### Bonnes pratiques :
- Tester les plans sur un employé pilote
- Documenter les règles métier dans le nom du plan
- Prévoir les cas de transition entre niveaux

---

## USE CASE 5 : Tableau de bord employé (hr.employee extensions)

### Description métier
Extensions du modèle employé pour afficher les informations de congés dans le profil employé.

### Modèle : hr.employee (extension via hr.employee.base)

#### Champs ajoutés :
- **leave_manager_id** : Responsable des congés (res.users)
- **remaining_leaves** : Solde total des congés
- **current_leave_state** : État actuel si en congé
- **leave_date_from/leave_date_to** : Dates du congé en cours
- **is_absent** : Absent aujourd'hui
- **allocation_display** : Affichage formaté des allocations

#### Fonctionnalités :

1. **Calcul des soldes**
   - Méthode `_get_remaining_leaves()` : SQL optimisée
   - Agrégation des allocations et consommations
   - Filtrage par types actifs et validés

2. **Détection d'absence**
   - `_compute_leave_status()` : État temps réel
   - Mise à jour de `hr_presence_state`
   - Intégration avec le système de présence

3. **Affichage dans les vues**
   - Kanban employés avec badges de congés
   - Formulaire avec onglet "Congés"
   - Indicateurs visuels sur les absences

### Menu Odoo :
- **Employés > Employés** (onglet Congés dans le formulaire)
- **Employés > Tableau de Bord > Employés en Congés**

### Calculs importants :
```sql
-- Solde = Allocations validées - Congés validés
SELECT sum(h.number_of_days) AS days, h.employee_id
FROM (
    SELECT number_of_days, state, employee_id FROM hr_leave_allocation
    UNION ALL
    SELECT (number_of_days * -1), state, employee_id FROM hr_leave
) h
WHERE h.state='validate'
GROUP BY h.employee_id
```

### Pièges courants :
- `remaining_leaves` ne compte que les types avec `requires_allocation='yes'`
- Les congés en attente ne sont pas dans le calcul de base
- `current_leave_state` peut être vide si pas de congé actuel

### Bonnes pratiques :
- Utiliser `_get_contextual_employee()` pour le contexte utilisateur
- Préférer les méthodes calculées aux requêtes directes
- Vérifier les droits d'accès sur les données sensibles

---

## Règles de sécurité et permissions

### Groupes utilisateurs :
- **hr_holidays.group_hr_holidays_user** : Responsable RH Congés
- **hr_holidays.group_hr_holidays_manager** : Manager Congés
- **base.group_user** : Utilisateur standard

### Règles d'accès spécifiques :
1. **Employé standard** :
   - Voir tous les congés (pas les descriptions privées)
   - Modifier ses propres demandes non validées
   - Ne peut pas valider

2. **Responsable RH** :
   - Valider selon les règles de hiérarchie
   - Accès aux descriptions privées
   - Gestion des allocations

3. **Manager** :
   - Tous droits sur son équipe
   - Cannot validate ses propres congés

### Règles de validation automatique :
- Manager direct si défini
- Responsable départemental
- Responsable RH selon configuration du type

Ce module est central dans la gestion RH d'Odoo et nécessite une configuration précise selon les règles de l'entreprise.