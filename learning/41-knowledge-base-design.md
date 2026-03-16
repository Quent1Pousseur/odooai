# Learning — Support Engineer (41) — Knowledge Base Design
## Date : 2026-03-20
## Duree : 3 heures

## Ce que j'ai appris

### Structure d'une knowledge base efficace
- **Categorie > Article > Section** — hierarchie a 3 niveaux max
- Chaque article repond a UNE question precise
- Format : Probleme → Solution → Etapes → Resultat attendu
- Les articles les plus consultes en premier (pareto : 20% des articles resolvent 80% des tickets)

### Patterns de support SaaS
- **Tier 1** : FAQ + Knowledge Base → self-service (cible : 60% des questions)
- **Tier 2** : Chat avec support humain → resolution guidee
- **Tier 3** : Escalade technique → devs
- OdooAI est dans une position unique : l'IA EST le tier 1

### Categories identifiees pour OdooAI
1. **Demarrage** : Connexion, premier message, comprendre les reponses
2. **Connexion Odoo** : URL, DB, API Key, erreurs courantes
3. **Fonctionnalites** : Que peut faire OdooAI ? Domaines couverts
4. **Securite** : Mes donnees sont-elles en securite ? Anonymisation
5. **Facturation** : Plans, upgrade, annulation
6. **Troubleshooting** : Reponses vides, erreurs, lenteur

### FAQ initiale (20 questions — issue #17)
Les questions les plus probables des premiers beta users :
1. Comment connecter mon Odoo ?
2. OdooAI peut-il modifier mes donnees ?
3. Mes donnees sont-elles envoyees a un tiers ?
4. Quels modules Odoo sont supportes ?
5. Pourquoi la reponse est-elle lente ?
6. L'IA se trompe, que faire ?
7. Comment creer une cle API Odoo ?
8. OdooAI fonctionne-t-il avec Odoo Community ?
9. Puis-je utiliser OdooAI sans connexion internet ?
10. Comment supprimer mes conversations ?

## Comment ca s'applique a OdooAI

- La KB doit etre prete AVANT les premiers beta users
- Les 9 BA Profiles sont une mine d'or pour generer des articles
- Le format question/reponse est naturel pour un produit de chat
- Integrer la KB dans le chat : si l'utilisateur pose une question de support, rediriger vers l'article

## Ce que je recommande

1. Sprint 4 : FAQ 20 questions (issue #17) — en cours
2. Sprint 5 : Knowledge Base structuree dans le site (/help)
3. Sprint 5 : In-app help (tooltip "?" sur les boutons)
4. Sprint 6 : Chatbot de support (different du BA — repond aux questions produit)

## Sources
- Intercom Knowledge Base best practices
- Zendesk Help Center design guide
- "The Effortless Experience" — Matthew Dixon
