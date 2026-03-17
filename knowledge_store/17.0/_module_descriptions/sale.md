# Module Odoo 17 : Sale - Description Métier Complète

Le module **sale** d'Odoo 17 est le cœur du processus commercial, gérant l'intégralité du cycle de vente depuis le devis jusqu'à la facturation. Il s'intègre parfaitement avec les modules de comptabilité, de paiement et de livraison.

## USE CASE 1 : Création et Gestion des Devis/Commandes

### Modèle Principal : `sale.order`

**Champs clés :**
- `name` : Référence du devis (ex: "SO001", "QU002")
- `partner_id` : Client (Many2one vers `res.partner`)
- `state` : Statut avec les valeurs :
  - `draft` : "Devis" (état initial)
  - `sent` : "Devis envoyé"
  - `sale` : "Commande de vente" (confirmé)
  - `cancel` : "Annulé"
- `date_order` : Date de création/confirmation
- `validity_date` : Date d'expiration du devis
- `commitment_date` : Date de livraison promise
- `locked` : Commande verrouillée (non modifiable)

### Workflow Complet :

1. **Création du devis** :
   - Navigation : `Ventes > Commandes > Devis`
   - Clic sur "Créer"
   - État initial : `draft`
   - Référence automatique : "Nouveau" puis séquence générée

2. **Configuration du devis** :
   - Sélection du client (`partner_id`)
   - Calcul automatique des adresses de facturation/livraison
   - Position fiscale calculée selon le client

3. **Envoi du devis** :
   - Bouton "Envoyer par email"
   - État passe à `sent`
   - Email automatique avec PDF attaché

4. **Confirmation** :
   - Bouton "Confirmer"
   - État passe à `sale`
   - `date_order` mise à jour avec la date de confirmation
   - Contrainte SQL : commande confirmée doit avoir une date

5. **Verrouillage** :
   - Champ `locked = True`
   - Empêche toute modification
   - Utilisé après génération de factures/livraisons

### Menu dans Odoo :
```
Ventes
├── Commandes
│   ├── Devis
│   ├── Commandes de vente
│   └── Commandes verrouillées
```

### Pièges Courants :
- **Contrainte de date** : Une commande confirmée DOIT avoir une date_order
- **Modification impossible** : Les commandes verrouillées ne peuvent plus être modifiées
- **Adresses manquantes** : Vérifier que le client a des adresses de facturation/livraison

### Bonnes Pratiques :
- Toujours vérifier la position fiscale avant confirmation
- Utiliser `commitment_date` pour les promesses de livraison spécifiques
- Verrouiller les commandes après facturation complète

## USE CASE 2 : Gestion des Lignes de Commande

### Modèle Principal : `sale.order.line`

**Champs clés :**
- `order_id` : Référence vers la commande (cascade delete)
- `product_id` : Produit sélectionné
- `name` : Description de la ligne
- `product_uom_qty` : Quantité
- `price_unit` : Prix unitaire
- `tax_id` : Taxes applicables (Many2many)
- `display_type` : Type d'affichage (`line_section`, `line_note`)
- `is_downpayment` : Ligne d'acompte
- `sequence` : Ordre d'affichage

### Workflow Complet :

1. **Ajout de produit** :
   - Dans la commande, onglet "Lignes de commande"
   - Sélection du produit
   - Auto-completion de la description, prix, taxes

2. **Configuration avancée** :
   - Modification de la quantité
   - Ajustement du prix unitaire
   - Sélection des taxes spécifiques

3. **Lignes spéciales** :
   - **Section** : `display_type = 'line_section'` (titre de regroupement)
   - **Note** : `display_type = 'line_note'` (texte explicatif)
   - **Acompte** : `is_downpayment = True` (créé automatiquement)

4. **Calculs automatiques** :
   - Montant ligne = `product_uom_qty * price_unit`
   - Application des taxes selon `tax_id`
   - Total commande mis à jour en temps réel

### Contraintes SQL Importantes :
```sql
-- Lignes comptables doivent avoir produit et UdM
"CHECK(display_type IS NOT NULL OR (product_id IS NOT NULL AND product_uom IS NOT NULL))"

-- Lignes d'affichage ne doivent pas avoir de valeurs métier
"CHECK(display_type IS NULL OR (product_id IS NULL AND price_unit = 0))"
```

### Pièges Courants :
- **Lignes sans produit** : Les sections/notes n'acceptent pas de produit
- **UdM manquante** : Toute ligne avec produit doit avoir une unité de mesure
- **Taxes incorrectes** : Vérifier la cohérence avec la position fiscale

