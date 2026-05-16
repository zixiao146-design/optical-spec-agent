"""Documentation tests for the local Agent API contract."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_api_agent_contract_doc_exists_and_bounds_defaults():
    path = ROOT / "docs" / "api_agent_contract.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Local Agent API Contract" in text
    assert "Current public prerelease: v0.9.0rc6" in text
    assert "Current main development version: 0.9.0rc7.dev0" in text
    assert "API readiness: in progress" in text
    assert "API response models" in text
    assert "examples/api/" in text
    assert "Frontend implementation: not started" in text
    assert "No external solver execution by default" in text
    assert "No external LLM call by default" in text
    assert "No proprietary solver dependency" in text
    assert "No network dependency for documented local examples" in text
    assert "No production-grade physical validation claim" in text
    assert "No formal convergence proof claim" in text
    assert "docs/api_error_model.md" in text
    assert "status: error" in text
    for endpoint in [
        "GET /api/health",
        "GET /api/version",
        "GET /api/adapters",
        "GET /api/schema",
        "POST /api/parse",
        "POST /api/validate",
        "POST /api/workflow-plan",
        "POST /api/adapter-preview",
        "GET /api/validation-evidence",
        "GET /api/readiness",
    ]:
        assert endpoint in text
    assert "Frontend Agent Studio should call this API" in text


def test_api_error_model_doc_exists_and_defines_stable_shape():
    path = ROOT / "docs" / "api_error_model.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Local Agent API Error Model" in text
    assert "status: error" in text
    assert "error_code" in text
    assert "recommended_next_actions" in text
    assert "external_solver_executed: false" in text
    assert "external_llm_required: false" in text
    assert "production_grade_validation_claimed: false" in text
    assert "formal_convergence_proof_claimed: false" in text
    for error_code in [
        "invalid_json",
        "invalid_spec",
        "unsupported_adapter",
        "invalid_workflow_request",
        "preview_generation_error",
        "solver_execution_not_enabled",
        "external_llm_not_enabled",
    ]:
        assert error_code in text
