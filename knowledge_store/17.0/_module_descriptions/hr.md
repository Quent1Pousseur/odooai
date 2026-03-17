# MODULE ODOO 17 : HR - GESTION DES EMPLOYÉS

## VUE D'ENSEMBLE

Le module HR est le cœur de la gestion des ressources humaines dans Odoo. Il gère les informations des employés avec une architecture à trois niveaux : `hr.employee` (données complètes et privées), `hr.employee.public` (vue publique limitée), et `hr.employee.base` (modèle abstrait commun).

---

## USE CASE 1 : CRÉATION ET GESTION D'UN EMPLOYÉ

### Modèle principal
- **Modèle** : `hr.employee`
- **Héritage** : `hr.employee.base`, `mail.thread.main.attachment`, `mail.activity.mixin`, `resource.mixin`, `avatar.mixin`

### Champs clés pour la création
```python
# Informations de base
name = fields.Char()  # Nom de l'employé
active = fields.Boolean()  # Actif/Inactif
company_id = fields.Many2one('res.company')  # Société
department_id = fields.Many2one('hr.department')  # Département
job_id = fields.Many2one('hr.job')  # Poste
job_title = fields.Char()  # Titre du poste
user_id = fields.Many2one('res.users')  # Utilisateur associé
resource_id = fields.Many2one('resource.resource')  # Ressource
```

### Workflow complet
1. **Accès au menu** : Employés → Employés → Employés
2. **Création** :
   - Cliquer sur "Créer"
   - Remplir les champs obligatoires :
     - `name` : Nom de l'employé
     - `company_id` : Sélectionner la société
   - Optionnel mais recommandé :
     - `department_id` : Département
     - `job_id` : Poste
     - `user_id` : Associer à un utilisateur Odoo

3. **Configuration avancée** :
   - Onglet "Informations de travail" : adresse, téléphones, email
   - Onglet "Informations privées" : données personnelles (accès restreint)
   - Onglet "Paramètres RH" : manager, coach, calendrier

### Menu dans Odoo
```
Employés
├── Employés
│   ├── Employés (hr.employee)
│   ├── Départements (hr.department)
│   └── Postes de travail (hr.job)
├── Rapports
└── Configuration
```

### Pièges courants
- **Sécurité** : Les champs privés nécessitent le groupe `hr.group_hr_user`
- **Resource** : La création d'un employé crée automatiquement une ressource
- **User** : L'association utilisateur/employé est bidirectionnelle
- **Company** : Contrainte : un utilisateur = un employé par société

### Bonnes pratiques
- Toujours définir `company_id` lors de la création
- Utiliser les groupes de sécurité appropriés
- Maintenir la cohérence entre `user_id` et `work_email`

---

## USE CASE 2 : GESTION DES DÉPARTEMENTS

### Modèle
- **Modèle** : `hr.department`
- **Héritage** : `mail.thread`

### Champs clés
```python
name = fields.Char(required=True)  # Nom du département
complete_name = fields.Char()  # Nom complet hiérarchique
parent_id = fields.Many2one('hr.department')  # Département parent
manager_id = fields.Many2one('hr.employee')  # Manager
member_ids = fields.One2many('hr.employee', 'department_id')  # Membres
total_employee = fields.Integer()  # Nombre total d'employés
```

### Workflow complet
1. **Accès** : Employés → Employés → Départements
2. **Création hiérarchique** :
   - Créer le département racine : `name = "Direction Générale"`
   - Créer des sous-départements : 
     - `parent_id = Direction Générale`
     - `name = "Ressources Humaines"`
3. **Assignment du manager** :
   - `manager_id` : Sélectionner l'employé manager
   - Auto-abonnement du manager aux notifications

### Fonctionnalités spéciales
- **Hiérarchie** : Structure arborescente avec `parent_path`
- **Auto-assignation** : Changement de manager → mise à jour automatique des employés
- **Comptage automatique** : `total_employee` calculé dynamiquement

### Pièges courants
- **Récursion** : Contrainte empêche les départements circulaires
- **Manager** : Changement de manager affecte tous les employés du département
- **Suppression** : Vérifier les employés assignés avant suppression

---

## USE CASE 3 : VUE PUBLIQUE DES EMPLOYÉS

### Modèle
- **Modèle** : `hr.employee.public`
- **Type** : Vue SQL (pas de table physique)
- **Héritage** : `hr.employee.base`

### Champs accessibles
```python
# Champs publics (lecture seule)
name, department_id, job_id, job_title, work_email, work_phone
mobile_phone, work_location_id, image_*, avatar_*

# Champs calculés spécifiques
is_manager = fields.Boolean()  # Est-ce un manager
employee_id = fields.Many2one('hr.employee')  # Lien vers l'employé privé
```

### Workflow d'accès
1. **Utilisateurs normaux** : Voient uniquement `hr.employee.public`
2. **RH** : Accès complet à `hr.employee`
3. **Managers** : Accès étendu aux subordonnés via `is_manager`

### Génération de la vue SQL
```sql
CREATE VIEW hr_employee_public AS (
    SELECT emp.id, emp.name, emp.department_id, ...
    FROM hr_employee emp
)
```

