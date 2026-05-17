from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def _assert_safe(payload: dict) -> None:
    assert payload["external_solver_executed"] is False
    assert payload["external_llm_required"] is False
    assert payload["proprietary_solver_required"] is False
    assert payload["production_grade_validation_claimed"] is False
    assert payload["formal_convergence_proof_claimed"] is False


def test_material_api_lists_details_and_suggests_preview_materials():
    client = TestClient(app)

    materials = client.get("/api/materials")
    assert materials.status_code == 200
    payload = materials.json()
    _assert_safe(payload)
    ids = {item["material_id"] for item in payload["materials"]}
    assert {"sio2", "si", "au", "ag"}.issubset(ids)
    assert "not a production-grade optical constants database" in payload["catalog_note"]

    detail = client.get("/api/materials/sio2")
    assert detail.status_code == 200
    detail_payload = detail.json()
    _assert_safe(detail_payload)
    assert detail_payload["material"]["material_id"] == "sio2"
    assert detail_payload["material"]["production_grade"] is False

    suggestion = client.post(
        "/api/materials/suggest",
        json={"application": "dielectric metasurface"},
    )
    assert suggestion.status_code == 200
    suggestion_payload = suggestion.json()
    _assert_safe(suggestion_payload)
    suggestion_ids = {item["material_id"] for item in suggestion_payload["suggested_materials"]}
    assert {"tio2", "si3n4", "sio2"}.issubset(suggestion_ids)
