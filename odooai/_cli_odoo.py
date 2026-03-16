"""
Module: _cli_odoo.py
Role: Odoo connection helper for CLI chat command.
Dependencies: infrastructure/odoo, domain entities
"""

from __future__ import annotations

import asyncio
import getpass
import sys
from typing import Any


def connect_odoo(url: str, db: str) -> tuple[Any, int, str]:
    """
    Authenticate to an Odoo instance interactively.

    Returns (client, uid, api_key) or (None, 0, "") on failure.
    """
    from odooai.domain.entities.connection import OdooApiType
    from odooai.infrastructure.odoo.client import OdooClient

    login = input("Login Odoo : ").strip()
    odoo_key = getpass.getpass("API Key Odoo : ")

    # Auto-detect protocol: try version endpoint, use XML-RPC for Odoo <19
    print("Detection de la version...")
    tmp_client = OdooClient(base_url=url, db=db, api_type=OdooApiType.JSON2)
    version = asyncio.run(tmp_client.get_server_version())

    if version and int(version.split(".")[0]) >= 19:
        api_type = OdooApiType.JSON2
        print(f"Odoo {version} detecte → JSON-2")
    else:
        api_type = OdooApiType.XML_RPC
        v_display = version or "inconnue"
        print(f"Odoo {v_display} detecte → XML-RPC")

    client = OdooClient(base_url=url, db=db, api_type=api_type)
    print("Authentification...")

    try:
        user_info = asyncio.run(client.authenticate(login, odoo_key))
        admin = "admin" if user_info.is_system else "interne"
        print(f"Connecte : {user_info.name} (uid={user_info.uid}, {admin})")

        # Detect installed modules
        try:
            modules = asyncio.run(
                client.search_read(
                    odoo_key,
                    "ir.module.module",
                    [("state", "=", "installed")],
                    ["name"],
                    limit=200,
                    uid=user_info.uid,
                )
            )
            print(f"Modules installes : {len(modules)}")
        except Exception:
            print("(Detection modules non disponible)")

        return client, user_info.uid, odoo_key
    except Exception as exc:
        # Use user_message if available, otherwise generic message
        msg = getattr(
            exc, "user_message", "Connexion impossible. Verifiez l'URL et vos credentials."
        )
        print(f"Erreur : {msg}", file=sys.stderr)
        print("Le chat continue en mode BA Profiles.\n")
        return None, 0, ""
