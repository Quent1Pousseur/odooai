"""
Module: knowledge/_ba_prompt.py
Role: Build prompts for BA Profile generation.
Dependencies: knowledge schemas
"""

from __future__ import annotations

from odooai.knowledge.schemas.index import ModuleKnowledgeGraph
from odooai.services.field_scorer import select_top_fields


def build_kg_summary(kgs: list[ModuleKnowledgeGraph]) -> str:
    """
    Build a concise summary of Knowledge Graphs for LLM consumption.

    Extracts the most important information: models, key fields,
    actions, constraints. Targets ~2000-3000 tokens.
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
                    extras.append("computed")
                if f.relation:
                    extras.append(f"-> {f.relation}")
                info = f" ({', '.join(extras)})" if extras else ""
                parts.append(f"  - {fname}: {f.type}{info}")

            parts.append("")

        if kg.action_methods:
            action_names = [a.name for a in kg.action_methods[:10]]
            parts.append(f"Actions: {', '.join(action_names)}")

        if kg.sql_constraints:
            parts.append(f"SQL Constraints: {len(kg.sql_constraints)}")
            for c in kg.sql_constraints[:5]:
                parts.append(f"  - {c.name}: {c.message}")

        parts.append("")

    return "\n".join(parts)


def build_ba_messages(
    domain_name: str,
    domain_id: str,
    kg_summary: str,
    language: str = "fr",
) -> list[dict[str, str]]:
    """Build the messages list for BA Profile generation LLM call."""
    system = f"""Tu es un Business Analyst expert Odoo. Tu analyses le schema technique
d'un domaine fonctionnel et tu produis un profil d'intelligence business.

Ton objectif : aider les PME a decouvrir les fonctionnalites qu'elles n'utilisent pas.

Reponds en {language.upper()} uniquement.
Format de sortie : JSON strict, pas de markdown, pas de commentaires."""

    user = f"""Voici le schema technique du domaine "{domain_name}" extrait du code source Odoo :

{kg_summary}

Genere un BA Profile JSON avec cette structure exacte :
{{
  "domain_name": "{domain_name}",
  "domain_id": "{domain_id}",
  "summary": "2-3 phrases resumant ce que ce domaine permet de faire pour une PME",
  "capabilities": [
    {{
      "name": "Nom de la capacite",
      "description": "Description business (pas technique)",
      "key_models": ["modele1", "modele2"],
      "common_workflows": ["workflow1", "workflow2"]
    }}
  ],
  "feature_discoveries": [
    {{
      "name": "Nom de la fonctionnalite cachee",
      "module": "nom_module",
      "model": "nom.modele",
      "field_or_setting": "nom_champ_ou_config",
      "description": "Ce que ca fait",
      "business_value": "Pourquoi c'est utile pour la PME",
      "how_to_activate": "Comment l'activer en langage simple",
      "prerequisites": ["prerequis1"],
      "complexity": "simple|medium|complex"
    }}
  ],
  "gotchas": [
    {{
      "description": "Piege ou contrainte",
      "source_model": "modele",
      "source_constraint": "contrainte",
      "workaround": "Comment eviter le probleme"
    }}
  ],
  "cross_module_combos": ["combo1: explication"],
  "limitations": ["limitation1"]
}}

Genere au moins 5 feature_discoveries (les plus utiles pour une PME).
Genere au moins 3 gotchas (les pieges les plus frequents).
Sois concret et actionnable. Pas de generalites."""

    return [
        {"role": "system", "content": system},  # Extracted separately by caller
        {"role": "user", "content": user},
    ]
