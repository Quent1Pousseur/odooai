# Module stock_account - Odoo 17 : Comptabilité des Stocks

## Vue d'ensemble
Le module **stock_account** est un module essentiel d'Odoo qui fait le pont entre la gestion des stocks et la comptabilité. Il permet la valorisation automatique des mouvements de stock en temps réel et génère les écritures comptables correspondantes selon la méthode anglo-saxonne.

---

## USE CASE 1 : Valorisation des produits en temps réel

### Modèles impliqués
- **product.template** (template de produit)
- **product.product** (variante de produit)
- **stock.valuation.layer** (couche de valorisation)
- **product.category** (catégorie de produit)

### Champs clés

**Sur product.template :**
- `cost_method` : Méthode de coût (standard, average, fifo)
- `valuation` : Type de valorisation (manual_periodic, real_time)

**Sur product.product :**
- `value_svl` : Valeur totale en stock
- `quantity_svl` : Quantité totale en stock
- `avg_cost` : Coût moyen
- `total_value` : Valeur totale
- `stock_valuation_layer_ids` : Lien vers les couches de valorisation

### Workflow complet

1. **Configuration initiale**
   - Accéder à *Inventaire > Configuration > Catégories de produits*
   - Définir `property_cost_method` (standard/average/fifo)
   - Définir `property_valuation` (manual_periodic/real_time)
   - Configurer les comptes comptables stock

2. **Changement de catégorie avec impact valorisation**
   - Modification du champ `categ_id` sur un produit
   - Le système détecte si la méthode de coût ou valorisation change
   - Vidage automatique du stock avec l'ancienne méthode
   - Reconstitution avec la nouvelle méthode
   - Génération des écritures comptables si valorisation en temps réel

### Menu dans Odoo
- *Inventaire > Configuration > Catégories de produits*
- *Inventaire > Produits > Produits* (vue form, onglet Inventaire)

### Pièges courants
- **Changement de catégorie en cours d'exercice** : Impact sur les valorisations historiques
- **Produits avec stock existant** : Le changement déclenche automatiquement un vidage/reconstitution
- **Droits d'accès comptables** : L'utilisateur doit avoir les droits sur les écritures comptables

### Bonnes pratiques
- Définir les catégories et méthodes de coût avant la saisie des mouvements
- Éviter les changements de catégorie sur des produits avec historique
- Tester les changements sur un environnement de test

---

## USE CASE 2 : Mouvements de stock avec valorisation

### Modèles impliqués
- **stock.move** (mouvement de stock)
- **stock.move.line** (ligne de mouvement détaillée)
- **stock.valuation.layer** (couche de valorisation)
- **account.move** (écriture comptable)

### Champs clés

**Sur stock.move :**
- `to_refund` : Mise à jour des quantités sur commande
- `account_move_ids` : Écritures comptables liées
- `stock_valuation_layer_ids` : Couches de valorisation
- `analytic_account_line_ids` : Lignes analytiques

### Workflow complet

1. **Réception de marchandises** (`_is_in()` = True)
   - Mouvement depuis fournisseur vers stock interne
   - Calcul du prix unitaire via `_get_price_unit()`
   - Création d'une couche de valorisation positive
   - Si valorisation temps réel : écriture Débit Stock / Crédit Stock Intérim

2. **Sortie de marchandises** (`_is_out()` = True)
   - Mouvement depuis stock interne vers client
   - Application de la méthode de coût (FIFO, Average, Standard)
   - Création d'une couche de valorisation négative
   - Si valorisation temps réel : écriture Débit COGS / Crédit Stock

3. **Dropshipping** (`_is_dropshipped()` = True)
   - Livraison directe fournisseur → client
   - Pas d'impact sur le stock physique
   - Couches de valorisation neutres (entrée + sortie)

4. **Retours**
   - Utilisation de `origin_returned_move_id`
   - Reprise du prix de la livraison originale
   - Inversion des écritures comptables

