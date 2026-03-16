"""Integration tests for API endpoints — tests the real pipeline (mock LLM)."""

from __future__ import annotations

from collections.abc import Generator

import uuid

import pytest
from fastapi.testclient import TestClient

from odooai.main import create_app


@pytest.fixture()
def client() -> Generator[TestClient, None, None]:
    """Create a test client with lifespan (init_db)."""
    app = create_app()
    with TestClient(app) as c:
        yield c


class TestHealthEndpoint:
    """Test /health endpoint."""

    def test_health_returns_ok(self, client: TestClient) -> None:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestMetricsEndpoint:
    """Test /metrics endpoint."""

    def test_metrics_returns_json(self, client: TestClient) -> None:
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "chat_requests_total" in data
        assert "tokens_total" in data


class TestAuthEndpoints:
    """Test /api/auth/* endpoints."""

    def test_signup_success(self, client: TestClient) -> None:
        response = client.post(
            "/api/auth/signup",
            json={"email": f"integ-{uuid.uuid4().hex[:8]}@test.com", "password": "password123"},
        )
        assert response.status_code == 200
        data = response.json()
        assert "token" in data
        assert "user_id" in data

    def test_signup_short_password(self, client: TestClient) -> None:
        response = client.post(
            "/api/auth/signup",
            json={"email": f"short-{uuid.uuid4().hex[:8]}@test.com", "password": "123"},
        )
        assert response.status_code == 400

    def test_login_success(self, client: TestClient) -> None:
        email = f"login-{uuid.uuid4().hex[:8]}@test.com"
        client.post(
            "/api/auth/signup",
            json={"email": email, "password": "password123"},
        )
        response = client.post(
            "/api/auth/login",
            json={"email": email, "password": "password123"},
        )
        assert response.status_code == 200
        assert "token" in response.json()

    def test_login_wrong_password(self, client: TestClient) -> None:
        email = f"wrong-{uuid.uuid4().hex[:8]}@test.com"
        client.post(
            "/api/auth/signup",
            json={"email": email, "password": "password123"},
        )
        response = client.post(
            "/api/auth/login",
            json={"email": email, "password": "wrongpassword"},
        )
        assert response.status_code == 401

    def test_login_nonexistent_user(self, client: TestClient) -> None:
        response = client.post(
            "/api/auth/login",
            json={"email": f"noone-{uuid.uuid4().hex[:8]}@test.com", "password": "password123"},
        )
        assert response.status_code == 401


class TestWaitlistEndpoint:
    """Test /api/waitlist endpoint."""

    def test_waitlist_signup(self, client: TestClient) -> None:
        unique_email = f"waitlist-{uuid.uuid4().hex[:8]}@test.com"
        response = client.post(
            "/api/waitlist",
            json={"email": unique_email},
        )
        assert response.status_code == 200
        assert response.json()["status"] == "ok"


class TestChatEndpoint:
    """Test /api/chat endpoint (no LLM — will error without API key)."""

    def test_chat_returns_stream(self, client: TestClient) -> None:
        """Chat should return 200 SSE stream even without API key."""
        response = client.post(
            "/api/chat",
            json={"message": "test question"},
        )
        assert response.status_code == 200
