# Module Comptabilité Odoo 17 - Description Métier Complète

## Vue d'ensemble

Le module **accounting** d'Odoo 17 est le cœur du système comptable. Il gère l'ensemble des opérations comptables : écritures de journal, factures, paiements, relevés bancaires, et le plan comptable. Il s'articule autour de quatre modèles principaux interconnectés.

---

## Use Case 1 : Gestion des Écritures Comptables (account.move)

### Modèle et champs clés
**Modèle :** `account.move`
**Description :** Représente toute écriture comptable (factures, notes de crédit, paiements, écritures diverses)

**Champs essentiels :**
- `name` : Numéro de l'écriture (auto-généré selon séquence du journal)
- `move_type` : Type d'écriture (entry, out_invoice, in_invoice, out_refund, in_refund, out_receipt, in_receipt)
- `state` : État (draft, posted, cancel)
- `date` : Date comptable
- `journal_id` : Journal associé
- `line_ids` : Lignes d'écriture (One2many vers account.move.line)
- `partner_id` : Partenaire (client/fournisseur)
- `ref` : Référence externe
- `company_id` : Société

**Champs spécialisés :**
- `payment_id` : Lien vers un paiement
- `statement_line_id` : Lien vers une ligne de relevé bancaire
- `tax_cash_basis_*` : Gestion de la TVA sur encaissement
- `auto_post` : Comptabilisation automatique
- `is_storno` : Écriture de type storno (annulation)

### Workflow principal

1. **Création (Draft)**
   - Initialisation avec type de mouvement
   - Assignation automatique du journal selon le type
   - Génération des lignes d'écriture

2. **Validation (Posted)**
   - Vérification de l'équilibre débit/crédit
   - Attribution du numéro définitif
   - Verrouillage des modifications
   - Création des réconciliations automatiques

3. **Annulation (Cancel)**
   - Possible uniquement si pas de réconciliations
   - Génération d'écriture d'extourne si nécessaire

### Menu dans Odoo
- **Comptabilité > Écritures de journal > Écritures de journal**
- **Comptabilité > Clients > Factures**
- **Comptabilité > Fournisseurs > Factures**

### Pièges courants

1. **Modification après validation**
   - Les écritures comptabilisées ne peuvent plus être modifiées
   - Nécessité de passer par écriture d'extourne

2. **Déséquilibre comptable**
   - Total débit ≠ total crédit bloque la validation
   - Problème fréquent avec les devises multiples

3. **Séquence des numéros**
   - Gaps dans la numérotation causés par des brouillons supprimés
   - Attention aux séquences par journal

4. **Date comptable**
   - Impact sur la période fiscale et les reportings
   - Blocage si période clôturée

### Bonnes pratiques

1. **Gestion des types**
   - Utiliser les bons types de mouvement selon le contexte
   - `entry` pour écritures diverses, `out_invoice` pour factures clients

2. **Journaux appropriés**
   - Associer le bon journal selon le type d'opération
   - Respecter la logique métier (vente, achat, banque, etc.)

3. **Traçabilité**
   - Renseigner systématiquement la référence (`ref`)
   - Utiliser les pièces jointes pour justificatifs

4. **Contrôles**
   - Vérifier l'équilibre avant validation
   - Contrôler les comptes utilisés selon le type de journal

---

## Use Case 2 : Gestion des Paiements (account.payment)

### Modèle et champs clés
**Modèle :** `account.payment`
**Hérite de :** `account.move` (via _inherits)

**Champs spécifiques aux paiements :**
- `payment_type` : Type (inbound/outbound)
- `partner_type` : Type partenaire (customer/supplier)
- `amount` : Montant
- `payment_method_line_id` : Méthode de paiement
- `partner_bank_id` : Compte bancaire destinataire
- `is_internal_transfer` : Transfert interne
- `payment_reference` : Référence du paiement
- `outstanding_account_id` : Compte de transit
- `destination_account_id` : Compte de destination

**Champs de réconciliation :**
- `is_reconciled` : Paiement réconcilié
- `is_matched` : Rapproché avec relevé bancaire
- `reconciled_invoice_ids` : Factures réconciliées

### Workflow des paiements

