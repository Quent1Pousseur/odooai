"""
Module: infrastructure/odoo/_xmlrpc.py
Role: XML-RPC helpers for Odoo 17/18 communication.
      All synchronous xmlrpc.client calls are wrapped in asyncio.to_thread().
Dependencies: xmlrpc.client, asyncio, odooai.exceptions
"""

import asyncio
import xmlrpc.client  # nosec B411 — connecting to trusted Odoo instances only
from typing import Any

import structlog

from odooai.domain.value_objects.odoo_user_info import OdooUserInfo
from odooai.exceptions import OdooAuthError, OdooConnectionError
from odooai.infrastructure.odoo._errors import raise_from_xmlrpc_fault

logger = structlog.get_logger(__name__)


def _sync_authenticate(base_url: str, db: str, login: str, api_key: str) -> int | bool:
    """Synchronous XML-RPC authenticate. Returns uid or False."""
    common = xmlrpc.client.ServerProxy(
        f"{base_url}/xmlrpc/2/common",
        allow_none=True,
    )
    try:
        result = common.authenticate(db, login, api_key, {})
        if isinstance(result, int):
            return result
        return False
    except xmlrpc.client.Fault as exc:
        if "Access Denied" in str(exc.faultString):
            raise OdooAuthError(
                f"XML-RPC access denied: {exc.faultString}",
                user_message="Invalid Odoo credentials. Check your login and API key.",
            ) from exc
        raise OdooConnectionError(
            f"XML-RPC fault during authenticate: {exc.faultString}",
            user_message="An error occurred while contacting Odoo.",
        ) from exc


def _sync_execute_kw(
    base_url: str,
    db: str,
    uid: int,
    api_key: str,
    model: str,
    method: str,
    args: list[Any],
    kwargs: dict[str, Any],
) -> Any:
    """Synchronous XML-RPC execute_kw. Meant for asyncio.to_thread()."""
    models = xmlrpc.client.ServerProxy(
        f"{base_url}/xmlrpc/2/object",
        allow_none=True,
    )
    try:
        return models.execute_kw(db, uid, api_key, model, method, args, kwargs)
    except xmlrpc.client.Fault as exc:
        fault = str(exc.faultString)
        if "cannot marshal" in fault:
            logger.info(
                "XML-RPC result not serializable — action succeeded",
                model=model,
                method=method,
            )
            return True
        raise_from_xmlrpc_fault(fault, model, method)
        return True  # raise_from_xmlrpc_fault raises unless "cannot marshal"


def _sync_version(base_url: str) -> str:
    """Synchronous XML-RPC version detection. Returns version string or ''."""
    common = xmlrpc.client.ServerProxy(
        f"{base_url}/xmlrpc/2/common",
        allow_none=True,
    )
    info = common.version()
    if isinstance(info, dict):
        return str(info.get("server_version", ""))
    return ""


async def xmlrpc_authenticate(
    base_url: str,
    db: str,
    login: str,
    api_key: str,
) -> OdooUserInfo:
    """
    Authenticate via XML-RPC (Odoo 17/18).

    Flow: common.authenticate → users.read → has_group checks.
    Rejects portal users (not is_internal).
    """
    try:
        uid = await asyncio.to_thread(_sync_authenticate, base_url, db, login, api_key)
    except (OdooAuthError, OdooConnectionError):
        raise
    except Exception as exc:
        raise OdooConnectionError(
            f"XML-RPC authenticate failed: {exc}",
            user_message="Cannot connect to your Odoo instance.",
        ) from exc

    if not uid:
        raise OdooAuthError(
            f"XML-RPC authentication failed for {login}",
            user_message="Invalid Odoo credentials. Check your login and API key.",
        )

    uid_int = int(uid)

    # Read user fields
    user_data = await xmlrpc_execute_kw(
        base_url,
        db,
        uid_int,
        api_key,
        "res.users",
        "read",
        [[uid_int]],
        {"fields": ["name", "login", "lang", "tz", "share", "groups_id"]},
    )
    if not user_data or not isinstance(user_data, list):
        raise OdooAuthError(
            f"Could not read res.users for uid {uid_int}",
            user_message="Could not retrieve user information from Odoo.",
        )
    user = user_data[0]

    # Group checks (parallel)
    is_system = await _check_has_group(base_url, db, uid_int, api_key, "base.group_system")
    is_internal = is_system or not bool(user.get("share", True))

    # Reject portal users
    if not is_internal:
        raise OdooAuthError(
            f"Portal user {login} (uid={uid_int}) rejected — internal access required",
            user_message="OdooAI requires an internal Odoo user. Portal users are not supported.",
        )

    return OdooUserInfo(
        uid=uid_int,
        login=str(user.get("login", login)),
        name=str(user.get("name", login)),
        is_system=is_system,
        is_internal=is_internal,
        lang=str(user.get("lang", "")),
        tz=str(user.get("tz", "")),
    )


async def xmlrpc_execute_kw(
    base_url: str,
    db: str,
    uid: int,
    api_key: str,
    model: str,
    method: str,
    args: list[Any],
    kwargs: dict[str, Any],
) -> Any:
    """Execute an XML-RPC call wrapped in asyncio.to_thread()."""
    try:
        return await asyncio.to_thread(
            _sync_execute_kw,
            base_url,
            db,
            uid,
            api_key,
            model,
            method,
            args,
            kwargs,
        )
    except (OdooAuthError, OdooConnectionError):
        raise
    except Exception as exc:
        raise OdooConnectionError(
            f"XML-RPC execute_kw failed for {model}.{method}: {exc}",
            user_message=f"Odoo error on {model}.{method}: {exc}",
        ) from exc


async def xmlrpc_version(base_url: str) -> str:
    """Detect Odoo version via XML-RPC. Returns '' on failure."""
    try:
        return await asyncio.to_thread(_sync_version, base_url)
    except Exception as exc:
        logger.warning("XML-RPC version detection failed", error=str(exc))
        return ""


async def _check_has_group(
    base_url: str,
    db: str,
    uid: int,
    api_key: str,
    group_ext_id: str,
) -> bool:
    """Check if user belongs to an Odoo group via XML-RPC."""
    try:
        result = await xmlrpc_execute_kw(
            base_url,
            db,
            uid,
            api_key,
            "res.users",
            "has_group",
            [group_ext_id],
            {},
        )
        return bool(result)
    except (OdooAuthError, OdooConnectionError):
        raise
    except Exception as exc:
        logger.warning(
            "has_group check failed — denying access", group=group_ext_id, error=str(exc)
        )
        return False
