# OdooAI — Conformite EU AI Act (DRAFT)
## Redige par : AI Safety & Ethics (33) + Legal (16)
## Date : 2026-03-20
## Status : DRAFT

---

## 1. Classification

OdooAI est un **systeme IA a risque limite** selon l'EU AI Act (Reglement 2024/1689).

**Pourquoi "limited risk" et pas "high risk" :**
- OdooAI ne prend PAS de decisions automatisees sur les personnes
- OdooAI ne fait PAS de scoring credit, recrutement, ou notation sociale
- OdooAI est un outil d'aide a la decision — l'humain decide toujours

**Article applicable** : Article 50 — Obligations de transparence

---

## 2. Obligations et conformite

### 2.1 Transparence — "L'utilisateur sait qu'il parle a une IA"

| Obligation | Status | Implementation |
|-----------|--------|---------------|
| Informer que le contenu est genere par IA | ✅ Fait | Nom "OdooAI" + disclaimer chaque reponse |
| Ne pas faire croire que c'est un humain | ✅ Fait | Branding explicite "Business Analyst IA" |
| Citer les sources | ✅ Fait | Module, modele, champ cites dans les reponses |
| Expliquer les limites | ✅ Fait | "OdooAI peut se tromper", "pas de conseil legal/fiscal" |
| Page d'information sur l'IA | ⬜ A faire | Page /about-ai sur le site |

### 2.2 Supervision humaine

| Obligation | Status | Implementation |
|-----------|--------|---------------|
| L'humain peut ignorer les recommandations | ✅ By design | OdooAI recommande, l'utilisateur decide |
| L'humain peut desactiver le systeme | ✅ By design | Deconnexion a tout moment |
| Pas d'action automatique sans validation | ✅ By design | Lecture seule, aucune modification Odoo |

### 2.3 Donnees et vie privee

| Obligation | Status | Implementation |
|-----------|--------|---------------|
| Politique de confidentialite | ✅ Draft | business/privacy-policy-draft.md |
| Anonymisation des donnees sensibles | ✅ Fait | Security Guardian anonymise RH, salaires |
| Droit a la suppression | ⬜ A faire | Suppression des conversations a implementer |
| Information sur les sous-traitants | ⬜ A faire | Mentionner Anthropic dans la privacy policy |

### 2.4 Audit et tracabilite

| Obligation | Status | Implementation |
|-----------|--------|---------------|
| Logs des recommandations | ⬜ A faire | Audit trail dans la DB (Sprint 5) |
| Documentation technique | ✅ Partiel | Specs, reviews, architecture documentees |
| Evaluation des risques | ✅ Fait | Ce document + red teaming effectue |

---

## 3. Risques identifies et mitigations

| Risque | Probabilite | Mitigation |
|--------|------------|------------|
| Hallucination (fausse recommandation) | Moyenne | Disclaimer + sources citees + eval framework |
| Mauvais conseil comptable | Faible | Disclaimer explicite "pas de conseil fiscal/comptable" |
| Fuite de donnees sensibles | Tres faible | Guardian anonymise avant envoi a Anthropic |
| Biais dans les recommandations | Faible | BA Profiles bases sur le code source, pas sur des donnees utilisateur |
| Dependance excessive a l'IA | Faible | Lecture seule — l'utilisateur doit agir manuellement dans Odoo |

---

## 4. Plan de conformite

### Sprint 4 (maintenant)
- [x] Disclaimer dans chaque reponse
- [x] Branding transparent "IA"
- [x] Anonymisation Security Guardian
- [x] Ce document de conformite

### Sprint 5
- [ ] Page /about-ai sur le site
- [ ] Mentionner Anthropic dans la privacy policy
- [ ] Audit trail des recommandations en DB

### Sprint 6
- [ ] Droit a la suppression des conversations
- [ ] Evaluation formelle des risques (selon template NIST AI RMF)

### Avant beta publique
- [ ] Validation juridique du document par un avocat
- [ ] DPA (Data Processing Agreement) avec Anthropic
- [ ] Mise en conformite GDPR complete

---

## 5. Declaration de transparence (a publier sur /about-ai)

> **Comment OdooAI utilise l'intelligence artificielle**
>
> OdooAI utilise le modele Claude d'Anthropic pour generer des recommandations sur l'utilisation d'Odoo. Voici ce que vous devez savoir :
>
> - **Ce n'est PAS un humain.** Toutes les reponses sont generees par une IA.
> - **L'IA peut se tromper.** Verifiez toujours les recommandations avant d'agir.
> - **Vos donnees sont protegees.** Les informations sensibles (RH, salaires) sont anonymisees avant d'etre traitees par l'IA.
> - **Pas de conseil legal/fiscal.** OdooAI ne remplace pas un expert-comptable ou un avocat.
> - **Vous restez en controle.** OdooAI ne modifie jamais vos donnees Odoo. Vous decidez quoi faire des recommandations.
>
> Pour toute question : contact@odooai.com

---

*A valider par un avocat specialise en droit du numerique et reglementation IA.*
