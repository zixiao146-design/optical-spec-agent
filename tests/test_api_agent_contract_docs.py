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
    assert "Frontend implementation: not started" in text
    assert "No external solver execution by default" in text
    assert "No external LLM call by default" in text
    assert "No proprietary solver dependency" in text
    assert "No network dependency for documented local examples" in text
    assert "No production-grade physical validation claim" in text
    assert "No formal convergence proof claim" in text
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
