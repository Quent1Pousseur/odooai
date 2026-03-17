"""
Module: knowledge/_ba_prompt.py
Role: Build prompts for BA Profile generation.
      V3: uses Business Extractor for pre-digested intelligence.
Dependencies: knowledge schemas, business_extractor
"""

from __future__ import annotations

from odooai.knowledge.business_extractor import extract_business
from odooai.knowledge.schemas.index import ModuleKnowledgeGraph
from odooai.services.field_scorer import select_top_fields


def build_kg_summary(kgs: list[ModuleKnowledgeGraph], domain_id: str = "") -> str:
    """
    Build a BUSINESS-ORIENTED summary of KGs for LLM consumption.

    Uses the Business Extractor to pre-digest intelligence (0 tokens).
    The LLM receives structured business data, not raw field lists.
    """
    # Phase 1: extract business intelligence (Python, 0 tokens)
    biz = extract_business(kgs, domain_id)

    parts: list[str] = []

    # Workflows — the most valuable info
    if biz.workflows:
        parts.append("=== WORKFLOWS ===")
        for wf in biz.workflows:
            states = " → ".join(wf.states) if wf.states else "unknown"
            parts.append(f"{wf.model}: {states}")
            for t in wf.transitions:
                parts.append(f"  {t.method} → {t.to_state}")
            if wf.timeline_fields:
                parts.append(f"  Dates: {', '.join(wf.timeline_fields)}")
        parts.append("")

    # Action flows — what each action DOES
    if biz.action_flows:
        parts.append("=== ACTION FLOWS ===")
        for af in biz.action_flows:
            parts.append(f"{af.trigger_model}.{af.trigger_method}:")
            state_changes = [e for e in af.effects if e.type == "state_change"]
            for sc in state_changes:
                parts.append(f"  → state_change: {sc.field} = {sc.value}")
            if af.calls_methods:
                parts.append(f"  → calls: {', '.join(af.calls_methods)}")
            env_refs = [e.target_model for e in af.effects if e.type == "env_ref"]
            if env_refs:
                parts.append(f"  → refs: {', '.join(env_refs)}")
        parts.append("")

    # Relations — how models connect
    if biz.dependency_graph.relations:
        parts.append("=== RELATIONS ===")
        seen: set[str] = set()
        for rel in biz.dependency_graph.relations:
            key = f"{rel.source}.{rel.field}"
            if key in seen:
                continue
            seen.add(key)
            req = " (required)" if rel.required else ""
            parts.append(f"  {rel.source}.{rel.field} → {rel.target} [{rel.type}]{req}")
        parts.append("")

    # Field intents — grouped by intent
    if biz.field_intents:
        parts.append("=== CHAMPS PAR INTENTION BUSINESS ===")
        intents: dict[str, list[str]] = {}
        for fi in biz.field_intents:
            intents.setdefault(fi.intent, []).append(f"{fi.model}.{fi.name}")
        for intent, fields in sorted(intents.items()):
            parts.append(f"  {intent.upper()}: {', '.join(fields[:8])}")
        parts.append("")

    # Auto Q&A — the most actionable for LLM
    if biz.auto_qa:
        parts.append("=== QUESTIONS AUTO-GENEREES ===")
        for qa in biz.auto_qa[:10]:
            parts.append(f"  Q: {qa.question}")
            parts.append(f"  → {qa.model} {qa.domain_filter} [{qa.method}]")
            if qa.fields:
                parts.append(f"  → champs: {', '.join(qa.fields)}")
        parts.append("")

    # Computed fields — automation capabilities
    if biz.dependency_graph.computed_fields:
        parts.append("=== CHAMPS CALCULES (automatisation) ===")
        for model_name, fields in list(biz.dependency_graph.computed_fields.items())[:5]:
            parts.append(f"  {model_name}: {', '.join(fields[:5])}")
        parts.append("")

    # Key models with top fields (compact)
    parts.append("=== MODELES PRINCIPAUX ===")
    for kg in kgs:
        for model in kg.models:
            if model.is_extension or len(model.fields) < 5:
                continue
            fields_meta = {
                f.name: {"type": f.type, "required": f.required} for f in model.fields.values()
            }
            top = select_top_fields(fields_meta, top_n=7)
            top_str = ", ".join(top)
            parts.append(f"  {model.name} ({len(model.fields)} champs): {top_str}")

    return "\n".join(parts)


def build_ba_messages(
    domain_name: str,
    domain_id: str,
    kg_summary: str,
    language: str = "fr",
) -> list[dict[str, str]]:
    """Build the messages list for BA Profile generation LLM call."""
    system = f"""Tu es un expert en REVERSE ENGINEERING business d'Odoo.

Ton travail : transformer du CODE SOURCE en INTELLIGENCE BUSINESS.
Odoo a ete cree pour repondre a des besoins business. Chaque modele,
chaque champ, chaque contrainte, chaque workflow existe parce qu'un
besoin business l'a demande. TON JOB est de retrouver ce besoin.

Exemples de reverse engineering :
- Un champ `state` avec ['draft','confirmed','done'] → c'est un workflow
  de validation en 3 etapes. Le business a besoin de controler les etapes.
- Une contrainte `CHECK(amount > 0)` → le business interdit les montants
  negatifs pour eviter les erreurs de saisie.
- Un champ `compute='_compute_margin'` → le business veut voir sa marge
  en temps reel sans la calculer a la main.
- Un `@api.onchange('partner_id')` → quand on change le client, le
  systeme met a jour automatiquement l'adresse, les conditions, etc.
- Un champ `tracking=True` → le business veut l'historique des changements
  pour l'audit et la tracabilite.

Tu connais les VRAIS workflows Odoo, les bonnes pratiques, les pieges.
Tu sais POURQUOI chaque fonctionnalite existe — quel probleme business
elle resout.

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