### Menu dans Odoo
- *Inventaire > Opérations > Mouvements de stock*
- Bouton "Écritures comptables" sur la fiche mouvement
- *Inventaire > Rapports > Valorisation du stock*

### Pièges courants
- **Mouvements sans prix** : Utilise le prix standard par défaut
- **Retours complexes** : Calcul du prix basé sur les couches originales
- **Dropshipping** : Double mouvement comptable (entrée puis sortie immédiate)

### Bonnes pratiques
- Valider tous les mouvements de stock quotidiennement
- Surveiller les alertes de prix négatif ou nul
- Effectuer régulièrement un rapprochement stock comptable/physique

---

## USE CASE 3 : Couches de valorisation (Stock Valuation Layers)

### Modèles impliqués
- **stock.valuation.layer** (couche de valorisation principale)
- **product.product** (produit lié)
- **stock.move** (mouvement source)
- **account.move** (écriture comptable générée)

### Champs clés

**Sur stock.valuation.layer :**
- `product_id` : Produit concerné
- `quantity` : Quantité de la couche
- `unit_cost` : Coût unitaire
- `value` : Valeur totale (quantity × unit_cost)
- `remaining_qty` : Quantité restante (pour FIFO)
- `remaining_value` : Valeur restante
- `stock_move_id` : Mouvement de stock source
- `account_move_id` : Écriture comptable générée
- `stock_valuation_layer_id` : Couche parente (pour corrections)

### Workflow complet

1. **Création automatique**
   - Déclenchée par la validation d'un mouvement de stock valorisé
   - Une couche par mouvement (positive pour entrées, négative pour sorties)
   - Calcul automatique des valeurs selon la méthode de coût

2. **Méthode FIFO**
   - Les sorties consomment les couches dans l'ordre chronologique
   - Mise à jour des champs `remaining_qty` et `remaining_value`
   - Création de couches multiples si plusieurs lots consommés

3. **Génération des écritures comptables**
   - Via `_validate_accounting_entries()`
   - Création automatique des account.move
   - Réconciliation automatique en comptabilité anglo-saxonne

4. **Corrections de prix**
   - Champ `price_diff_value` pour les ajustements de facture
   - Création de couches de correction liées

### Menu dans Odoo
- *Inventaire > Rapports > Stock Valuation*
- *Comptabilité > Comptabilité > Écritures diverses* (couches liées)
- Bouton "Couches de valorisation" sur fiche produit

### Pièges courants
- **Suppression manuelle interdite** : Les couches sont en lecture seule
- **Corrections multiples** : Attention aux chaînages de corrections
- **Performances** : Index nécessaires sur gros volumes

### Bonnes pratiques
- Ne jamais modifier manuellement les couches
- Utiliser les rapports standard pour l'analyse
- Surveiller les couches avec `remaining_qty` négatif (anomalies)

---

## USE CASE 4 : Comptabilité anglo-saxonne (COGS)

### Modèles impliqués
- **account.move** (facture client/fournisseur)
- **account.move.line** (ligne de facture et COGS)
- **stock.move** (mouvements de stock liés)
- **stock.valuation.layer** (valorisation des sorties)

### Champs clés

**Sur account.move :**
- `stock_move_id` : Mouvement de stock lié
- `stock_valuation_layer_ids` : Couches de valorisation liées

**Sur account.move.line :**
- `display_type` : Type d'affichage ('cogs' pour les lignes de coût)

### Workflow complet

1. **Configuration préalable**
   - Activer "Comptabilité anglo-saxonne" dans les paramètres comptables
   - Configurer les comptes sur les catégories de produits :
     - `property_stock_account_input_categ_id` : Stock Intérim Réceptionné
     - `property_stock_account_output_categ_id` : Stock Intérim Livré
     - `property_stock_valuation_account_id` : Compte de valorisation stock

