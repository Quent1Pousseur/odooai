# OdooAI — Conditions Generales d'Utilisation (DRAFT v1)
## Redige par : Legal & Compliance (16)
## Review : CEO (01), CFO (15), Security Arch (07)
## Date : 2026-03-20
## Status : DRAFT — a valider par un avocat avant publication

---

## 1. Objet

Les presentes Conditions Generales d'Utilisation (CGU) regissent l'acces et l'utilisation du service OdooAI, un outil d'analyse et de recommandation base sur l'intelligence artificielle pour les utilisateurs du logiciel Odoo.

OdooAI est edite par [NOM SOCIETE], [FORME JURIDIQUE], immatriculee sous le numero [NUMERO], dont le siege social est situe a [ADRESSE].

## 2. Definitions

- **Service** : la plateforme OdooAI accessible via le web et/ou le CLI
- **Utilisateur** : toute personne physique ou morale utilisant le Service
- **Instance Odoo** : l'installation Odoo de l'Utilisateur connectee au Service
- **Credentials** : les identifiants de connexion Odoo fournis par l'Utilisateur (URL, base de donnees, login, cle API)
- **Donnees** : les informations extraites de l'Instance Odoo de l'Utilisateur

## 3. Acceptation

L'utilisation du Service implique l'acceptation sans reserve des presentes CGU. L'Utilisateur declare etre autorise a connecter son Instance Odoo au Service.

## 4. Description du Service

OdooAI fournit :
- L'analyse de la configuration de l'Instance Odoo de l'Utilisateur
- Des recommandations d'optimisation basees sur les fonctionnalites Odoo
- Des reponses a des questions relatives a l'utilisation d'Odoo

Le Service fonctionne en **lecture seule**. Il ne modifie, ne cree, et ne supprime aucune donnee dans l'Instance Odoo de l'Utilisateur.

## 5. Inscription et acces

L'Utilisateur s'inscrit en fournissant une adresse email valide. L'acces au Service est personnel et non-cessible. L'Utilisateur est responsable de la confidentialite de ses identifiants.

## 6. Connexion a Odoo

L'Utilisateur fournit ses Credentials pour permettre au Service d'acceder a son Instance Odoo. Ces Credentials :
- Ne sont PAS stockes de maniere permanente (memoire de session uniquement)
- Sont transmis de maniere securisee (HTTPS obligatoire en production)
- Ne sont jamais partages avec des tiers

L'Utilisateur garantit etre autorise par le proprietaire de l'Instance Odoo a connecter le Service.

## 7. Traitement des donnees

### 7.1 Donnees collectees
- Donnees de l'Instance Odoo : modeles, champs, configurations, enregistrements (en lecture seule)
- Donnees d'utilisation : questions posees, reponses generees, nombre de requetes
- Donnees de compte : email, plan souscrit, historique de facturation

### 7.2 Sous-traitants
Le Service utilise l'API Anthropic (Claude) pour generer les reponses. Les donnees de l'Instance Odoo sont transmises a Anthropic dans le cadre du traitement des requetes. Anthropic ne stocke pas les donnees des requetes API et ne les utilise pas pour l'entrainement de ses modeles.

### 7.3 Anonymisation
Les donnees sensibles (RH, salaires, donnees personnelles) sont anonymisees par le Security Guardian AVANT transmission a Anthropic.

### 7.4 Conservation
- Conversations : conservees tant que le compte est actif
- Credentials Odoo : non conserves (session uniquement)
- Logs d'audit : conserves selon le plan (30 a 365 jours)

Voir la Politique de Confidentialite pour plus de details (GDPR).

## 8. Responsabilite

### 8.1 Limitation de responsabilite
OdooAI est un outil d'aide a la decision. Les recommandations generees par l'IA sont fournies **a titre indicatif** et ne constituent en aucun cas :
- Un conseil juridique
- Un conseil fiscal ou comptable
- Une garantie de resultat
- Un audit professionnel

L'Utilisateur reste seul responsable des decisions prises sur la base des recommandations du Service.

### 8.2 Exactitude des reponses
Le Service utilise l'intelligence artificielle qui peut produire des reponses imprecises, incompletes ou erronees. L'Editeur ne garantit pas l'exactitude des reponses generees.

### 8.3 Disponibilite
L'Editeur s'efforce d'assurer la disponibilite du Service mais ne garantit pas un fonctionnement ininterrompu. Le Service peut etre indisponible pour maintenance, mise a jour ou en cas de force majeure.

## 9. Tarification et paiement

Le Service est propose sous forme d'abonnement mensuel selon les plans affiches sur le site. Les prix sont indiques hors taxes.

Le paiement est effectue par carte bancaire via Stripe. L'abonnement est reconduit tacitement chaque mois sauf resiliation.

## 10. Resiliation

L'Utilisateur peut resilier son abonnement a tout moment depuis son espace personnel. La resiliation prend effet a la fin du cycle de facturation en cours. Aucun remboursement prorata n'est effectue.

L'Editeur se reserve le droit de suspendre ou resilier l'acces au Service en cas de :
- Violation des presentes CGU
- Utilisation abusive du Service (depassement des quotas, scraping, reverse engineering)
- Non-paiement

## 11. Propriete intellectuelle

Le Service, son code source, ses Knowledge Graphs, ses BA Profiles, et sa documentation sont la propriete exclusive de l'Editeur. L'Utilisateur ne dispose d'aucun droit de propriete intellectuelle sur le Service.

L'Utilisateur conserve la propriete de ses Donnees Odoo. Le Service ne revendique aucun droit sur les Donnees de l'Utilisateur.

## 12. Relation avec Odoo SA

OdooAI **n'est pas affilie a Odoo SA**. "Odoo" est une marque deposee d'Odoo SA. Le Service est un produit independant qui interagit avec le logiciel Odoo via ses APIs publiques.

## 13. Droit applicable et litiges

Les presentes CGU sont regies par le droit belge. En cas de litige, les tribunaux de Bruxelles sont seuls competents.

## 14. Modification des CGU

L'Editeur se reserve le droit de modifier les presentes CGU. Les Utilisateurs seront informes par email au moins 30 jours avant l'entree en vigueur des modifications. La poursuite de l'utilisation du Service apres cette date vaut acceptation.

---

*Version : DRAFT v1 — 2026-03-20*
*A faire valider par un avocat specialise en droit du numerique et propriete intellectuelle.*

## Notes Legal (16) — Points a discuter avec l'avocat

1. **LGPL et Knowledge Graphs** : les KG sont-ils du "derived work" ? Position preliminaire = non, mais a confirmer
2. **Responsabilite IA** : le disclaimer est-il suffisant en droit belge ?
3. **Sous-traitant Anthropic** : un DPA (Data Processing Agreement) est-il necessaire ?
4. **Marque "Odoo"** : l'utilisation du nom "OdooAI" pose-t-elle un risque de confusion ?
5. **EU AI Act** : obligations supplementaires pour un systeme IA "limited risk" ?
