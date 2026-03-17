# R&D — OdooAI Innovation Lab

Projets internes des agents. Innovation, prototypes, POCs.

## Structure

```
docs/rnd/
  README.md                    # Ce fichier
  NN-nom-projet.md             # Doc du projet (template dans docs/TEMPLATES.md)

rnd/
  nom-projet/                  # Code du projet (si applicable)
    README.md                  # Description + comment lancer
    ...                        # Code source du prototype
```

**2 endroits distincts :**
- `docs/rnd/` → documentation, plan, avancement
- `rnd/` (racine) → code source des prototypes

**Le code R&D ne va JAMAIS dans odooai/ ou frontend/.** C'est isole tant que le projet n'est pas adopte. Quand un projet passe en "Adopt", son code est merge dans le code principal via une PR.

## Regles
- Propose au meeting, valide par CTO/fondateur
- MVP obligatoire en 1-2 sprints
- Documentation a jour a chaque session
- Show & Tell a chaque sprint
- Budget max $50/sprint (approuve CFO)
- Voir docs/hr/cellule-rnd.md pour les details complets
