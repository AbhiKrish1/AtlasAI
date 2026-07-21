"""
AtlasAI

Module:
    test_health.py

Responsibility:
    Integration tests for the health endpoint.

Last Updated:
    Sprint 4
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from backend.api.app import app


client = TestClient(app)


def test_health_endpoint() -> None:
    """
    Verify that the health endpoint is reachable.
    """

    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == "AtlasAI Backend"