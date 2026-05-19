"""Local Agent API contract tests."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


ROOT = Path(__file__).resolve().parents[1]
CLIENT = TestClient(app)


def _assert_safety(payload: dict) -> None:
    assert payload["external_solver_executed"] is False
    assert payload["external_llm_required"] is False
    assert payload["proprietary_solver_required"] is False
    assert payload["production_grade_validation_claimed"] is False
    assert payload["formal_convergence_proof_claimed"] is False


def _assert_status_and_diagnostics(payload: dict) -> None:
    assert payload["api_contract_version"] == "0.1"
    assert "status" in payload
    assert "diagnostics" in payload
    assert "recommended_next_actions" in payload


def test_agent_api_health_and_version_are_local_first():
    health = CLIENT.get("/api/health")
    assert health.status_code == 200
    health_payload = health.json()
    assert health_payload["status"] == "ok"
    assert health_payload["service"] == "optical-spec-agent"
    _assert_status_and_diagnostics(health_payload)
    _assert_safety(health_payload)

    version = CLIENT.get("/api/version")
    assert version.status_code == 200
    version_payload = version.json()
    assert version_payload["package_version"] == "0.9.0rc8.dev0"
    assert version_payload["current_public_prerelease"] == "v0.9.0rc7"
    assert version_payload["main_development_version"] == "0.9.0rc8.dev0"
    assert version_payload["pypi_published"] is False
    assert version_payload["testpypi_verified"] is True
    _assert_status_and_diagnostics(version_payload)
    _assert_safety(version_payload)


def test_agent_api_adapters_include_expected_registry_and_claim_bounds():
    response = CLIENT.get("/api/adapters")
    assert response.status_code == 200
    payload = response.json()
    _assert_status_and_diagnostics(payload)
    _assert_safety(payload)
    by_tool = {item["tool_name"]: item for item in payload["adapters"]}
    for tool in ("meep", "gmsh", "mpb", "elmer", "optiland"):
        assert tool in by_tool
        assert by_tool[tool]["external_solver_required_by_default"] is False
        assert by_tool[tool]["production_grade_validation_claimed"] is False
    assert by_tool["elmer"]["maturity_level"] == "Level 2 + Level-3-ready"


def test_agent_api_schema_returns_schema_like_response():
    response = CLIENT.get("/api/schema")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["schema_name"] == "OpticalSpec"
    assert "properties" in payload["schema"]
    assert "task" in payload["schema"]["properties"]
    _assert_status_and_diagnostics(payload)
    _assert_safety(payload)


def test_agent_api_parse_defaults_to_local_no_llm():
    response = CLIENT.post(
        "/api/parse",
        json={
            "text": "Use Meep FDTD to simulate a gold nanoparticle scattering spectrum.",
            "parser": "heuristic",
            "json": True,
        },
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["parser"] == "rule"
    assert "spec" in payload
    assert "diagnostics" in payload
    assert "recommended_next_actions" in payload
    assert payload["external_llm_required"] is False
    _assert_status_and_diagnostics(payload)
    _assert_safety(payload)


def test_agent_api_validate_accepts_inline_spec_and_local_path():
    spec = json.loads((ROOT / "examples/specs/minimal_nanoparticle.json").read_text())

    inline = CLIENT.post("/api/validate", json={"spec": spec})
    assert inline.status_code == 200
    inline_payload = inline.json()
    assert inline_payload["valid"] is True
    _assert_status_and_diagnostics(inline_payload)
    _assert_safety(inline_payload)

    by_path = CLIENT.post(
        "/api/validate",
        json={"path": "examples/specs/minimal_nanoparticle.json"},
    )
    assert by_path.status_code == 200
    by_path_payload = by_path.json()
    assert by_path_payload["valid"] is True
    _assert_status_and_diagnostics(by_path_payload)
    _assert_safety(by_path_payload)


def test_agent_api_workflow_plan_and_adapter_preview_do_not_execute_solver():
    plan = CLIENT.post(
        "/api/workflow-plan",
        json={"path": "examples/workflows/local_preview_request.json"},
    )
    assert plan.status_code == 200
    plan_payload = plan.json()
    assert plan_payload["status"] == "ok"
    assert plan_payload["workflow_plan"]["execute_policy"] == "no_execute_by_default"
    assert plan_payload["external_solver_executed"] is False
    _assert_status_and_diagnostics(plan_payload)
    _assert_safety(plan_payload)

    preview = CLIENT.post(
        "/api/adapter-preview",
        json={"path": "examples/specs/minimal_nanoparticle.json", "tool": "gmsh"},
    )
    assert preview.status_code == 200
    preview_payload = preview.json()
    assert preview_payload["tool"] == "gmsh"
    assert preview_payload["output_extension"] == ".geo"
    assert preview_payload["preview_content"]
    _assert_status_and_diagnostics(preview_payload)
    _assert_safety(preview_payload)


def test_agent_api_validation_evidence_and_readiness_bound_claims():
    evidence = CLIENT.get("/api/validation-evidence")
    assert evidence.status_code == 200
    evidence_payload = evidence.json()
    _assert_status_and_diagnostics(evidence_payload)
    _assert_safety(evidence_payload)
    by_tool = {item["tool_name"]: item for item in evidence_payload["validation_evidence"]}
    for tool in ("gmsh", "meep", "mpb", "optiland"):
        assert by_tool[tool]["maturity_level"] == "Level 3"
    assert by_tool["elmer"]["maturity_level"] == "Level 2 + Level-3-ready"
    assert "deferred" in by_tool["elmer"]["status_note"].lower()

    readiness = CLIENT.get("/api/readiness")
    assert readiness.status_code == 200
    readiness_payload = readiness.json()
    assert readiness_payload["current_public_prerelease"] == "v0.9.0rc7"
    assert readiness_payload["main_development_version"] == "0.9.0rc8.dev0"
    assert readiness_payload["testpypi"]["uploaded_and_verified"] is True
    assert readiness_payload["pypi"]["published"] is False
    assert readiness_payload["public_contract_freeze"]["status"] == "approved"
    assert readiness_payload["adapter_maturity"]["elmer"] == "Level 2 + Level-3-ready"
    assert readiness_payload["v1_0_0_released"] is False
    _assert_status_and_diagnostics(readiness_payload)
    _assert_safety(readiness_payload)


def test_agent_api_adapter_preview_invalid_adapter_returns_stable_error():
    response = CLIENT.post(
        "/api/adapter-preview",
        json={"path": "examples/specs/minimal_nanoparticle.json", "tool": "not-a-tool"},
    )
    assert response.status_code == 400
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["error_code"] == "unsupported_adapter"
    assert "message" in payload
    _assert_status_and_diagnostics(payload)
    _assert_safety(payload)


def test_agent_api_validate_invalid_spec_returns_diagnostic_response():
    response = CLIENT.post("/api/validate", json={"spec": {"bad": "shape"}})
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] in {"ok", "needs_review"}
    assert "valid" in payload
    _assert_status_and_diagnostics(payload)
    _assert_safety(payload)


def test_agent_api_parse_rejects_external_llm_modes_by_default():
    response = CLIENT.post(
        "/api/parse",
        json={"text": "Use MPB for a band diagram.", "parser": "llm"},
    )
    assert response.status_code == 400
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["error_code"] == "external_llm_not_enabled"
    _assert_status_and_diagnostics(payload)
    _assert_safety(payload)
