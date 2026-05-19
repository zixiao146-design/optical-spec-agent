"""Adapter golden coverage API tests."""

from __future__ import annotations

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def test_adapter_native_golden_coverage_api_returns_all_adapters_and_safety_flags():
    client = TestClient(app)
    response = client.get("/api/adapter-native-golden-coverage")
    assert response.status_code == 200
    body = response.json()
    assert body["api_contract_version"] == "0.1"
    assert body["status"] == "ok"
    assert set(body["adapters_covered"]) == {"meep", "mpb", "gmsh", "elmer", "optiland"}
    assert body["missing_adapters"] == []
    assert body["external_solver_executed"] is False
    assert body["external_llm_required"] is False
    assert body["proprietary_solver_required"] is False
    assert body["production_grade_validation_claimed"] is False
    assert body["formal_convergence_proof_claimed"] is False
    assert all(item["coverage_status"] == "pass" for item in body["coverage_items"])
