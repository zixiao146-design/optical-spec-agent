"""API tests for v0.8 parser selection."""

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


client = TestClient(app)


def test_old_parse_request_still_works():
    resp = client.post("/parse", json={"text": "用 Meep FDTD 仿真金纳米球散射。"})
    assert resp.status_code == 200
    assert resp.json()["spec_json"]["simulation"]["software_tool"]["value"] == "meep"


def test_parse_llm_mock_works():
    resp = client.post(
        "/parse",
        json={
            "text": "Use MPB to compute a photonic crystal band diagram.",
            "parser": "llm",
            "llm_provider": "mock",
            "parser_report": True,
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["spec_json"]["simulation"]["software_tool"]["value"] == "mpb"
    assert data["parser_report"]["provider"] == "mock"


def test_parse_hybrid_mock_works():
    resp = client.post(
        "/parse",
        json={"text": "Use Gmsh to mesh a waveguide.", "parser": "hybrid", "llm_provider": "mock"},
    )
    assert resp.status_code == 200
    assert resp.json()["spec_json"]["simulation"]["software_tool"]["value"] == "gmsh"


def test_parse_unsupported_provider_errors():
    resp = client.post(
        "/parse",
        json={"text": "Use MPB.", "parser": "llm", "llm_provider": "real-provider"},
    )
    assert resp.status_code == 400
    assert "Unsupported LLM provider" in resp.json()["detail"]
