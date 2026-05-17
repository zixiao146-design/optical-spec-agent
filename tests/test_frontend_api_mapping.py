"""Agent Studio frontend API mapping checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_api_mapping_covers_endpoints_fixtures_and_safety_notes():
    path = ROOT / "docs" / "frontend_api_mapping.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for endpoint in [
        "/api/readiness",
        "/api/agent-session",
        "/api/parse",
        "/api/validate",
        "/api/adapters",
        "/api/validation-evidence",
        "/api/workflow-plan",
        "/api/adapter-preview",
        "/api/health",
        "/api/version",
    ]:
        assert endpoint in text
    for fixture in [
        "examples/api/readiness_response.json",
        "examples/api/agent_session_request_nanoparticle.json",
        "examples/api/agent_session_response_nanoparticle.json",
        "examples/api/parse_request_heuristic.json",
        "examples/api/parse_response_heuristic.json",
        "examples/api/validate_request_minimal.json",
        "examples/api/validate_response_minimal.json",
        "examples/api/adapters_response.json",
        "examples/api/workflow_plan_request.json",
        "examples/api/workflow_plan_response.json",
        "examples/api/adapter_preview_gmsh_request.json",
        "examples/api/adapter_preview_gmsh_response.json",
        "examples/api/health_response.json",
        "examples/api/version_response.json",
    ]:
        assert fixture in text
    assert "Safety notes" in text
    assert "no solver execution" in text.lower()
    assert "no external LLM" in text
