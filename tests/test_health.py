"""Smoke test: verify the app starts and health endpoint works."""

from fastapi.testclient import TestClient

from odooai.main import app


def test_health_returns_ok() -> None:
    """Health endpoint should return status ok."""
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
