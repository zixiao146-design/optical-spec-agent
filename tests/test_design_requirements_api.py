"""Design requirement API tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_design_requirements_api_list_detail_and_match():
    client = TestClient(app)

    listing = client.get("/api/design-requirements")
    assert listing.status_code == 200
    payload = listing.json()
    assert payload["api_contract_version"] == "0.1"
    assert payload["template_count"] == 7
    assert payload["external_solver_executed"] is False
    assert payload["external_llm_required"] is False

    detail = client.get("/api/design-requirements/thin_film_ar_coating")
    assert detail.status_code == 200
    assert detail.json()["template"]["template_id"] == "thin_film_ar_coating"

    match = client.post(
        "/api/design-requirements/match",
        json={
            "goal": "Design an anti-reflection coating for glass at 550 nm.",
            "language": "en",
        },
    )
    assert match.status_code == 200
    match_payload = match.json()
    assert match_payload["matched_template_id"] == "thin_film_ar_coating"
    assert match_payload["external_solver_executed"] is False
    assert match_payload["external_llm_required"] is False


def test_design_requirements_api_rejects_empty_goal_and_unknown_template():
    client = TestClient(app)
    empty = client.post("/api/design-requirements/match", json={"goal": "   "})
    assert empty.status_code == 400
    assert empty.json()["status"] == "error"

    unknown = client.get("/api/design-requirements/missing_template")
    assert unknown.status_code == 404
    assert unknown.json()["external_solver_executed"] is False

