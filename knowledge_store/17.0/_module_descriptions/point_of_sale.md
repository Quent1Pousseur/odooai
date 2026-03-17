# Module Point of Sale (POS) d'Odoo 17 - Documentation Métier Complète

## Vue d'ensemble du module
Le module Point of Sale d'Odoo 17 est un système de caisse complet permettant de gérer les ventes en magasin physique. Il couvre la configuration des caisses, la gestion des sessions, la prise de commandes et les paiements.

## USE CASE 1 : Configuration d'un Point de Vente

### Modèle principal : `pos.config`
**Menu Odoo :** Point of Sale > Configuration > Points de Vente

### Champs clés :
- `name` : Nom du point de vente (requis)
- `picking_type_id` : Type d'opération stock (sortie par défaut)
- `journal_id` : Journal comptable POS (POSS par défaut)
- `invoice_journal_id` : Journal de facturation
- `currency_id` : Devise (calculée depuis le journal)
- `payment_method_ids` : Méthodes de paiement autorisées
- `iface_cashdrawer` : Ouverture automatique du tiroir-caisse
- `iface_print_auto` : Impression automatique des reçus
- `cash_control` : Contrôle de caisse activé
- `module_pos_restaurant` : Mode restaurant
- `module_pos_discount` : Module remises

### Workflow complet :
1. **Création** : Point of Sale > Configuration > Points de Vente > Créer
2. **Configuration de base** :
   - Définir le nom (ex: "Caisse Magasin 1")
   - Sélectionner l'entrepôt et le type d'opération
   - Configurer les journaux comptables
3. **Méthodes de paiement** :
   - Ajouter Cash, Carte Bancaire, etc.
   - Paramétrer les journaux associés
4. **Interface utilisateur** :
   - Activer tiroir-caisse si nécessaire
   - Configurer l'impression automatique
   - Définir la catégorie de produits par défaut
5. **Modules additionnels** :
   - Activer restaurant si besoin
   - Activer contrôle des remises

### Pièges courants :
- **Erreur journal manquant** : Vérifier qu'un journal POSS existe
- **Devise incompatible** : S'assurer que la devise du journal correspond
- **Type d'opération incorrect** : Doit être de type "sortie"

### Bonnes pratiques :
- Un point de vente par caisse physique
- Nommer clairement (lieu + numéro)
- Tester la configuration avant mise en production
- Sauvegarder la configuration via duplication

## USE CASE 2 : Gestion des Sessions de Caisse

### Modèle principal : `pos.session`
**Menu Odoo :** Point of Sale > Tableau de Bord > Sessions

### Champs clés :
- `name` : ID de session (auto-généré)
- `config_id` : Point de vente associé (requis)
- `user_id` : Utilisateur qui ouvre (défaut : utilisateur courant)
- `state` : États ('opening_control', 'opened', 'closing_control', 'closed')
- `start_at` : Date/heure d'ouverture
- `stop_at` : Date/heure de fermeture
- `cash_register_balance_start` : Solde initial caisse
- `cash_register_balance_end_real` : Solde final réel
- `cash_register_balance_end` : Solde théorique calculé
- `cash_register_difference` : Différence théorique/réel
- `sequence_number` : Numéro de séquence des commandes
- `access_token` : Token de sécurité

### Workflow complet :
1. **Ouverture de session** :
   ```
   État : opening_control
   Action : action_pos_session_open()
   ```
   - Point of Sale > Tableau de Bord > Nouvelle Session
   - Sélectionner le point de vente
   - Saisir le montant initial si contrôle de caisse activé
   - Notes d'ouverture optionnelles

2. **Session en cours** :
   ```
   État : opened
   ```
   - Prise de commandes
   - Encaissement
   - Suivi temps réel

3. **Contrôle de fermeture** :
   ```
   État : closing_control
   Action : action_pos_session_closing_control()
   ```
   - Vérification solde caisse
   - Saisie montant final réel
   - Notes de fermeture

4. **Fermeture définitive** :
   ```
   État : closed
   Action : action_pos_session_close()
   ```
   - Génération écriture comptable
   - Mise à jour stocks
   - Verrouillage session