1. **Création du paiement**
   - Sélection du type (réception/envoi)
   - Choix du partenaire et montant
   - Sélection de la méthode de paiement

2. **Validation**
   - Génération automatique de l'écriture comptable
   - Création des lignes débit/crédit appropriées
   - Comptabilisation automatique

3. **Réconciliation**
   - Rapprochement avec les factures
   - Réconciliation automatique ou manuelle
   - Mise à jour du statut de paiement des factures

### Menu dans Odoo
- **Comptabilité > Clients > Paiements**
- **Comptabilité > Fournisseurs > Paiements**
- **Comptabilité > Tableau de bord > Paiements**

### Pièges courants

1. **Méthodes de paiement**
   - Configuration incomplète des méthodes
   - Comptes de transit non configurés

2. **Réconciliation manquée**
   - Paiements non réconciliés avec factures
   - Impact sur l'âge des créances/dettes

3. **Devises multiples**
   - Problèmes de change lors de réconciliation
   - Écarts de change non gérés

4. **Transferts internes**
   - Double écriture non automatisée
   - Comptes de liaison mal configurés

### Bonnes pratiques

1. **Configuration préalable**
   - Paramétrer correctement les méthodes de paiement
   - Définir les comptes de transit appropriés

2. **Réconciliation systématique**
   - Réconcilier rapidement les paiements avec factures
   - Utiliser la réconciliation automatique quand possible

3. **Suivi des impayés**
   - Monitorer les paiements en attente
   - Tracer les rejets et retours

---

## Use Case 3 : Gestion des Journaux (account.journal)

### Modèle et champs clés
**Modèle :** `account.journal`

**Champs de base :**
- `name` : Nom du journal
- `code` : Code court (5 caractères max)
- `type` : Type (sale, purchase, cash, bank, general)
- `default_account_id` : Compte par défaut
- `company_id` : Société
- `currency_id` : Devise du journal
- `sequence` : Ordre d'affichage

**Champs de configuration :**
- `account_control_ids` : Comptes autorisés
- `restrict_mode_hash_table` : Verrouillage par hash
- `refund_sequence` : Séquence dédiée aux avoirs
- `payment_sequence` : Séquence dédiée aux paiements
- `suspense_account_id` : Compte d'attente (pour banque)

**Champs spécialisés :**
- `invoice_reference_type` : Type de référence facture
- `invoice_reference_model` : Modèle de référence
- `bank_statements_source` : Source des relevés bancaires

### Workflow de configuration

1. **Création du journal**
   - Définition du type selon l'usage
   - Attribution d'un code unique
   - Sélection du compte par défaut

2. **Configuration avancée**
   - Paramétrage des séquences
   - Définition des comptes autorisés
   - Configuration des méthodes de paiement

3. **Activation et utilisation**
   - Test avec écritures de test
   - Validation du paramétrage
   - Formation des utilisateurs

### Types de journaux et usages

**Journal de Vente (sale) :**
- Pour factures clients et avoirs
- Compte par défaut : compte de vente
- Séquences spécifiques factures/avoirs

**Journal d'Achat (purchase) :**
- Pour factures fournisseurs
- Compte par défaut : compte d'achat
- Contrôle des comptes utilisables

**Journal de Banque (bank) :**
- Pour opérations bancaires
- Compte par défaut : compte banque
- Configuration suspense pour rapprochement

**Journal de Caisse (cash) :**
- Pour opérations en espèces
- Compte par défaut : compte caisse
- Contrôles renforcés

**Journal Divers (general) :**
- Pour écritures diverses
- Tous comptes autorisés
- Maximum de flexibilité

### Menu dans Odoo
- **Comptabilité > Configuration > Journaux**
- **Comptabilité > Configuration > Comptabilité > Journaux**

### Pièges courants

1. **Type de journal incorrect**
   - Impact sur les automatismes
   - Problèmes de séquences et numérotation

2. **Comptes par défaut manquants**
   - Erreurs lors de la création d'écritures
   - Saisies incomplètes

3. **Séquences mal configurées**
   - Doublons dans la numérotation
   - Non-conformité légale

4. **Devises incohérentes**
   - Problèmes avec comptes multi-devises
   - Erreurs de change

