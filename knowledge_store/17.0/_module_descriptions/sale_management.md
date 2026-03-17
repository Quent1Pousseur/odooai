# Module Odoo 17 : sale_management - Description Métier Complète

Ce module étend le module de vente Odoo en ajoutant un système de **modèles de devis** (quotation templates) avec des **produits optionnels**. Il permet de standardiser et accélérer la création de devis en utilisant des templates prédéfinis.

## USE CASE 1 : Création et Configuration des Modèles de Devis

### Modèle Principal
**Modèle** : `sale.order.template`

### Champs Clés
- `name` : Nom du modèle de devis (requis)
- `active` : Activer/désactiver le modèle
- `company_id` : Société propriétaire du modèle
- `note` : Conditions générales (HTML, traduisible)
- `number_of_days` : Durée de validité du devis en jours
- `require_signature` : Exiger une signature électronique
- `require_payment` : Exiger un paiement en ligne
- `prepayment_percent` : Pourcentage d'acompte (0.0 à 1.0)
- `mail_template_id` : Modèle d'email de confirmation
- `journal_id` : Journal comptable de facturation
- `sale_order_template_line_ids` : Lignes du modèle (One2many)
- `sale_order_template_option_ids` : Produits optionnels (One2many)

### Menu dans Odoo
**Navigation** : Ventes → Configuration → Modèles de devis
**Vue** : Liste et formulaire standard

### Workflow Complet
1. **Création du modèle** :
   - Aller dans Ventes → Configuration → Modèles de devis
   - Cliquer sur "Créer"
   - Remplir le nom du modèle
   - Configurer les paramètres (signature, paiement, validité)

2. **Ajout des lignes** :
   - Dans l'onglet "Lignes", ajouter les produits standards
   - Définir les quantités par défaut
   - Organiser avec des sections et notes si nécessaire

3. **Ajout des options** :
   - Dans l'onglet "Produits Optionnels", ajouter les produits optionnels
   - Ces produits pourront être ajoutés par le client ou commercial

4. **Configuration avancée** :
   - Définir le modèle d'email de confirmation
   - Choisir le journal de facturation spécifique

### Pièges Courants
- **Cohérence multi-sociétés** : Tous les produits du modèle doivent appartenir à la même société que le modèle
- **Pourcentage d'acompte** : Doit être entre 0 et 100% si le paiement en ligne est requis
- **Traductions automatiques** : Les descriptions de produits sont automatiquement mises à jour lors des changements de langue

### Bonnes Pratiques
- Créer des modèles spécifiques par type de client ou secteur d'activité
- Utiliser les sections pour organiser les lignes logiquement
- Définir des durées de validité adaptées au cycle de vente
- Tester les modèles d'email avant mise en production

## USE CASE 2 : Lignes de Modèle de Devis

### Modèle
**Modèle** : `sale.order.template.line`

### Champs Clés
- `sale_order_template_id` : Référence au modèle parent
- `sequence` : Ordre d'affichage des lignes
- `product_id` : Produit sélectionné
- `name` : Description (calculée depuis le produit)
- `product_uom_qty` : Quantité par défaut
- `product_uom_id` : Unité de mesure
- `display_type` : Type d'affichage ("line_section", "line_note", ou False)

### Workflow Complet
1. **Ajout d'une ligne produit** :
   - Dans le formulaire du modèle, onglet "Lignes"
   - Cliquer sur "Ajouter une ligne"
   - Sélectionner le produit → la description se remplit automatiquement
   - Définir la quantité par défaut
   - Ajuster la séquence si nécessaire

2. **Ajout d'une section** :
   - Cliquer sur "Ajouter une ligne"
   - Changer le type d'affichage vers "Section"
   - Saisir le titre de la section dans "Description"

3. **Ajout d'une note** :
   - Cliquer sur "Ajouter une ligne"
   - Changer le type d'affichage vers "Note"
   - Saisir le contenu de la note

### Contraintes SQL
- Lignes comptabilisables : `product_id` et `product_uom_id` requis
- Lignes non-comptabilisables : `product_id` doit être vide et quantité = 0

### Pièges Courants
- **Changement de type impossible** : Une fois créée, on ne peut pas changer le type d'une ligne (produit → section)
- **Contraintes de cohérence** : Les sections/notes ne peuvent pas avoir de produit associé

## USE CASE 3 : Produits Optionnels de Modèle

### Modèle
**Modèle** : `sale.order.template.option`

