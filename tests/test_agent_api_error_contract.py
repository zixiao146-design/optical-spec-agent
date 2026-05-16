"""Stable error contract tests for the Local Agent API."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


CLIENT = TestClient(app)


def _assert_error(payload: dict, error_code: str) -> None:
    assert payload["api_contract_version"] == "0.1"
    assert payload["status"] == "error"
    assert payload["error_code"] == error_code
    assert payload["message"]
    assert isinstance(payload["diagnostics"], dict)
    assert isinstance(payload["recommended_next_actions"], list)
    assert payload["external_solver_executed"] is False
    assert payload["external_llm_required"] is False
    assert payload["proprietary_solver_required"] is False
    assert payload["production_grade_validation_claimed"] is False
    assert payload["formal_convergence_proof_claimed"] is False


def test_adapter_preview_unknown_tool_returns_stable_error():
    response = CLIENT.post(
        "/api/adapter-preview",
        json={"path": "examples/specs/minimal_nanoparticle.json", "tool": "unknown"},
    )
    assert response.status_code == 400
    _assert_error(response.json(), "unsupported_adapter")


def test_validate_invalid_payload_returns_stable_error():
    response = CLIENT.post("/api/validate", json={})
    assert response.status_code == 400
    _assert_error(response.json(), "invalid_spec")


def test_workflow_plan_invalid_request_returns_stable_error():
    response = CLIENT.post("/api/workflow-plan", json={})
    assert response.status_code == 400
    _assert_error(response.json(), "invalid_workflow_request")


def test_parse_external_llm_request_is_rejected_without_llm_call():
    response = CLIENT.post(
        "/api/parse",
        json={"text": "Use MPB for a band diagram.", "parser": "llm"},
    )
    assert response.status_code == 400
    _assert_error(response.json(), "external_llm_not_enabled")