### Bonnes pratiques

1. **Nomenclature claire**
   - Codes courts mais explicites
   - Noms compréhensibles par tous

2. **Configuration progressive**
   - Commencer par les journaux essentiels
   - Tester avant mise en production

3. **Droits d'accès**
   - Limiter l'accès selon les rôles
   - Traçabilité des modifications

4. **Documentation**
   - Documenter l'usage de chaque journal
   - Former les équipes comptables

---

## Use Case 4 : Gestion des Relevés Bancaires (account.bank.statement)

### Modèle et champs clés
**Modèle :** `account.bank.statement`

**Champs principaux :**
- `name` : Référence du relevé
- `reference` : Référence externe
- `date` : Date du relevé
- `journal_id` : Journal bancaire
- `line_ids` : Lignes du relevé (One2many)
- `balance_start` : Solde initial
- `balance_end` : Solde final calculé
- `balance_end_real` : Solde final réel
- `currency_id` : Devise

**Champs de contrôle :**
- `is_complete` : Relevé complet (équilibré)
- `is_valid` : Relevé valide (continuité avec précédent)
- `problem_description` : Description des problèmes
- `first_line_index` : Index de première ligne

### Workflow des relevés

1. **Import/Création**
   - Import automatique depuis banque
   - Ou création manuelle
   - Génération des lignes de relevé

2. **Rapprochement**
   - Rapprochement automatique avec écritures existantes
   - Rapprochement manuel pour lignes non reconnues
   - Création d'écritures pour opérations non comptabilisées

3. **Validation**
   - Vérification de l'équilibre
   - Contrôle de continuité avec relevé précédent
   - Validation finale du relevé

### Processus de rapprochement

**Rapprochement automatique :**
- Recherche par montant et partenaire
- Recherche par référence
- Tolérance sur les dates

**Rapprochement manuel :**
- Sélection manuelle d'écritures
- Création de nouvelles écritures
- Gestion des écarts

**Gestion des suspens :**
- Utilisation du compte de suspense
- Régularisation ultérieure
- Traçabilité des opérations

### Menu dans Odoo
- **Comptabilité > Banque > Relevés bancaires**
- **Comptabilité > Tableau de bord > Rapprocher les comptes bancaires**

### Pièges courants

1. **Soldes incohérents**
   - Écart entre solde calculé et réel
   - Erreurs de saisie ou d'import

2. **Continuité rompue**
   - Solde initial ≠ solde final du relevé précédent
   - Impact sur validité des relevés suivants

3. **Doublons de rapprochement**
   - Même opération rapprochée plusieurs fois
   - Désquilibre des comptes

4. **Devises multiples**
   - Problèmes de change
   - Comptes en devises étrangères

### Bonnes pratiques

1. **Import régulier**
   - Connecter les comptes bancaires
   - Automatiser l'import des relevés
   - Vérifier quotidiennement

2. **Rapprochement rapide**
   - Traiter les relevés dès réception
   - Former sur les outils de rapprochement
   - Utiliser les fonctions automatiques

3. **Contrôles qualité**
   - Vérifier la continuité des soldes
   - Analyser les écarts persistants
   - Documenter les opérations complexes

4. **Archivage**
   - Conserver les justificatifs
   - Traçabilité des opérations
   - Respect des obligations légales

---

## Use Case 5 : Plan Comptable (account.account)

### Modèle et champs clés
**Modèle :** `account.account`

