"""Frontend handoff spec documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_handoff_spec_maps_screens_to_endpoints_and_limits_scope():
    path = ROOT / "docs" / "frontend_handoff_spec.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Frontend Handoff Spec" in text
    assert "API contract version: 0.1" in text
    assert "Package version: 0.9.0rc8.dev0" in text
    assert "docs/frontend_mvp_product_spec.md" in text
    assert "docs/frontend_information_architecture.md" in text
    assert "docs/frontend_api_mapping.md" in text
    assert "docs/frontend_mvp_user_flows.md" in text
    assert "docs/frontend_mvp_acceptance_criteria.md" in text
    assert "docs/frontend_safety_policy.md" in text
    assert "docs/frontend_mvp_implementation_plan.md" in text
    assert "docs/frontend_mvp_runbook.md" in text
    assert "loading, empty, error, and API disconnected states" in text
    assert "not live validation" in text
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
    for mapping in [
        "Spec input screen -> `POST /api/parse` and `POST /api/validate`",
        "Adapter matrix -> `GET /api/adapters` and `GET /api/validation-evidence`",
        "Workflow plan -> `POST /api/workflow-plan`",
        "Artifact preview -> `POST /api/adapter-preview`",
        "Readiness/status -> `GET /api/readiness`",
        "Evidence view -> `GET /api/validation-evidence`",
    ]:
        assert mapping in text
    assert "React + Vite + TypeScript frontend app exists under `frontend/`" in text
    assert "VITE_API_BASE_URL" in text
    assert "Dashboard, Spec Input, Adapter Matrix, Workflow Plan" in text
    assert "LoadingState" in text
    assert "ApiDisconnectedNotice" in text
    assert "No session history" in text
    assert "No login" in text
    assert "No cloud backend" in text
    assert "No default solver execution" in text
    assert "No default external LLM" in text
    assert "No PyPI/TestPyPI upload controls" in text
    assert "No tag/release controls" in text
