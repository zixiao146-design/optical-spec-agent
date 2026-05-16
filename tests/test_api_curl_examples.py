"""Curl example documentation checks for the local Agent API."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_api_curl_examples_cover_frontend_handoff_endpoints():
    path = ROOT / "docs" / "api_curl_examples.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Local Agent API Curl Examples" in text
    assert "curl http://127.0.0.1:8000/api/health" in text
    assert "curl http://127.0.0.1:8000/api/version" in text
    assert "curl http://127.0.0.1:8000/api/adapters" in text
    assert "curl http://127.0.0.1:8000/api/schema" in text
    assert "http://127.0.0.1:8000/api/parse" in text
    assert "http://127.0.0.1:8000/api/validate" in text
    assert "http://127.0.0.1:8000/api/workflow-plan" in text
    assert "http://127.0.0.1:8000/api/adapter-preview" in text
    assert "curl http://127.0.0.1:8000/api/validation-evidence" in text
    assert "curl http://127.0.0.1:8000/api/readiness" in text
    assert "@examples/api/parse_request_heuristic.json" in text
    assert "@examples/api/validate_request_minimal.json" in text
    assert "@examples/api/workflow_plan_request.json" in text
    assert "@examples/api/adapter_preview_gmsh_request.json" in text
    assert "do not execute solvers" in text
    assert "do not call an external LLM" in text
    assert "do not require external network access beyond the local API server" in text
