# Module Odoo 17 : hr_expense
## Description générale
Le module **hr_expense** permet aux employés de créer, soumettre et gérer leurs notes de frais. Il couvre le cycle complet depuis la saisie d'une dépense jusqu'au remboursement, en passant par l'approbation managériale et la comptabilisation.

---

## USE CASE 1 : Création d'une dépense par un employé

### Modèle principal
**hr.expense** - Représente une ligne de dépense individuelle

### Champs clés
- `name` : Description de la dépense (calculée automatiquement depuis le produit)
- `date` : Date de la dépense (par défaut aujourd'hui)
- `employee_id` : Employé concerné (par défaut l'utilisateur connecté)
- `product_id` : Catégorie de dépense (produits avec `can_be_expensed = True`)
- `quantity` : Quantité (défaut = 1)
- `total_amount` : Montant total en devise de l'entreprise
- `total_amount_currency` : Montant en devise originale
- `currency_id` : Devise de la dépense
- `state` : États possibles : `draft`, `reported`, `submitted`, `approved`, `done`, `refused`

### Workflow complet
1. **Création** : État `draft` ("To Report")
2. **Saisie des informations** : 
   - Sélection du produit/catégorie
   - Saisie du montant
   - Ajout de pièces justificatives via `attachment_ids`
3. **Validation automatique** : Vérification des champs obligatoires

### Menu dans Odoo
**Expenses > My Expenses > Expenses**

### Pièges courants
- Un employé doit exister pour l'utilisateur connecté (sinon `ValidationError`)
- Le produit doit avoir `can_be_expensed = True`
- Les pièces justificatives sont fortement recommandées

### Bonnes pratiques
- Utiliser `message_main_attachment_id` pour la pièce principale
- Vérifier `duplicate_expense_ids` pour éviter les doublons
- Utiliser `description` pour les notes internes

---

## USE CASE 2 : Soumission et approbation des notes de frais

### Modèle principal
**hr.expense.sheet** - Rapport de dépenses regroupant plusieurs lignes

### Champs clés
- `name` : Nom du rapport de dépenses
- `expense_line_ids` : Lignes de dépenses associées
- `employee_id` : Employé demandeur
- `user_id` : Manager approbateur (calculé depuis l'employé)
- `state` : `draft`, `submit`, `approve`, `post`, `done`, `cancel`
- `approval_state` : État d'approbation spécifique
- `approval_date` : Date d'approbation
- `total_amount` : Montant total du rapport

### Workflow complet
1. **Regroupement** : Les dépenses `draft` sont ajoutées au rapport
2. **Soumission** : Passage en état `submit` ("Submitted")
3. **Approbation managériale** : Le manager change l'état vers `approve`
4. **Comptabilisation** : Création des écritures comptables (état `post`)
5. **Finalisation** : Paiement et passage en `done`

### Menu dans Odoo
**Expenses > My Expenses > Expense Reports**
**Expenses > Expense Reports to Approve** (pour managers)

### Droits d'accès détaillés
- **Submit** : Employé (ses propres dépenses), Officer (s'il manage l'employé), Manager (toujours)
- **Approve** : Officer (pas les siennes + manage l'employé), Manager (toujours)
- **Post/Done** : Tout utilisateur avec journal défini et état `approve`

### Pièges courants
- Le manager (`user_id`) est calculé automatiquement depuis `employee_id.parent_id.user_id`
- Un utilisateur ne peut pas approuver ses propres dépenses
- Le journal de dépenses doit être configuré (`expense_journal_id`)

### Bonnes pratiques
- Configurer les managers dans la hiérarchie RH
- Définir `expense_manager_id` pour des approbateurs spécifiques
- Utiliser les groupes `group_hr_expense_team_approver` et `group_hr_expense_user`

---

## USE CASE 3 : Comptabilisation et paiement

### Modèle étendu
**account.move** - Écriture comptable générée depuis les dépenses

### Champs ajoutés
- `expense_sheet_id` : Lien vers le rapport de dépenses
- `show_commercial_partner_warning` : Alerte pour partenaire commercial

### Workflow complet
1. **Génération automatique** : Création d'une `account.move` depuis le rapport approuvé
2. **Mode de paiement** :
   - `own_account` : L'employé a payé (créditeur = employé)
   - `company_account` : L'entreprise paie directement (créditeur = fournisseur)
3. **Comptabilisation** : Validation de l'écriture
4. **Paiement** : Règlement via les moyens de paiement configurés

### Menu dans Odoo
**Accounting > Vendors > Bills** (écritures générées)

### Champs de configuration dans res.company
- `expense_journal_id` : Journal des achats pour les dépenses
- `expense_product_id` : Produit par défaut
- `company_expense_allowed_payment_method_line_ids` : Moyens de paiement autorisés

### Pièges courants
- La devise de l'entreprise et celle de la dépense peuvent différer
- Les écritures liées aux dépenses ne peuvent être supprimées individuellement
- Le compte de destination dépend du `payment_mode`

### Bonnes pratiques
- Configurer un journal dédié aux dépenses (type `purchase`)
- Utiliser `_get_expense_account_destination()` pour le compte de contrepartie
- Vérifier `amount_residual` pour le suivi des paiements

---

## USE CASE 4 : Gestion par email (Mail Gateway)

### Configuration
**Settings > Expenses > Let your employees record expenses by email**

### Champs de configuration
- `hr_expense_alias_prefix` : Préfixe de l'alias email
- `hr_expense_alias_domain_id` : Domaine de messagerie
- `hr_expense_use_mailgateway` : Activation de la fonction

### Workflow complet
1. **Envoi email** : Employé envoie un email à `expenses@company.com`
2. **Traitement automatique** : 
   - Création d'une `hr.expense` avec l'expéditeur comme employé
   - Pièce jointe devient `message_main_attachment_id`
   - Extraction du montant depuis l'objet si possible
3. **Finalisation manuelle** : L'employé complète les informations manquantes

### Menu dans Odoo
**Settings > General Settings > Discuss**

### Pièges courants
- L'expéditeur doit être un utilisateur Odoo avec un employé associé
- L'alias doit être configuré avec `alias_contact = 'employees'`
- Le montant n'est pas toujours extrait correctement

### Bonnes pratiques
- Former les employés sur le format d'email attendu
- Utiliser des sujets descriptifs avec le montant
- Vérifier régulièrement les dépenses créées par email

---

## USE CASE 5 : Gestion des droits et hiérarchie

### Groupes de sécurité
- `group_hr_expense_user` : Utilisateur de base (ses dépenses)
- `group_hr_expense_team_approver` : Approbateur d'équipe
- `group_hr_expense_manager` : Manager général

### Champs de hiérarchie
- `employee_id.parent_id` : Manager hiérarchique
- `employee_id.expense_manager_id` : Manager spécifique aux dépenses
- `employee_id.department_id.manager_id` : Manager de département

### Logique de filtrage (`_search_filter_for_expense`)
1. **Utilisateur normal** : Seulement ses propres dépenses
2. **Team Approver** : Ses subordonnés + département géré + assignations spécifiques
3. **Manager/Comptable** : Toutes les dépenses de l'entreprise

### Menu dans Odoo
**Settings > Users & Companies > Users** (configuration des managers)

### Pièges courants
- `expense_manager_id` doit avoir le groupe approprié
- La hiérarchie doit être cohérente entre employés et utilisateurs
- Les droits se cumulent selon les groupes

### Bonnes pratiques
- Maintenir une hiérarchie RH claire
- Utiliser `expense_manager_id` pour des cas spéciaux
- Tester les droits avec différents profils utilisateur

---

## Configuration générale recommandée

### Dans res.config.settings
1. **Journal** : Créer un journal "Dépenses" de type achat
2. **Produit** : Configurer un produit générique "Frais divers"
3. **Moyens de paiement** : Activer virement/chèque pour remboursements
4. **Mail gateway** : Configurer l'alias si nécessaire

### Données de base
1. **Catégories de produits** : Créer des produits avec `can_be_expensed = True`
2. **Employés** : Associer chaque utilisateur à un employé
3. **Hiérarchie** : Définir les managers dans la fiche employé

Cette documentation couvre les aspects essentiels du module hr_expense d'Odoo 17 avec tous les détails techniques nécessaires pour une implémentation réussie.