2. **Facturation client (vente)**
   - Validation de la facture client
   - Appel de `_stock_account_prepare_anglo_saxon_out_lines_vals()`
   - Création automatique des lignes COGS :
     - Débit : Compte de charges (expense)
     - Crédit : Stock Intérim Livré

3. **Réconciliation automatique**
   - Via `_stock_account_anglo_saxon_reconcile_valuation()`
   - Rapprochement entre les lignes COGS et les sorties de stock
   - Lettrage automatique des comptes intérimaires

4. **Facturation fournisseur (achat)**
   - Réconciliation entre la réception et la facture
   - Ajustement des écarts de prix si nécessaire

### Menu dans Odoo
- *Comptabilité > Configuration > Paramètres* (activation anglo-saxon)
- *Inventaire > Configuration > Catégories* (configuration comptes)
- *Comptabilité > Comptabilité > Pièces comptables* (visualisation COGS)

### Pièges courants
- **Comptes manquants** : Les lignes COGS ne se créent pas
- **Produits non stockables** : Pas de génération COGS automatique
- **Factures d'avoir** : Inversion des signes dans les calculs
- **Réconciliation bloquée** : Vérifier les comptes et montants

### Bonnes pratiques
- Tester la configuration sur quelques produits pilotes
- Vérifier régulièrement les réconciliations automatiques
- Documenter le plan de comptes spécifique aux stocks
- Former les utilisateurs sur les spécificités anglo-saxonnes

---

## USE CASE 5 : Comptabilité analytique sur stocks

### Modèles impliqués
- **account.analytic.plan** (plan analytique)
- **account.analytic.account** (compte analytique)
- **account.analytic.line** (ligne analytique)
- **stock.move** (mouvement de stock)

### Champs clés

**Sur stock.move :**
- `analytic_account_line_ids` : Lignes analytiques liées

### Workflow complet

1. **Configuration analytique**
   - Définir les plans analytiques dans *Comptabilité > Configuration > Comptabilité analytique*
   - Associer les comptes analytiques aux produits ou emplacements

2. **Distribution automatique**
   - Lors de la validation du mouvement : appel de `_account_analytic_entry_move()`
   - Calcul de la distribution via `_perform_analytic_distribution()`
   - Création/mise à jour des lignes analytiques

3. **Répartition proportionnelle**
   - Méthode `_calculate_distribution_amount()` pour éviter les erreurs d'arrondi
   - Gestion des pourcentages avec précision décimale
   - Correction automatique sur la dernière ligne

### Menu dans Odoo
- *Comptabilité > Comptabilité analytique > Comptes analytiques*
- *Comptabilité > Rapports > Comptabilité analytique*

### Pièges courants
- **Erreurs d'arrondi** : Cumul sur plusieurs lignes de répartition
- **Plans multiples** : Complexité dans les calculs de distribution
- **Suppression** : Les lignes analytiques sont supprimées avec l'annulation du mouvement

### Bonnes pratiques
- Définir clairement les règles de répartition analytique
- Vérifier la cohérence des totaux après répartition
- Utiliser les rapports analytiques pour le contrôle

---

## Configuration globale recommandée

### Paramètres comptables
- *Comptabilité > Configuration > Paramètres*
- Activer "Valorisation des stocks en temps réel"
- Activer "Comptabilité anglo-saxonne" si nécessaire

### Plan comptable stocks
- 3xxxxx : Comptes de stock (par catégorie)
- 4xxxxx : Comptes clients/fournisseurs
- 6xxxxx : Comptes de charges (COGS)
- Comptes intérimaires pour anglo-saxon

### Surveillance et maintenance
- Rapprocher mensuellement stock comptable/physique
- Contrôler les couches de valorisation négatives
- Valider les réconciliations automatiques
- Archiver les anciennes couches pour optimiser les performances

Le module stock_account est complexe mais essentiel pour une gestion comptable rigoureuse des stocks. Une configuration correcte et une bonne compréhension des mécanismes permettent une automatisation efficace de la comptabilité des stocks.