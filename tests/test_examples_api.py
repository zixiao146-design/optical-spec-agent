from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def _assert_safe(payload: dict) -> None:
    assert payload["external_solver_executed"] is False
    assert payload["external_llm_required"] is False
    assert payload["production_grade_validation_claimed"] is False
    assert payload["formal_convergence_proof_claimed"] is False


def test_examples_api_lists_details_and_example_trace():
    client = TestClient(app)

    response = client.get("/api/examples")
    assert response.status_code == 200
    payload = response.json()
    _assert_safe(payload)
    ids = {example["example_id"] for example in payload["examples"]}
    assert "nanoparticle_plasmonics" in ids
    assert "lens_raytrace_preview" in ids

    response = client.get("/api/examples/nanoparticle_plasmonics")
    assert response.status_code == 200
    detail = response.json()
    _assert_safe(detail)
    assert detail["example"]["summary"]["suggested_adapter"] == "meep"
    assert detail["example"]["spec"]["application"] == "nanoparticle plasmonics"

    response = client.post("/api/examples/nanoparticle_plasmonics/agent-trace", json={})
    assert response.status_code == 200
    trace = response.json()
    _assert_safe(trace)
    assert trace["example_id"] == "nanoparticle_plasmonics"
    assert trace["timeline_summary"]
    assert trace["material_suggestions"]
    assert trace["adapter_recommendation"]