**Champs de base :**
- `code` : Code comptable (jusqu'à 64 caractères)
- `name` : Libellé du compte
- `account_type` : Type de compte (sélection prédéfinie)
- `company_id` : Société
- `currency_id` : Devise forcée (optionnel)
- `deprecated` : Compte déprécié

**Champs de comportement :**
- `reconcile` : Autoriser la réconciliation
- `include_initial_balance` : Reporter le solde N-1
- `internal_group` : Groupe interne (asset, liability, etc.)
- `non_trade` : Compte hors exploitation

**Champs de configuration :**
- `tax_ids` : Taxes par défaut
- `allowed_journal_ids` : Journaux autorisés
- `tag_ids` : Étiquettes personnalisées
- `group_id` : Groupe comptable (calculé)
- `note` : Notes internes

### Types de comptes disponibles

**Actif :**
- `asset_receivable` : Créances clients
- `asset_cash` : Banques et caisses
- `asset_current` : Actif circulant
- `asset_non_current` : Actif immobilisé
- `asset_prepayments` : Charges constatées d'avance
- `asset_fixed` : Immobilisations

**Passif :**
- `liability_payable` : Dettes fournisseurs
- `liability_credit_card` : Cartes de crédit
- `liability_current` : Passif circulant
- `liability_non_current` : Passif non-circulant

**Capitaux propres :**
- `equity` : Capitaux propres
- `equity_unaffected` : Résultat de l'exercice

**Charges et produits :**
- `income` : Produits d'exploitation
- `income_other` : Autres produits
- `expense` : Charges d'exploitation
- `expense_depreciation` : Dotations amortissements
- `expense_direct_cost` : Coût des ventes

**Hors-bilan :**
- `off_balance` : Comptes d'ordre

### Workflow de configuration

1. **Analyse des besoins**
   - Étude du plan comptable réglementaire
   - Adaptation aux besoins métier
   - Définition des analytiques

2. **Paramétrage initial**
   - Import ou création manuelle
   - Attribution des types corrects
   - Configuration des comportements

3. **Tests et validation**
   - Test sur écritures type
   - Validation avec expertise-comptable
   - Formation des équipes

### Menu dans Odoo
- **Comptabilité > Configuration > Plan comptable**
- **Comptabilité > Configuration > Comptabilité > Plan comptable**

### Pièges courants

1. **Types de comptes incorrects**
   - Impact sur les états financiers
   - Problèmes de réconciliation
   - Erreurs de reporting

2. **Réconciliation mal configurée**
   - Comptes clients/fournisseurs sans réconciliation
   - Comptes de bilan avec réconciliation inutile

3. **Codes en doublon**
   - Impossible dans une même société
   - Problème lors de consolidation

4. **Devises incohérentes**
   - Devise forcée sur mauvais comptes
   - Problèmes multi-sociétés

### Bonnes pratiques

1. **Respect des normes**
   - Suivre le plan comptable réglementaire
   - Adapter selon la taille de l'entreprise
   - Documenter les choix

2. **Codification logique**
   - Structure hiérarchique cohérente
   - Codes parlants et extensibles
   - Éviter les codes trop courts

3. **Maintenance régulière**
   - Nettoyer les comptes inutilisés
   - Mettre à jour selon évolution métier
   - Contrôler l'usage des comptes

4. **Documentation**
   - Commenter les comptes spécifiques
   - Former sur l'usage des comptes
   - Créer des guides utilisateur

---

## Interactions entre les modèles

### Relations clés
1. **account.move ↔ account.journal** : Chaque écriture appartient à un journal
2. **account.payment → account.move** : Les paiements génèrent des écritures
3. **account.bank.statement → account.move** : Les relevés créent des écritures de rapprochement
4. **account.move.line → account.account** : Chaque ligne d'écriture utilise un compte

### Flux de données
1. **Facturation** : Facture (account.move) → Paiement (account.payment) → Réconciliation
2. **Banque** : Import relevé → Rapprochement → Création écritures → Réconciliation
3. **Comptabilité** : Écriture diverse → Validation → Impact plan comptable

### Intégrité référentielle
- Contrôles de société (multi-company)
- Vérifications de devises
- Validation des équilibres comptables
- Traçabilité des modifications

---

## Points d'attention transversaux

### Sécurité et droits d'accès
- Séparation des rôles comptables
- Verrouillage des périodes
- Traçabilité des modifications
- Sauvegarde des données sensibles

### Performance et volumétrie
- Index sur les champs de recherche fréquente
- Archivage des données anciennes
- Optimisation des requêtes de reporting
- Monitoring des performances

### Conformité légale
- Respect des obligations comptables locales
- Inaltérabilité des écritures validées
- Piste d'audit complète
- Archivage légal des justificatifs

Cette description complète couvre l'ensemble des aspects métier du module accounting d'Odoo 17, permettant une compréhension approfondie des mécanismes comptables et de leur mise en œuvre pratique.