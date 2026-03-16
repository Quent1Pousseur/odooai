"""
Module: knowledge/index.py
Role: Inverse index for Knowledge Graphs — O(1) lookups.
      Learning Data Engineer (11): field→module→model.
Dependencies: knowledge/storage
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import structlog

logger = structlog.get_logger(__name__)

# In-memory inverse index
_field_index: dict[str, list[dict[str, str]]] = {}
_model_index: dict[str, list[str]] = {}
_loaded = False


def build_index(version: str = "17.0", store_path: Path | None = None) -> None:
    """Build inverse index from all stored KGs."""
    global _loaded
    from odooai.knowledge.storage import load_module_kg

    path = store_path or Path("knowledge_store")
    version_path = path / version

    if not version_path.exists():
        logger.warning("Version path not found", path=str(version_path))
        return

    count = 0
    for module_dir in sorted(version_path.iterdir()):
        if module_dir.name.startswith("_") or not module_dir.is_dir():
            continue

        kg = load_module_kg(module_dir.name, version, store_path=path)
        if kg is None:
            continue

        for model in kg.models:
            # Model index: model_name → [module1, module2]
            if model.name not in _model_index:
                _model_index[model.name] = []
            if kg.manifest.technical_name not in _model_index[model.name]:
                _model_index[model.name].append(kg.manifest.technical_name)

            # Field index: field_name → [{model, module, type}]
            for field_name, field_def in model.fields.items():
                if field_name not in _field_index:
                    _field_index[field_name] = []
                _field_index[field_name].append(
                    {
                        "model": model.name,
                        "module": kg.manifest.technical_name,
                        "type": field_def.type,
                    }
                )

        count += 1

    _loaded = True
    logger.info(
        "KG index built",
        modules=count,
        models=len(_model_index),
        fields=len(_field_index),
    )


def lookup_field(field_name: str) -> list[dict[str, str]]:
    """Find all models/modules that define a field."""
    return _field_index.get(field_name, [])


def lookup_model(model_name: str) -> list[str]:
    """Find all modules that define or extend a model."""
    return _model_index.get(model_name, [])


def get_index_stats() -> dict[str, Any]:
    """Return index statistics."""
    return {
        "loaded": _loaded,
        "models": len(_model_index),
        "fields": len(_field_index),
    }
