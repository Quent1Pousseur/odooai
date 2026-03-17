"""
Module: knowledge/rag.py
Role: RAG engine — index ALL Odoo knowledge, retrieve the right context.
      Uses ChromaDB (local). ZERO API tokens for retrieval.
Dependencies: chromadb, knowledge schemas
"""

from __future__ import annotations

import contextlib
from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

_COLLECTION_NAME = "odoo_knowledge"


def build_rag_index(
    version: str = "17.0",
    store_path: Path | None = None,
) -> dict[str, int]:
    """Build the RAG index from ALL KGs + BA Profiles."""
    import chromadb

    from odooai.knowledge.storage import load_module_kg

    path = store_path or Path("knowledge_store")
    version_path = path / version

    if not version_path.exists():
        return {"chunks": 0, "modules": 0}

    db = chromadb.PersistentClient(path=str(path / "vectordb"))
    with contextlib.suppress(Exception):
        db.delete_collection(_COLLECTION_NAME)

    collection = db.create_collection(
        name=_COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    chunks: list[str] = []
    ids: list[str] = []
    metas: list[dict[str, Any]] = []
    n = 0  # unique counter
    module_count = 0

    for module_dir in sorted(version_path.iterdir()):
        if module_dir.name.startswith("_") or not module_dir.is_dir():
            continue
        kg = load_module_kg(module_dir.name, version, store_path=path)
        if kg is None:
            continue
        module_count += 1
        mod = kg.manifest.technical_name

        for model in kg.models:
            if model.is_extension and len(model.fields) < 3:
                continue

            # Model chunk
            fnames = list(model.fields.keys())[:10]
            sf = model.fields.get("state")
            states = ""
            if sf and isinstance(sf.selection, list):
                sv = [s[0] if isinstance(s, list) else s for s in sf.selection]
                states = f" States: {' > '.join(sv)}."
            n += 1
            chunks.append(
                f"{model.name} ({mod}): {model.description or 'Modele Odoo'}. "
                f"Champs: {', '.join(fnames)}.{states}"
            )
            ids.append(f"c{n}")
            metas.append({"type": "model", "module": mod, "model": model.name})

            # Computed fields
            comp = [f for f, fd in model.fields.items() if fd.compute]
            if comp:
                n += 1
                chunks.append(f"Champs calcules {model.name}: {', '.join(comp[:10])}.")
                ids.append(f"c{n}")
                metas.append({"type": "computed", "module": mod, "model": model.name})

            # Relations
            rels = [
                f"{f} > {fd.relation}"
                for f, fd in model.fields.items()
                if fd.type in ("many2one", "one2many") and fd.relation
            ]
            if rels:
                n += 1
                chunks.append(f"Relations {model.name}: {'; '.join(rels[:8])}.")
                ids.append(f"c{n}")
                metas.append({"type": "relation", "module": mod, "model": model.name})

        # Action flows
        for af in kg.action_flows:
            efx = []
            for e in af.effects:
                if e.type == "state_change":
                    efx.append(f"state {e.field}={e.value}")
                elif e.type in ("create", "write"):
                    efx.append(f"{e.type} {e.target_model}")
            if efx or af.env_refs or af.calls:
                n += 1
                parts = [f"Action {af.model}.{af.method_name}:"]
                if efx:
                    parts.append(f" Effets: {', '.join(efx)}.")
                if af.env_refs:
                    parts.append(f" Refs: {', '.join(af.env_refs[:5])}.")
                if af.calls:
                    parts.append(f" Calls: {', '.join(af.calls[:5])}.")
                chunks.append("".join(parts))
                ids.append(f"c{n}")
                metas.append({"type": "action", "module": mod, "model": af.model})

    # BA Profiles
    ba_path = version_path / "_ba_profiles"
    if ba_path.exists():
        import json

        from odooai.knowledge.schemas.ba_profile import BAProfile

        for bp_file in sorted(ba_path.glob("*.json")):
            try:
                data = json.loads(bp_file.read_text(encoding="utf-8"))
                profile = BAProfile.model_validate(data)

                for qa in profile.qa_pairs:
                    n += 1
                    chunks.append(
                        f"Q: {qa.question} "
                        f"Chercher: {', '.join(qa.models_to_query)} "
                        f"Champs: {', '.join(qa.fields_to_fetch)}. "
                        f"Filtre: {qa.domain_filter_example}"
                    )
                    ids.append(f"c{n}")
                    metas.append({"type": "qa", "module": profile.domain_id})

                for wf in profile.workflows:
                    n += 1
                    steps = " > ".join(wf.steps[:6]) if wf.steps else ""
                    chunks.append(f"Workflow {wf.name}: {wf.description} Etapes: {steps}.")
                    ids.append(f"c{n}")
                    metas.append({"type": "workflow", "module": profile.domain_id})

                for feat in profile.feature_discoveries:
                    n += 1
                    chunks.append(
                        f"Feature: {feat.name}. {feat.description} Activer: {feat.how_to_activate}."
                    )
                    ids.append(f"c{n}")
                    metas.append({"type": "feature", "module": profile.domain_id})

            except Exception as exc:
                logger.warning("BA chunk failed", error=str(exc))

    # Add in batches
    batch = 500
    for i in range(0, len(chunks), batch):
        end = min(i + batch, len(chunks))
        collection.add(
            documents=chunks[i:end],
            ids=ids[i:end],
            metadatas=metas[i:end],  # type: ignore[arg-type]
        )

    logger.info("RAG index built", chunks=len(chunks), modules=module_count)
    return {"chunks": len(chunks), "modules": module_count}


def query_rag(
    question: str,
    n_results: int = 5,
    store_path: Path | None = None,
) -> list[dict[str, Any]]:
    """Query the RAG index."""
    import chromadb

    path = store_path or Path("knowledge_store")
    try:
        db = chromadb.PersistentClient(path=str(path / "vectordb"))
        collection = db.get_collection(_COLLECTION_NAME)
    except Exception:
        return []

    results = collection.query(query_texts=[question], n_results=n_results)
    if not results or not results["documents"]:
        return []

    output: list[dict[str, Any]] = []
    for i, doc in enumerate(results["documents"][0]):
        output.append(
            {
                "text": doc,
                "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                "distance": results["distances"][0][i] if results["distances"] else 0,
            }
        )
    return output


def get_context_for_question(question: str, n_results: int = 5) -> str:
    """Get RAG context as a string for the LLM prompt."""
    results = query_rag(question, n_results=n_results)
    if not results:
        return ""
    parts = ["Contexte Odoo :"]
    for r in results:
        parts.append(f"- {r['text']}")
    return "\n".join(parts)
