"""
Module: main.py
Role: FastAPI application entrypoint.
Dependencies: fastapi
"""

from fastapi import FastAPI

app = FastAPI(
    title="OdooAI",
    description="AI Business Analyst that has read every line of Odoo source code.",
    version="0.1.0",
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
