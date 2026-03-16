# OdooAI — Pitch, Personas & Aha Moment

## Pitch

### En 10 mots
**"Votre Odoo peut faire plus. L'IA vous montre comment."**

> **Sales (05)** : Court, concret, parle a Marie. Pas de jargon technique.
>
> **CEO (01)** : Ca positionne OdooAI comme un revelateur de potentiel, pas un outil technique.
>
> **CPO (03)** : Le "vous montre comment" implique de l'action, pas juste de l'information.

### Variantes testables en interview
- "L'expert Odoo IA qui connait chaque fonctionnalite de votre ERP."
- "Arretez de payer un consultant. Demandez a l'IA."
- "Vous utilisez 30% d'Odoo. On active les 70% restants."

### Elevator pitch (30 secondes)
"Les PME n'utilisent que 30% des capacites de leur Odoo. Les consultants coutent 150-300€/h et ne sont la que temporairement. OdooAI est un Business Analyst IA qui a lu chaque ligne du code source d'Odoo. Il se connecte a votre instance, detecte ce que vous n'utilisez pas, et vous montre comment en tirer profit. 24h/24, dans votre langue, a partir de 49€/mois."

---

## Personas

### Marie — La dirigeante pragmatique
- **Profil** : CEO d'une PME de 15 employes, import-export de produits alimentaires
- **Odoo** : Utilise depuis 2 ans. Modules actifs : ventes, achats, stock, comptabilite
- **Frustration** : "Je sais qu'Odoo peut faire plus mais je n'ai pas le temps d'explorer. La derniere mission de consulting m'a coute 4500€ pour configurer les rappels de paiement."
- **Besoin** : Comprendre ce qu'Odoo peut faire pour elle sans lire la doc et sans payer un consultant
- **Aha moment** : OdooAI lui dit "Saviez-vous que votre module Stock peut automatiser les receptions en 3 etapes ? Actuellement vous faites tout manuellement."
- **Niveau technique** : Faible. Parle business, pas `ir.model`.
- **Budget** : Prete a payer 49-149€/mois si ca remplace un consulting a 1500€/jour
- **Citation** : "Je veux quelqu'un qui me dise : voila ce que tu rates, et voila comment l'activer."

### Thomas — Le responsable operationnel
- **Profil** : Responsable logistique, 28 ans, dans une PME industrielle de 40 employes
- **Odoo** : Power user du module Stock, connait bien la gestion d'entrepots
- **Frustration** : "Je gere bien le stock mais je galere avec la fabrication (MRP). J'ai demande une formation, on m'a dit que c'etait 2000€ pour 2 jours."
- **Besoin** : Apprendre a utiliser les modules qu'il ne connait pas, avec des guides pas-a-pas
- **Aha moment** : OdooAI lui genere un plan d'action pour connecter son stock a la fabrication, avec les champs a configurer et l'ordre des operations
- **Niveau technique** : Moyen. Comprend les concepts Odoo mais pas le code.
- **Budget** : Ne decide pas du budget, mais recommande a Marie
- **Citation** : "Si l'IA peut me faire un tuto specifique a MA configuration, je gagne des semaines."

### Sophie — La CEO startup
- **Profil** : Fondatrice d'une startup SaaS B2B, 8 employes, vient d'installer Odoo
- **Odoo** : Debutante totale. A installe Odoo sur recommandation d'un ami. Ne sait pas par ou commencer.
- **Frustration** : "J'ai installe 12 modules et je ne sais meme pas lesquels je devrais utiliser. L'interface est enorme."
- **Besoin** : Un guide de demarrage personnalise qui tient compte de son business (SaaS B2B)
- **Aha moment** : OdooAI analyse ses modules installes et dit "Pour un SaaS B2B, voici les 5 premieres choses a configurer, dans cet ordre"
- **Niveau technique** : Tres faible. Vient du marketing.
- **Budget** : Bootstrapped, sensible au prix. Plan Starter 49€/mois max.
- **Citation** : "J'ai besoin qu'on me prenne par la main, pas qu'on me donne 200 pages de doc."

---

## Aha Moment

### Definition
> Le aha moment = la premiere fois qu'OdooAI revele a l'utilisateur une fonctionnalite Odoo qu'il ne connaissait pas et qui resout un vrai probleme business.

### Parcours vers le aha moment

```
1. Connexion Odoo (30 sec)
   → L'utilisateur entre URL + credentials
   → OdooAI detecte les modules installes et la version

2. Analyse automatique (10 sec)
   → OdooAI compare la configuration actuelle aux Knowledge Graphs
   → Identifie les fonctionnalites non-activees

3. AHA MOMENT (< 2 min apres connexion)
   → "Saviez-vous que votre module [X] peut aussi [Y] ?"
   → Explication en langage business, pas technique
   → Plan d'action concret : "Voici comment l'activer en 3 etapes"

4. Premiere action guidee (5 min)
   → L'utilisateur suit le plan
   → OdooAI valide chaque etape
   → Resultat visible immediatement
```

### Metriques du aha moment
- **Time to aha** : < 2 minutes apres connexion (cible)
- **Aha rate** : % d'utilisateurs qui declarent avoir decouvert quelque chose (cible > 80%)
- **Action rate** : % d'utilisateurs qui executent la premiere action (cible > 50%)

> **SaaS Architect (06)** : "Si le time-to-aha depasse 5 minutes, on perd 80% des utilisateurs. Tout le produit doit etre designe autour de ce moment."
>
> **Customer Success (17)** : "Le aha moment doit etre personnalise. Pas le meme message pour Marie (stock 3 etapes) et Sophie (guide demarrage). Les Knowledge Graphs permettent ca."

---

## Script d'Interview PME (CPO + Customer Success)

### Objectif
Valider que le probleme existe et que notre solution resonne.

### Questions (15-20 min)

**Contexte (3 min)**
1. Depuis combien de temps utilisez-vous Odoo ?
2. Quels modules utilisez-vous au quotidien ?
3. Combien de personnes utilisent Odoo dans votre entreprise ?

**Probleme (5 min)**
4. Estimez-vous utiliser Odoo a son plein potentiel ? (echelle 1-10)
5. Avez-vous deja eu l'impression qu'Odoo pouvait faire quelque chose mais sans savoir comment ?
6. Avez-vous fait appel a un consultant Odoo ? Si oui, pour quoi et combien ca a coute ?
7. Comment trouvez-vous les reponses a vos questions sur Odoo aujourd'hui ?

**Solution (5 min)**
8. Si un assistant IA pouvait analyser votre configuration Odoo et vous dire "voila ce que vous n'utilisez pas et comment l'activer", est-ce que ca vous interesserait ?
9. Quelle serait la premiere chose que vous lui demanderiez ?
10. A quel prix mensuel ca deviendrait une evidence ? Un luxe ? Trop cher ?

**Closing (2 min)**
11. Seriez-vous interesse par une demo quand le produit sera pret ?
12. Connaissez-vous d'autres PME qui pourraient etre interessees ?

### Reponses a tracker
- [ ] Taux d'utilisation percu (Q4)
- [ ] Cout consulting passe (Q6)
- [ ] Premiere question a l'IA (Q9)
- [ ] Willingness to pay (Q10)
- [ ] Intent to demo (Q11)
- [ ] Referral (Q12)
