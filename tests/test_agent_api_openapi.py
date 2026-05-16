"""OpenAPI contract tests for the local Agent API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_agent_api_openapi_includes_agent_endpoints():
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    for path in [
        "/api/health",
        "/api/version",
        "/api/adapters",
        "/api/schema",
        "/api/parse",
        "/api/validate",
        "/api/workflow-plan",
        "/api/adapter-preview",
        "/api/validation-evidence",
        "/api/readiness",
    ]:
        assert path in paths