### Sécurité
- **Auto-restriction** : Seules les données publiques sont exposées
- **Calcul dynamique** : `is_manager` basé sur la hiérarchie
- **Performance** : Vue optimisée pour les accès fréquents

---

## USE CASE 4 : INTÉGRATION AVEC RES.USERS

### Extension du modèle utilisateur
```python
# Dans res.users
employee_ids = fields.One2many('hr.employee', 'user_id')
employee_id = fields.Many2one('hr.employee')  # Employé de la société active

# Champs miroirs
job_title = fields.Char(related='employee_id.job_title')
work_phone = fields.Char(related='employee_id.work_phone')
department_id = fields.Many2one(related='employee_id.department_id')
```

### Workflow d'association
1. **Création utilisateur** → Peut créer automatiquement un employé
2. **Multi-société** : Un utilisateur peut avoir plusieurs employés
3. **Employé actif** : Basé sur la société courante (`company_id`)

### Champs synchronisés
- **Professionnels** : `work_email`, `work_phone`, `mobile_phone`, `job_title`
- **Privés** : `private_email`, `private_phone`, données personnelles
- **Organisationnels** : `department_id`, `manager_id`, `coach_id`

### Listes de champs contrôlées
```python
HR_READABLE_FIELDS = ['active', 'child_ids', 'employee_id', ...]
HR_WRITABLE_FIELDS = ['additional_note', 'private_street', ...]
```

---

## USE CASE 5 : DONNÉES PERSONNELLES ET SÉCURITÉ

### Champs privés (groupe hr.group_hr_user)
```python
# Adresse privée
private_street, private_street2, private_city
private_state_id, private_zip, private_country_id

# Contact privé
private_phone, private_email

# Données personnelles
gender, marital, birthday, place_of_birth, country_of_birth
spouse_complete_name, spouse_birthdate, children

# Documents d'identité
identification_id, passport_id, ssnid, sinid
permit_no, visa_no, visa_expire, work_permit_expiration_date
```

### Workflow de sécurité
1. **Groupes d'accès** :
   - Utilisateur normal : `hr.employee.public` uniquement
   - RH : `hr.group_hr_user` → accès à `hr.employee`
   - Manager : accès étendu aux subordonnés

2. **Protection des données** :
   - `groups="hr.group_hr_user"` sur tous les champs sensibles
   - Prefetch limité pour éviter les fuites
   - `related_sudo=False` sur les champs utilisateur

### Bonnes pratiques de sécurité
- **Principe de moindre privilège** : Accès minimal par défaut
- **Audit trail** : `tracking=True` sur les champs sensibles
- **Séparation des rôles** : RH vs Managers vs Employés

---

## USE CASE 6 : GESTION DE LA PRÉSENCE ET ACTIVITÉ

### Champs de présence
```python
hr_presence_state = fields.Selection([
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('to_define', 'To Define')
])

hr_icon_display = fields.Selection([
    ('presence_present', 'Present'),
    ('presence_absent_active', 'Present but not active'),
    ('presence_absent', 'Absent'),
    ('presence_to_define', 'To define'),
    ('presence_undetermined', 'Undetermined')
])

last_activity = fields.Date()
last_activity_time = fields.Char()
newly_hired = fields.Boolean()  # Embauché depuis moins de 90 jours
```

### Calculs automatiques
```python
def _compute_newly_hired(self):
    new_hire_date = fields.Datetime.now() - timedelta(days=90)
    for employee in self:
        employee.newly_hired = employee.create_date > new_hire_date
```

### Intégration avec le module ressource
- **Calendrier de travail** : `resource_calendar_id`
- **Fuseau horaire** : `tz` depuis la ressource
- **Gestion des congés** : Base pour les modules de congés

---

## MENUS COMPLETS DANS ODOO

```
Employés (app_menu)
├── Employés
│   ├── Employés (/hr/employee)
│   │   └── Actions : Créer, Importer, Filtrer, Grouper
│   ├── Départements (/hr/department)  
│   │   └── Vue kanban avec hiérarchie
│   └── Postes de travail (/hr/job)
├── Rapports
│   ├── Employés par département
│   └── Organigramme
└── Configuration
    ├── Paramètres RH
    ├── Lieux de travail
    └── Types d'employé
```

---

## CONSEILS D'IMPLÉMENTATION

### Performance
- Utiliser `hr.employee.public` pour les vues publiques
- Index sur `department_id`, `user_id`, `company_id`
- Éviter les calculs coûteux dans les vues liste

### Extensibilité
- Hériter de `hr.employee.base` pour les modules tiers
- Respecter les groupes de sécurité existants
- Utiliser les hooks `_compute_*` pour les calculs personnalisés

### Maintenance
- Surveiller les contraintes de cohérence user/employee
- Nettoyer régulièrement les ressources orphelines
- Monitorer les permissions sur les données sensibles

Ce module HR constitue la fondation de tous les autres modules RH d'Odoo (congés, évaluations, recrutement, paie, etc.).