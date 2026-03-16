"""
Module: infrastructure/odoo/_errors.py
Role: Map Odoo API errors to domain exceptions.
      user_message NEVER contains technical details (model names, fault strings).
Dependencies: odooai.exceptions
"""

from typing import Any

from odooai.exceptions import (
    OdooAuthError,
    OdooConnectionError,
    OdooRecordNotFoundError,
    OdooValidationError,
)


def raise_from_json2_error(status_code: int, error: dict[str, Any]) -> None:
    """Map a JSON-2 HTTP error response to a domain exception."""
    message = str(error.get("message", f"HTTP {status_code}"))
    name = str(error.get("name", ""))

    if status_code in (401, 403) or "Unauthorized" in name or "Forbidden" in name:
        raise OdooAuthError(
            f"Odoo auth error ({status_code}): {message}",
            user_message="Your Odoo API key is invalid or has expired.",
        )
    if status_code == 404:
        raise OdooRecordNotFoundError(
            f"Odoo record not found: {message}",
            user_message="The requested record does not exist or is not accessible.",
        )
    if "ValidationError" in name or "UserError" in name:
        raise OdooValidationError(
            f"Odoo validation error: {message}",
            user_message="Odoo rejected the operation. Check your input and try again.",
        )
    raise OdooConnectionError(
        f"Odoo JSON-2 error {status_code}: {message}",
        user_message="Odoo returned an error. Please try again.",
    )


def raise_from_xmlrpc_fault(fault_string: str, model: str, method: str) -> None:
    """Map an XML-RPC fault string to a domain exception."""
    if "cannot marshal" in fault_string:
        return  # Action succeeded, return value not serializable

    if "AccessError" in fault_string or "Access Denied" in fault_string:
        raise OdooAuthError(
            f"XML-RPC access error on {model}.{method}: {fault_string}",
            user_message="Your Odoo API key is invalid or lacks the required access.",
        )
    if "MissingError" in fault_string or "does not exist" in fault_string.lower():
        raise OdooRecordNotFoundError(
            f"XML-RPC record not found: {fault_string}",
            user_message="The requested record does not exist or is not accessible.",
        )
    if "ValidationError" in fault_string or "UserError" in fault_string:
        raise OdooValidationError(
            f"XML-RPC validation error: {fault_string}",
            user_message="Odoo rejected the operation. Check your input and try again.",
        )
    raise OdooValidationError(
        f"XML-RPC fault on {model}.{method}: {fault_string}",
        user_message="An error occurred while communicating with Odoo.",
    )


def raise_from_rpc_error(error: dict[str, Any]) -> None:
    """Map a legacy JSON-RPC error dict to a domain exception."""
    message = str(error.get("message", "Unknown Odoo error"))
    data = error.get("data", {})
    exc_type = str(data.get("exception_type", ""))
    data_message = str(data.get("message", ""))

    combined = f"{message} {data_message} {exc_type}"
    if exc_type in ("access_error", "access_denied") or "Access Denied" in combined:
        raise OdooAuthError(
            f"Odoo access denied: {message} / {data_message}",
            user_message="Invalid Odoo credentials. Check your login and API key.",
        )
    if exc_type in ("validation_error", "user_error"):
        raise OdooValidationError(
            f"Odoo validation error: {message}",
            user_message="Odoo rejected the operation. Check your input and try again.",
        )
    raise OdooConnectionError(
        f"Odoo RPC error: {message} (type={exc_type})",
        user_message="An error occurred while communicating with Odoo.",
    )