### Relations importantes :
- `order_ids` : One2many vers `pos.order`
- `statement_line_ids` : Lignes de relevé bancaire
- `picking_ids` : Bons de livraison associés
- `move_id` : Écriture comptable générée

### Pièges courants :
- **Session non fermée** : Impossible d'ouvrir nouvelle session sur même POS
- **Différence de caisse importante** : Vérifier saisie montant final
- **Commandes orphelines** : Système de "rescue session" automatique
- **Stocks non synchronisés** : Paramètre `update_stock_at_closing`

### Bonnes pratiques :
- Une session par jour/équipe
- Fermer systématiquement les sessions
- Contrôler régulièrement les différences de caisse
- Documenter les écarts dans les notes

## USE CASE 3 : Prise de Commandes

### Modèle principal : `pos.order`
**Menu Odoo :** Point of Sale > Commandes > Commandes

### Champs clés :
- `name` : Numéro de commande (auto)
- `pos_reference` : Référence POS
- `session_id` : Session associée (requis)
- `partner_id` : Client (optionnel)
- `user_id` : Vendeur
- `date_order` : Date/heure commande
- `lines` : Lignes de commande (One2many)
- `amount_total` : Montant total TTC
- `amount_tax` : Montant taxes
- `amount_paid` : Montant payé
- `amount_return` : Montant rendu
- `state` : État ('draft', 'paid', 'done', 'invoiced')
- `sequence_number` : Numéro de séquence
- `fiscal_position_id` : Position fiscale

### Workflow complet :
1. **Interface POS** : Point of Sale > Tableau de Bord > Session > Nouvelle Commande

2. **Ajout produits** :
   - Scan code-barres ou sélection catalogue
   - Modification quantités
   - Application remises
   - Gestion variantes/options

3. **Sélection client** (optionnel) :
   - Recherche par nom/email
   - Création client à la volée
   - Application tarifs/remises spécifiques

4. **Validation commande** :
   - Vérification montants
   - Application position fiscale
   - Génération numéro séquence

5. **Paiement** :
   - Sélection méthode(s) paiement
   - Paiement partiel/multiple autorisé
   - Calcul monnaie à rendre

6. **Finalisation** :
   - Impression ticket
   - Mise à jour stocks (si configuré)
   - Passage état 'paid' ou 'done'

### Structure données UI vers Backend :
```python
ui_order = {
    'name': 'Order 00001-001-0001',
    'pos_session_id': 1,
    'user_id': 2,
    'partner_id': False,
    'lines': [...],  # Lignes de commande
    'amount_total': 23.50,
    'amount_paid': 25.00,
    'amount_return': 1.50,
    'date_order': '2024-01-15T14:30:00',
}
```

### Méthode de traitement :
`_process_order(order, draft, existing_order)` convertit les données UI en objet Odoo.

### Pièges courants :
- **Session fermée** : Génération automatique "rescue session"
- **Stock insuffisant** : Vérification avant validation
- **Taxes incorrectes** : Mapping position fiscale
- **Paiement incomplet** : Validation montant payé >= total

### Bonnes pratiques :
- Valider systématiquement les montants
- Utiliser codes-barres pour rapidité
- Former utilisateurs sur gestion retours
- Configurer impression automatique si nécessaire

## USE CASE 4 : Configuration Système via Paramètres

### Modèle principal : `res.config.settings`
**Menu Odoo :** Paramètres > Point of Sale

### Champs de configuration globaux :
- `update_stock_quantities` : Mise à jour stock (temps réel/fermeture session)
- `account_default_pos_receivable_account_id` : Compte client par défaut POS
- `sale_tax_id` : Taxe par défaut
- `barcode_nomenclature_id` : Nomenclature codes-barres

### Champs spécifiques POS (`pos_config_id`) :
- `pos_module_pos_discount` : Module remises
- `pos_module_pos_hr` : Module RH (vendeurs)
- `pos_module_pos_restaurant` : Mode restaurant
- `pos_cash_control` : Contrôle caisse
- `pos_iface_cashdrawer` : Tiroir-caisse
- `pos_iface_print_auto` : Impression automatique

