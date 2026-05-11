"""API contract smoke tests for release readiness."""

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


client = TestClient(app)


def test_api_contract_health_and_schema():
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    schema = client.get("/schema")
    assert schema.status_code == 200
    assert "properties" in schema.json()


def test_api_contract_parse_backward_compatible():
    response = client.post("/parse", json={"text": "用 Meep FDTD 仿真金纳米球散射。"})
    assert response.status_code == 200
    data = response.json()
    assert "spec_json" in data
    assert data["spec_json"]["simulation"]["software_tool"]["value"] == "meep"


def test_api_contract_parse_hybrid_mock():
    response = client.post(
        "/parse",
        json={
            "text": "用 MPB 计算二维光子晶体 band diagram。",
            "parser": "hybrid",
            "llm_provider": "mock",
            "parser_report": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["spec_json"]["simulation"]["software_tool"]["value"] == "mpb"
    assert data["parser_report"]["provider"] == "mock"


def test_api_contract_unsupported_provider_clean_error():
    response = client.post(
        "/parse",
        json={"text": "Use MPB.", "parser": "llm", "llm_provider": "external-required"},
    )
    assert response.status_code == 400
    assert "Unsupported LLM provider" in response.json()["detail"]
