"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_health(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.json()
    assert data["status"] == "ok"
    assert data["version"] == "0.3.0"


def test_parse(client):
    resp = client.post(
        "/parse",
        json={"text": "用FDTD仿真金纳米球散射，直径100nm，波长400-800nm"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "spec_json" in data
    assert "summary" in data
    assert "confirmed_fields" in data
    assert "inferred_fields" in data
    assert "missing_fields" in data
    assert "validation_status" in data


def test_validate_with_text(client):
    resp = client.post(
        "/validate",
        json={"text": "COMSOL模式分析脊波导"},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "is_executable" in data
    assert "errors" in data


def test_validate_empty_body(client):
    resp = client.post("/validate", json={})
    assert resp.status_code == 200
    data = resp.json()
    assert data["is_executable"] is False
    assert len(data["errors"]) > 0


def test_schema_endpoint(client):
    resp = client.get("/schema")
    assert resp.status_code == 200
    data = resp.json()
    assert "properties" in data
    assert "task" in data["properties"]