### Champs Clés
- `sale_order_template_id` : Référence au modèle parent
- `product_id` : Produit optionnel (requis)
- `name` : Description du produit
- `quantity` : Quantité par défaut
- `uom_id` : Unité de mesure

### Workflow Complet
1. **Configuration des options** :
   - Dans le modèle de devis, onglet "Produits Optionnels"
   - Ajouter les produits que le client pourra choisir
   - Définir les quantités par défaut

2. **Utilisation côté devis** :
   - Les options apparaissent dans le devis généré
   - Le commercial ou client peut les ajouter au besoin

## USE CASE 4 : Application des Modèles aux Devis

### Modèle Étendu
**Modèle** : `sale.order` (hérité)

### Nouveaux Champs
- `sale_order_template_id` : Modèle de devis appliqué
- `sale_order_option_ids` : Options disponibles sur ce devis

### Workflow Complet
1. **Application automatique** :
   - Lors de la création d'un devis, le modèle par défaut de la société s'applique automatiquement
   - Exception : commandes e-commerce (pas de modèle auto)

2. **Application manuelle** :
   - Dans le formulaire de devis, champ "Modèle de devis"
   - Sélectionner un modèle → les lignes et options se rechargent automatiquement
   - **Attention** : Efface les lignes existantes !

3. **Changement de client** :
   - Si le devis n'est pas sauvegardé et que les lignes ne sont pas modifiées
   - Le modèle se recharge automatiquement pour s'adapter au nouveau client

### Calculs Automatiques
Le modèle recalcule automatiquement :
- **Note/Conditions** : Reprend celles du modèle (dans la langue du client)
- **Signature requise** : Selon le paramétrage du modèle
- **Paiement requis** : Selon le paramétrage du modèle
- **Pourcentage d'acompte** : Si paiement requis
- **Date de validité** : Date actuelle + nombre de jours du modèle
- **Journal comptable** : Journal spécifique du modèle

### Menu dans Odoo
**Navigation** : Ventes → Commandes → Devis
**Champ** : "Modèle de devis" dans l'onglet "Autres informations"

## USE CASE 5 : Gestion des Produits Optionnels sur Devis

### Modèle
**Modèle** : `sale.order.option`

### Champs Clés
- `order_id` : Référence au devis parent
- `product_id` : Produit optionnel
- `line_id` : Ligne de commande créée (si ajoutée)
- `name` : Description
- `quantity` : Quantité
- `uom_id` : Unité de mesure
- `price_unit` : Prix unitaire (calculé)
- `discount` : Remise (calculée)
- `is_present` : Indique si le produit est déjà dans le devis
- `sequence` : Ordre d'affichage

### Workflow Complet
1. **Visualisation des options** :
   - Dans le devis, onglet dédié aux produits optionnels
   - Voir le prix calculé automatiquement
   - Statut "Présent sur devis" mis à jour dynamiquement

2. **Ajout d'une option au devis** :
   - Bouton "Ajouter au devis" sur chaque option
   - Crée automatiquement une ligne de commande
   - Lie l'option à la ligne créée (champ `line_id`)

3. **Calcul des prix** :
   - Prix et remise calculés automatiquement selon les règles tarifaires
   - Utilise temporairement une ligne de commande virtuelle pour les calculs

### Contrôles et Validations
- **Devis confirmé** : Impossible d'ajouter des options à un devis confirmé
- **Cohérence société** : Les produits optionnels doivent appartenir à la même société que le devis

### Pièges Courants
- **Modification après confirmation** : Les options ne peuvent plus être ajoutées une fois le devis confirmé
- **Doublons** : Le système détecte si un produit optionnel est déjà présent dans les lignes standard

### Bonnes Pratiques
- Organiser les options par ordre d'importance (champ sequence)
- Utiliser des descriptions claires pour les options
- Vérifier régulièrement la cohérence des prix calculés
- Former les commerciaux sur l'utilisation des options

## Points d'Attention Techniques

### Gestion Multi-Sociétés
- Contrôles stricts sur la cohérence des sociétés entre modèles, produits et devis
- Messages d'erreur explicites en cas d'incohérence

### Performance
- Calculs de prix optimisés avec création temporaire de lignes
- Mise à jour automatique des traductions sur tous les modèles

### Intégrations
- Compatible avec le module e-commerce (exclusion automatique)
- Intégration avec les journaux comptables
- Support des modèles d'emails personnalisés

Ce module est particulièrement utile pour les entreprises avec des offres standardisées ou récurrentes, permettant de gagner significativement en temps de création de devis tout en maintenant la cohérence commerciale.