## USE CASE 3 : Signature et Paiement en Ligne

### Champs de Configuration :
- `require_signature` : Signature obligatoire
- `require_payment` : Paiement obligatoire
- `prepayment_percent` : Pourcentage d'acompte requis
- `signature` : Image de la signature
- `signed_by` : Nom du signataire
- `signed_on` : Date de signature

### Workflow Portail Client :

1. **Configuration sur le devis** :
   - Activer "Signature en ligne" et/ou "Paiement en ligne"
   - Définir le pourcentage d'acompte si nécessaire

2. **Envoi au client** :
   - Email avec lien vers le portail
   - Client accède au devis via le portail

3. **Processus côté client** :
   - Visualisation du devis
   - Signature électronique si requise
   - Paiement en ligne si configuré

4. **Confirmation automatique** :
   - Si conditions remplies (signature + paiement)
   - Devis confirmé automatiquement
   - Passage à l'état `sale`

### Intégration Paiement (`payment.transaction`) :
- `sale_order_ids` : Commandes liées à la transaction
- Confirmation automatique si montant suffisant
- Support des acomptes partiels

## USE CASE 4 : Facturation depuis les Commandes

### Champs de Facturation :
- `invoice_status` : Statut facturation
  - `no` : "Rien à facturer"
  - `to invoice` : "À facturer"
  - `invoiced` : "Entièrement facturé"
  - `upselling` : "Opportunité de vente supplémentaire"

### Workflow de Facturation :

1. **Génération de facture** :
   - Menu : `Ventes > À facturer`
   - Sélection des commandes
   - Action "Créer les factures"

2. **Types de facturation** :
   - **Facture normale** : Tous les produits livrés
   - **Facture d'acompte** : Pourcentage ou montant fixe
   - **Facture finale** : Solde après déduction acomptes

3. **Intégration comptable** (`account.move.line`) :
   - `sale_line_ids` : Lien vers lignes de commande
   - `is_downpayment` : Marquage des acomptes
   - Réconciliation automatique des paiements

### Gestion des Acomptes :
```python
# Ligne d'acompte créée automatiquement
downpayment_line = {
    'is_downpayment': True,
    'name': "Acompte: 30%",
    'price_unit': -montant_acompte,  # Négatif pour déduction
}
```

## USE CASE 5 : Intégration avec la Comptabilité

### Modèle Étendu : `account.move`

**Nouveaux champs :**
- `team_id` : Équipe commerciale
- `sale_order_count` : Nombre de commandes liées
- UTM (campaign_id, medium_id, source_id) : Traçabilité marketing

### Workflows d'Intégration :

1. **Création facture depuis commande** :
   - Conservation des informations UTM
   - Attribution équipe commerciale automatique
   - Lien bidirectionnel commande ↔ facture

2. **Paiement des factures** :
   - Message automatique sur la commande : "Facture XXX payée"
   - Rapprochement automatique avec transactions de paiement
   - Mise à jour du statut de facturation

3. **Gestion des acomptes** :
   - Validation des taxes sur acomptes lors du passage en "Comptabilisé"
   - Calcul automatique du prix unitaire des acomptes
   - Suppression automatique des lignes d'acompte lors d'annulation

## USE CASE 6 : Suivi et Reporting

### Menus de Suivi :
```
Ventes
├── Rapports
│   ├── Ventes
│   ├── Équipes de vente
│   └── Clients
├── Configuration
│   ├── Paramètres
│   ├── Équipes de vente
│   └── Conditions de vente
```

### KPI Intégrés :
- Montant total des commandes
- Taux de conversion devis → commande
- Performance par équipe commerciale
- Analyse de la marge par produit

### Automatisations :
- **CRON d'envoi factures** : Envoi automatique des factures prêtes
- **Relances automatiques** : Devis non confirmés
- **Notifications** : Changements d'état, paiements reçus

## CONFIGURATION ESSENTIELLE

### Paramètres Requis :
1. **Séquences** : Configuration des numérotations (SO, QU)
2. **Conditions de paiement** : Délais et modalités
3. **Positions fiscales** : Gestion des taxes par région/client
4. **Méthodes de paiement** : Intégration avec les providers de paiement
5. **Modèles d'email** : Personnalisation des communications

### Sécurité et Droits :
- **Groupes utilisateurs** : Vendeur, Manager commercial, Admin
- **Règles d'enregistrement** : Visibilité par équipe commerciale
- **Workflow d'approbation** : Validation des gros montants

Cette architecture modulaire permet une grande flexibilité tout en maintenant l'intégrité des processus commerciaux et comptables.