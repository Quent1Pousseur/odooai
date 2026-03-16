# Learning — Legal (16) — GDPR Compliance Checklist for SaaS Products
## Date : 2026-03-21 (Sprint 5)
## Duree : 3 heures

## Ce que j'ai appris

1. **OdooAI est "processeur" (sous-traitant) des donnees Odoo du client** : le client est le "responsable de traitement" de ses donnees Odoo. OdooAI les traite pour fournir le service d'analyse. Ca necessite un Data Processing Agreement (DPA) signe avec chaque client, meme en free tier.

2. **Le transit des donnees Odoo vers Anthropic cree une chaine de sous-traitance** : OdooAI envoie des donnees Odoo (potentiellement personnelles) au LLM Claude. Anthropic est donc sous-traitant de sous-traitant. Il faut (a) un DPA avec Anthropic, (b) informer le client que ses donnees transitent par Anthropic, (c) documenter les garanties d'Anthropic (pas de training sur les donnees API).

3. **Le Data Anonymizer est une obligation legale, pas juste une feature** : le composant `security/anonymizer.py` qui masque les donnees personnelles AVANT envoi au LLM est requis par le principe de minimisation (Art. 5.1.c RGPD). Il faut pouvoir prouver que seules les donnees necessaires sont transmises.

4. **Droits des personnes concernees (DSAR)** : les employes dont les donnees apparaissent dans Odoo (hr.employee, res.partner) ont un droit d'acces, rectification, effacement. OdooAI doit pouvoir (a) lister toutes les donnees traitees pour une personne, (b) les supprimer sur demande. Le cache Redis doit avoir un TTL et supporter la purge par sujet.

5. **Le registre des traitements est obligatoire** : Article 30 RGPD. OdooAI doit maintenir un registre documentant : quelles donnees, pourquoi, combien de temps, qui y accede, quelles mesures de securite. Ca doit etre un document vivant, pas juste un PDF oublie.

## Comment ca s'applique a OdooAI

1. **L'Anonymizer doit etre auditable** : chaque anonymisation doit etre loguee (quel champ, quel type de donnee, quelle methode). Ca permet de prouver la conformite en cas de controle CNIL. Le audit log dans `security/audit.py` doit capturer ces evenements.

2. **Le DPA doit etre integre au onboarding** : quand un client connecte son instance Odoo, il doit accepter le DPA avant la premiere requete. C'est un blocker UX mais c'est legalement requis. L'UI doit presenter le DPA et enregistrer l'acceptation.

3. **La retention des donnees doit etre configurable** : les conversations, le cache, les logs doivent avoir des TTL clairs. Free tier : 7 jours. Pro : 30 jours. Enterprise : configurable. A la suppression du compte, tout doit etre purge sous 30 jours.

## Ce que je recommande

1. **Sprint 6** : Rediger le DPA template et la Privacy Policy specifique OdooAI. Les faire relire par un juriste RGPD. Budget : 500-1000 EUR pour une review juridique externe.

2. **Sprint 7** : Implementer le consentement DPA dans le flow de connexion Odoo (UI). Stocker l'acceptation avec timestamp et version du DPA dans la base.

3. **Sprint 8** : Creer le registre des traitements (Article 30) et implementer l'endpoint DSAR (`/api/privacy/data-request`) pour que les utilisateurs puissent demander l'export ou la suppression de leurs donnees.

## Sources

1. CNIL — "Guide du sous-traitant" (2024) : https://www.cnil.fr/fr/guide-du-sous-traitant
2. Anthropic — "Data Processing Addendum" (2025) : https://www.anthropic.com/legal/dpa
3. ICO — "SaaS and Cloud Computing GDPR Guidance" (2025) : https://ico.org.uk/for-organisations/guide-to-data-protection/
