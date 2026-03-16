"""
Module: knowledge/storage.py
Role: Read/write Knowledge Graphs as JSON files in knowledge_store/.
Dependencies: pydantic, pathlib
"""

from __future__ import annotations

import json
from pathlib import Path

import structlog

from odooai.knowledge.schemas.index import KnowledgeIndex, ModuleKnowledgeGraph

logger = structlog.get_logger(__name__)

DEFAULT_STORE_PATH = Path("knowledge_store")


def save_module_kg(
    kg: ModuleKnowledgeGraph,
    odoo_version: str,
    store_path: Path = DEFAULT_STORE_PATH,
) -> Path:
    """
    Save a module Knowledge Graph as JSON.

    Creates: knowledge_store/{version}/{module_name}/knowledge.json

    Returns:
        Path to the saved JSON file.
    """
    module_dir = store_path / odoo_version / kg.manifest.technical_name
    module_dir.mkdir(parents=True, exist_ok=True)

    output_file = module_dir / "knowledge.json"
    output_file.write_text(
        kg.model_dump_json(indent=2),
        encoding="utf-8",
    )

    logger.info(
        "Knowledge Graph saved",
        module=kg.manifest.technical_name,
        version=odoo_version,
        path=str(output_file),
    )
    return output_file


def load_module_kg(
    module_name: str,
    odoo_version: str,
    store_path: Path = DEFAULT_STORE_PATH,
) -> ModuleKnowledgeGraph | None:
    """
    Load a module Knowledge Graph from JSON.

    Returns:
        ModuleKnowledgeGraph or None if file not found or invalid.
    """
    kg_file = store_path / odoo_version / module_name / "knowledge.json"
    if not kg_file.exists():
        return None

    try:
        data = json.loads(kg_file.read_text(encoding="utf-8"))
        return ModuleKnowledgeGraph.model_validate(data)
    except Exception as exc:
        logger.error(
            "Failed to load Knowledge Graph",
            module=module_name,
            version=odoo_version,
            error=str(exc),
        )
        return None


def save_index(
    index: KnowledgeIndex,
    store_path: Path = DEFAULT_STORE_PATH,
) -> Path:
    """
    Save a version-level index as JSON.

    Creates: knowledge_store/{version}/_index.json
    """
    version_dir = store_path / index.odoo_version
    version_dir.mkdir(parents=True, exist_ok=True)

    output_file = version_dir / "_index.json"
    output_file.write_text(
        index.model_dump_json(indent=2),
        encoding="utf-8",
    )
    return output_file


def load_index(
    odoo_version: str,
    store_path: Path = DEFAULT_STORE_PATH,
) -> KnowledgeIndex | None:
    """Load a version-level index from JSON."""
    index_file = store_path / odoo_version / "_index.json"
    if not index_file.exists():
        return None

    try:
        data = json.loads(index_file.read_text(encoding="utf-8"))
        return KnowledgeIndex.model_validate(data)
    except Exception as exc:
        logger.error("Failed to load index", version=odoo_version, error=str(exc))
        return None
