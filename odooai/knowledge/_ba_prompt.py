"""
Module: knowledge/_ba_prompt.py
Role: Build prompts for BA Profile generation.
      V2: enriched with workflows, Q&A, field hints.
Dependencies: knowledge schemas
"""

from __future__ import annotations

from odooai.knowledge.schemas.index import ModuleKnowledgeGraph
from odooai.services.field_scorer import select_top_fields


def build_kg_summary(kgs: list[ModuleKnowledgeGraph]) -> str:
    """
    Build a concise summary of Knowledge Graphs for LLM consumption.

    Extracts: models, key fields, actions, constraints, onchange, compute.
    Targets ~2000-3000 tokens.
    """
    parts: list[str] = []

    for kg in kgs:
        parts.append(f"## Module: {kg.manifest.name} ({kg.manifest.technical_name})")
        parts.append(f"Depends: {', '.join(kg.manifest.depends)}")
        parts.append("")

        for model in kg.models:
            if model.is_extension and len(model.fields) < 3:
                continue

            label = "[EXT]" if model.is_extension else ""
            parts.append(f"### {model.name} {label}")
            if model.description:
                parts.append(f"Description: {model.description}")

            # Selection fields — show the states/options
            for fname, f in model.fields.items():
                if f.type == "selection" and isinstance(f.selection, list) and len(f.selection) > 0:
                        opts = ", ".join(
                            str(s[0]) if isinstance(s, list) else str(s) for s in f.selection[:8]
                        )
                        parts.append(f"  STATE {fname}: {opts}")

            # Top fields
            fields_meta = {
                f.name: {"type": f.type, "required": f.required} for f in model.fields.values()
            }
            top = select_top_fields(fields_meta, top_n=10)

            for fname in top:
                if fname not in model.fields:
                    continue
                f = model.fields[fname]
                extras: list[str] = []
                if f.required:
                    extras.append("required")
                if f.compute:
                    extras.append(f"compute={f.compute}")
                if f.relation:
                    extras.append(f"-> {f.relation}")
                if f.related:
                    extras.append(f"related={f.related}")
                info = f" ({', '.join(extras)})" if extras else ""
                parts.append(f"  - {fname}: {f.type}{info}")

            parts.append("")

        # Actions — include all, they tell the story
        if kg.action_methods:
            parts.append("Actions:")
            for a in kg.action_methods[:15]:
                parts.append(f"  - {a.model}.{a.name}")

        # Onchange methods
        if kg.onchange_methods:
            parts.append("Onchange:")
            for o in kg.onchange_methods[:10]:
                parts.append(f"  - {o.method_name} (fields: {o.fields})")

        # Constraints
        if kg.python_constraints:
            parts.append("Constraints Python:")
            for c in kg.python_constraints[:5]:
                parts.append(f"  - {c.method_name}: fields={c.fields}")

        if kg.sql_constraints:
            parts.append("Constraints SQL:")
            for sc in kg.sql_constraints[:5]:
                parts.append(f"  - {sc.name}: {sc.message}")

        parts.append("")

    return "\n".join(parts)


def build_ba_messages(
    domain_name: str,
    domain_id: str,
    kg_summary: str,
    language: str = "fr",
) -> list[dict[str, str]]:
    """Build the messages list for BA Profile generation LLM call."""
    system = f"""Tu es un expert Odoo senior avec 10 ans d'experience.
Tu analyses le code source d'un domaine Odoo et tu generes un profil
d'intelligence business ACTIONNABLE pour les PME.

Tu connais les VRAIS workflows Odoo, les bonnes pratiques, les pieges.
Tu sais comment les modules s'interconnectent.

Reponds en {language.upper()} uniquement.
Format de sortie : JSON strict, pas de markdown, pas de commentaires."""

    user = f"""Voici le schema technique du domaine "{domain_name}"
extrait du code source Odoo 17 :

{kg_summary}

Genere un BA Profile JSON ENRICHI avec cette structure :
{{
  "summary": "3 phrases : ce que ce domaine fait, pour qui, la valeur business",

  "workflows": [
    {{
      "name": "Nom du workflow (ex: Cycle de vente)",
      "description": "Explication business en 2 phrases",
      "steps": ["Etape 1 : ...", "Etape 2 : ...", "..."],
      "models_involved": ["sale.order", "stock.picking", "account.move"],
      "key_fields_per_step": {{
        "sale.order": ["state", "partner_id", "amount_total"],
        "stock.picking": ["state", "scheduled_date"]
      }}
    }}
  ],

  "capabilities": [
    {{
      "name": "Nom de la capacite",
      "description": "Description business (PAS technique)",
      "key_models": ["modele1"],
      "common_workflows": ["workflow1"]
    }}
  ],

  "feature_discoveries": [
    {{
      "name": "Fonctionnalite peu connue",
      "module": "nom_module",
      "model": "nom.modele",
      "field_or_setting": "nom_champ_ou_config",
      "description": "Ce que ca fait concretement",
      "business_value": "Impact business mesurable",
      "how_to_activate": "Menu > Sous-menu > Option exacte",
      "prerequisites": ["prerequis"],
      "complexity": "simple|medium|complex"
    }}
  ],

  "qa_pairs": [
    {{
      "question": "Question typique d'un gerant PME",
      "answer": "Reponse directe avec les modeles et champs a interroger",
      "models_to_query": ["modele1"],
      "fields_to_fetch": ["field1", "field2"],
      "domain_filter_example": "[('state','=','draft')]"
    }}
  ],

  "gotchas": [
    {{
      "description": "Piege courant",
      "source_model": "modele",
      "source_constraint": "contrainte",
      "workaround": "Comment eviter"
    }}
  ],

  "recommended_config": {{
    "small_company": "Config recommandee pour < 20 employes",
    "medium_company": "Config recommandee pour 20-100 employes",
    "large_company": "Config recommandee pour > 100 employes"
  }},

  "cross_module_combos": ["Module A + Module B : explication de la synergie"],
  "limitations": ["limitation1"]
}}

IMPORTANT :
- Genere au moins 3 workflows DETAILLES avec les etapes et modeles
- Genere au moins 10 qa_pairs (les questions les plus courantes)
- Genere au moins 7 feature_discoveries ACTIONNABLES
- Genere au moins 5 gotchas
- Les qa_pairs DOIVENT inclure les modeles et champs exacts a interroger
- Les workflows DOIVENT montrer les interdependances entre modules
- Sois CONCRET : noms de menus, noms de champs, pas de generalites"""

    return [
        {"role": "system", "content": system},
        {"role": "user", "content": user},
    ]
