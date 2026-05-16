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
    assert "`api_contract_version`: 0.1" in text
    assert "frontend-readiness / candidate API" in text
    assert "API response models" in text
    assert "examples/api/" in text
    assert "docs/api_versioning_policy.md" in text
    assert "docs/api_request_validation_contract.md" in text
    assert "docs/api_migration_notes.md" in text
    assert "docs/api_local_launch_guide.md" in text
    assert "docs/frontend_handoff_spec.md" in text
    assert "docs/api_curl_examples.md" in text
    assert "scripts/check_api_fixtures.py" in text
    assert "scripts/smoke_agent_api.sh" in text
    assert "docs/frontend_mvp_qa_checklist.md" in text
    assert "scripts/smoke_frontend_mvp.sh" in text
    assert "Demo fixture mode is explicitly not live validation" in text
    assert "not yet a separately frozen v1.0 API contract" in text
    assert "Frontend MVP implementation: available under `frontend/`" in text
    assert "docs/frontend_mvp_runbook.md" in text
    assert "does not include solver execution, external LLM" in text
    assert "upload, publish, tag, release, login, cloud" in text
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
    assert "Frontend Agent Studio calls this API" in text


def test_api_error_model_doc_exists_and_defines_stable_shape():
    path = ROOT / "docs" / "api_error_model.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Local Agent API Error Model" in text
    assert 'api_contract_version: "0.1"' in text
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
    assert "docs/api_request_validation_contract.md" in text
    assert "docs/api_versioning_policy.md" in text
    assert "docs/api_migration_notes.md" in text
    assert "examples/api/frontend_fixture_manifest.json" in text
    assert "scripts/check_api_fixtures.py" in text
