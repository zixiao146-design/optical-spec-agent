"""Agent session API tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_agent_session_api_returns_task_session():
    client = TestClient(app)
    response = client.post(
        "/api/agent-session",
        json={
            "goal": "Create a local preview workflow for a silver nanoparticle scattering case.",
            "example_id": "nanoparticle_plasmonics",
            "language": "en",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["api_contract_version"] == "0.1"
    assert payload["optical_intent_summary"]
    assert payload["selected_example_id"] == "nanoparticle_plasmonics"
    assert payload["plan_steps"]
    assert payload["artifacts"]
    assert payload["permission_gates"]
    assert payload["tool_call_ledger"]
    assert payload["agent_trace"]["agents"]
    assert payload["external_solver_executed"] is False
    assert payload["external_llm_required"] is False
    assert payload["production_grade_validation_claimed"] is False
    assert payload["formal_convergence_proof_claimed"] is False
    ledger = {entry["tool_name"]: entry for entry in payload["tool_call_ledger"]}
    assert ledger["material_catalog.suggest"]["executed"] is True
    assert ledger["external_solver.meep"]["executed"] is False
    assert ledger["external_llm"]["executed"] is False


def test_agent_session_api_blocks_empty_goal_and_unknown_example():
    client = TestClient(app)

    empty_goal = client.post("/api/agent-session", json={"goal": "   "})
    assert empty_goal.status_code == 400
    assert empty_goal.json()["status"] == "error"
    assert empty_goal.json()["error_code"] == "invalid_workflow_request"

    unknown_example = client.post(
        "/api/agent-session",
        json={"goal": "Plan a local preview.", "example_id": "missing_example"},
    )
    assert unknown_example.status_code == 404
    assert unknown_example.json()["status"] == "error"
    assert unknown_example.json()["external_solver_executed"] is False
    assert unknown_example.json()["external_llm_required"] is False