### Workflow configuration :
1. **Accès** : Paramètres généraux > Point of Sale
2. **Sélection POS** : Choisir point de vente à configurer
3. **Configuration modules** :
   - Activer modules nécessaires
   - Installation automatique si requis
4. **Paramètres comptables** :
   - Journaux par défaut
   - Comptes de produits
   - Taxes par défaut
5. **Interface utilisateur** :
   - Périphériques (tiroir, imprimante)
   - Affichage client
   - Navigation tactile
6. **Sauvegarde** : Validation applique à tous les POS sélectionnés

### Pièges courants :
- **Modules manquants** : Installation automatique peut échouer
- **Comptes comptables** : Doivent exister avant configuration
- **Périphériques** : Tester connectivité avant activation
- **Multi-devises** : Cohérence entre journaux et devises

### Bonnes pratiques :
- Configurer en environnement de test d'abord
- Documenter les paramètres spécifiques
- Former les utilisateurs après changement
- Backup avant modification importante

## USE CASE 5 : Rapports et Analyses

### Modèle principal : `report.point_of_sale.report_saledetails`
**Menu Odoo :** Point of Sale > Rapports > Z Report

### Méthode principale :
`get_sale_details(date_start, date_stop, config_ids, session_ids)`

### Paramètres :
- `date_start` : Date début (défaut : aujourd'hui 00:00)
- `date_stop` : Date fin (défaut : date_start + 23:59:59)
- `config_ids` : IDs points de vente
- `session_ids` : IDs sessions

### Données retournées :
```python
{
    'total': 1250.50,  # CA total
    'products_sold': {
        'product_1': {'qty': 10, 'total': 150.0},
        # ...
    },
    'taxes': {
        'base_amount': 1000.0,
        'taxes': {'TVA 20%': 200.0}
    },
    'payments': [
        {'name': 'Cash', 'total': 500.0, 'cash': True},
        {'name': 'Card', 'total': 750.5, 'cash': False}
    ],
    'refund_done': {...},  # Remboursements
    'sessions': [...]  # Détail sessions
}
```

### Workflow génération rapport :
1. **Accès** : Point of Sale > Rapports > Z Report
2. **Filtres** :
   - Période (date début/fin)
   - Points de vente spécifiques
   - Sessions spécifiques
3. **Génération** :
   - Calcul automatique totaux
   - Regroupement par méthode paiement
   - Détail taxes et produits
4. **Export** : PDF, Excel selon besoin

### Métriques calculées :
- **Chiffre d'affaires** : Somme `amount_total` commandes payées
- **Produits vendus** : Quantités et montants par produit
- **Répartition paiements** : Par méthode de paiement
- **Taxes collectées** : Détail par taux de taxe
- **Remboursements** : Montant et détail

### Pièges courants :
- **Fuseaux horaires** : Conversion UTC nécessaire
- **Multi-devises** : Conversion vers devise société
- **Sessions non fermées** : Peuvent fausser calculs
- **Commandes annulées** : États à exclure ('draft', 'cancel')

### Bonnes pratiques :
- Générer rapport quotidien de clôture
- Archiver rapports pour audit
- Comparer avec rapports comptables
- Analyser écarts et tendances
- Utiliser pour pilotage commercial

---

## Modèles et Relations Clés

### Relations principales :
```
pos.config (1) ← (N) pos.session (1) ← (N) pos.order
pos.order (1) ← (N) pos.order.line
pos.order (1) ← (N) pos.payment
pos.session (1) ← (N) account.bank.statement.line
```

### Contraintes importantes :
- Une seule session ouverte par `pos.config`
- Nom de session unique
- Montants cohérents commande/paiements
- Stock suffisant (si contrôle activé)

### Sécurité et Droits :
- `group_pos_manager` : Configuration complète
- `group_pos_user` : Utilisation caisse uniquement
- `access_token` : Sécurisation sessions
- Logs automatiques sur `mail.thread`

Cette documentation couvre les cas d'usage principaux du module POS Odoo 17, avec focus sur l'aspect métier et opérationnel pour les utilisateurs finaux.