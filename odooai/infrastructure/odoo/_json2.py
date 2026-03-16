"""
Module: infrastructure/odoo/_json2.py
Role: JSON-2 helpers for Odoo 19+ communication via HTTP Bearer token.
Dependencies: httpx, odooai.exceptions
"""

import asyncio
from typing import Any

import httpx
import structlog

from odooai.domain.value_objects.odoo_user_info import OdooUserInfo
from odooai.exceptions import OdooAuthError, OdooConnectionError
from odooai.infrastructure.odoo._errors import raise_from_json2_error
from odooai.infrastructure.odoo._http import MAX_RETRIES, get_http_pool

logger = structlog.get_logger(__name__)


async def json2_call(
    base_url: str,
    db: str,
    api_key: str,
    model: str,
    method: str,
    body: dict[str, Any],
) -> Any:
    """
    POST /json/2/<model>/<method> with Bearer auth and retry.

    Args:
        base_url: Odoo instance base URL.
        db: Odoo database name.
        api_key: Odoo API key (Bearer token).
        model: Odoo model technical name.
        method: Method to call.
        body: JSON body payload.

    Returns:
        Parsed JSON response.
    """
    url = f"{base_url}/json/2/{model}/{method}"
    headers = {
        "Authorization": f"bearer {api_key}",
        "Content-Type": "application/json; charset=utf-8",
        "X-Odoo-Database": db,
    }
    pool = get_http_pool()

    for attempt in range(MAX_RETRIES + 1):
        try:
            response = await pool.post(url, headers=headers, json=body)

            if response.status_code >= 400:
                try:
                    error_data = response.json()
                except Exception:
                    error_data = {}
                raise_from_json2_error(response.status_code, error_data)

            return response.json()

        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            if attempt < MAX_RETRIES:
                logger.warning(
                    "JSON-2 request failed, retrying",
                    attempt=attempt + 1,
                    model=model,
                    method=method,
                    error=str(exc),
                )
                await asyncio.sleep(0.5 * (attempt + 1))  # Backoff
                continue
            raise OdooConnectionError(
                f"Cannot reach Odoo at {base_url}: {exc}",
                user_message="Cannot connect to your Odoo instance. Please try again later.",
            ) from exc
        except (OdooAuthError, OdooConnectionError):
            raise
        except Exception as exc:
            raise OdooConnectionError(
                f"Unexpected error calling Odoo JSON-2: {exc}",
                user_message=f"Odoo error on {model}.{method}: {exc}",
            ) from exc

    raise OdooConnectionError("Max retries exceeded", user_message="Odoo is unreachable.")


async def json2_authenticate(
    base_url: str,
    db: str,
    login: str,
    api_key: str,
) -> OdooUserInfo:
    """
    Authenticate via JSON-2 (Odoo 19+).

    Flow: context_get → read user → has_group checks → reject portal.
    """
    # Step 1: Get user context (validates the API key)
    try:
        user_data = await json2_call(
            base_url,
            db,
            api_key,
            "res.users",
            "context_get",
            {},
        )
    except OdooAuthError:
        raise OdooAuthError(
            f"API key rejected by Odoo for login={login}",
            user_message="Invalid Odoo API key. Generate a new one in Odoo.",
        ) from None

    if not isinstance(user_data, dict) or not user_data.get("uid"):
        raise OdooAuthError(
            f"context_get returned no uid for login={login}",
            user_message="Invalid Odoo API key. Could not identify the user.",
        )

    uid = int(user_data["uid"])
    lang = str(user_data.get("lang", ""))
    tz = str(user_data.get("tz", ""))

    # Step 2: Read user name and login
    odoo_login = login
    odoo_name = login
    try:
        user_records = await json2_call(
            base_url,
            db,
            api_key,
            "res.users",
            "read",
            {"ids": [uid], "fields": ["login", "name"]},
        )
        if isinstance(user_records, list) and user_records:
            rec = user_records[0]
            odoo_login = str(rec.get("login", login))
            odoo_name = str(rec.get("name", login))
    except Exception as exc:
        logger.warning("Failed to read user record", uid=uid, error=str(exc))

    # Verify API key belongs to expected user
    if odoo_login.lower() != login.lower():
        raise OdooAuthError(
            f"API key belongs to {odoo_login}, not {login}",
            user_message=f"This API key belongs to {odoo_login}, not {login}.",
        )

    # Step 3: Group checks (parallel)
    is_system_task = _check_has_group(base_url, db, api_key, uid, "base.group_system")
    is_internal_task = _check_has_group(base_url, db, api_key, uid, "base.group_user")
    is_system, is_internal_group = await asyncio.gather(is_system_task, is_internal_task)
    is_internal = is_system or is_internal_group

    # Reject portal users
    if not is_internal:
        raise OdooAuthError(
            f"Portal user {login} (uid={uid}) rejected — internal access required",
            user_message="OdooAI requires an internal Odoo user. Portal users are not supported.",
        )

    return OdooUserInfo(
        uid=uid,
        login=odoo_login,
        name=odoo_name,
        is_system=is_system,
        is_internal=is_internal,
        lang=lang,
        tz=tz,
    )


async def json2_version(base_url: str, db: str) -> str:
    """Detect Odoo version via JSON endpoint. Returns '' on failure."""
    pool = get_http_pool()
    try:
        resp = await pool.post(
            f"{base_url}/web/webclient/version_info",
            json={"jsonrpc": "2.0", "method": "call", "params": {}},
            headers={"Content-Type": "application/json"},
            timeout=10.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            result = data.get("result", {})
            if isinstance(result, dict):
                return str(result.get("server_version", ""))
    except Exception as exc:
        logger.debug("JSON version_info failed", error=str(exc))
    return ""


async def _check_has_group(
    base_url: str,
    db: str,
    api_key: str,
    uid: int,
    group_ext_id: str,
) -> bool:
    """Check if the user belongs to an Odoo group via JSON-2."""
    try:
        result = await json2_call(
            base_url,
            db,
            api_key,
            "res.users",
            "has_group",
            {"ids": [uid], "group_ext_id": group_ext_id},
        )
        return bool(result)
    except Exception as exc:
        logger.warning("has_group check failed", group=group_ext_id, error=str(exc))
        return False
