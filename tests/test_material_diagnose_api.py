"""Material diagnostic API tests."""

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_material_diagnose_api_returns_safe_preview_diagnostic():
    client = TestClient(app)
    response = client.post(
        "/api/materials/diagnose",
        json={"material_id": "ag", "application": "nanoparticle plasmonics"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["api_contract_version"] == "0.1"
    assert payload["external_solver_executed"] is False
    assert payload["external_llm_required"] is False
    assert payload["production_grade_validation_claimed"] is False
    assert payload["formal_convergence_proof_claimed"] is False
    assert payload["diagnostic"]["suitability"] == "suitable"
    assert payload["diagnostic"]["production_grade_optical_constants"] is False
    assert payload["diagnostic"]["requires_user_verification"] is True
