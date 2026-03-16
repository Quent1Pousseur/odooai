# Learning — AI Safety & Ethics (33) — EU AI Act Limited Risk
## Date : 2026-03-20
## Duree : 5 heures

## Ce que j'ai appris

### Classification d'OdooAI selon l'EU AI Act
- OdooAI est un **systeme IA a risque limite** (Article 50)
- Pas "haut risque" car on ne prend pas de decisions automatisees sur les personnes
- Obligation principale : **transparence** — l'utilisateur doit savoir qu'il parle a une IA

### Obligations concretes pour un systeme "limited risk"
1. **Disclosure** : informer que le contenu est genere par IA
2. **Human oversight** : l'utilisateur peut toujours ignorer les recommandations
3. **No deception** : ne pas faire croire que c'est un humain qui repond
4. **Data transparency** : expliquer quelles donnees sont utilisees

### Ce qu'on fait deja bien
- Disclaimer en bas de chaque reponse ("OdooAI ne fournit pas de conseil juridique...")
- Le nom "OdooAI" est explicite — c'est une IA
- Les sources sont citees (modules, modeles)
- Le Guardian anonymise les donnees sensibles

### Ce qu'il manque
- **Document de conformite** : un page publique "Comment OdooAI utilise l'IA"
- **Log des decisions** : tracer quand le LLM a fait une recommandation et laquelle
- **Opt-out** : l'utilisateur doit pouvoir desactiver les recommandations automatiques
- **Data processing agreement** : pour les clients entreprise

### NIST AI Risk Management Framework (complement)
- Gouvernance : qui est responsable des outputs de l'IA ? (nous)
- Mapping : quels risques specifiques ? (hallucination, mauvais conseil comptable)
- Mesure : comment on detecte les problemes ? (eval framework)
- Management : comment on corrige ? (feedback loop, retraining prompts)

## Comment ca s'applique a OdooAI

- Le disclaimer actuel est **necessaire mais insuffisant**
- Il faut une page `/about-ai` sur le site expliquant le fonctionnement
- Les reponses comptables/fiscales doivent avoir un warning PLUS visible
- L'eval framework de Data Scientist (28) est critique pour la conformite

## Ce que je recommande

1. Creer un document "AI Transparency" pour le site (Sprint 4)
2. Ajouter un warning renforce sur les reponses comptables (highlight rouge)
3. Logger chaque recommandation dans un audit trail (Sprint 5)
4. Preparer un Data Processing Agreement template pour les clients enterprise

## Sources
- EU AI Act texte officiel (eur-lex.europa.eu)
- NIST AI RMF 1.0 (nist.gov)
- Article 50 — Transparency obligations for limited risk AI
