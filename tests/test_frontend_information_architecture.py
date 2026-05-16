"""Agent Studio frontend information architecture checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_information_architecture_maps_pages_to_api():
    path = ROOT / "docs" / "frontend_information_architecture.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for section in [
        "Dashboard / Readiness",
        "Spec Input",
        "Adapter Matrix",
        "Workflow Plan",
        "Artifact Preview",
        "Validation Evidence",
        "API / System Status",
    ]:
        assert section in text
    for endpoint in [
        "GET /api/readiness",
        "POST /api/parse",
        "POST /api/validate",
        "GET /api/adapters",
        "GET /api/validation-evidence",
        "POST /api/workflow-plan",
        "POST /api/adapter-preview",
        "GET /api/health",
        "GET /api/version",
    ]:
        assert endpoint in text
    assert "single-user local-first" in text
    assert "No cloud dependency" in text
    assert "No solver execution by default" in text
