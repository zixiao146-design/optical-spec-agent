"""API smoke script safety checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_agent_api_script_exists_and_does_not_publish_or_release():
    path = ROOT / "scripts" / "smoke_agent_api.sh"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for phrase in [
        "NO SOLVER EXECUTION PERFORMED",
        "NO EXTERNAL LLM CALLED",
        "NO PROPRIETARY SOLVER REQUIRED",
        "NO UPLOAD PERFORMED",
        "NO TAG CREATED",
        "NO RELEASE CREATED",
        "/api/health",
        "/api/version",
        "/api/adapters",
        "/api/schema",
        "/api/parse",
        "/api/validate",
        "/api/workflow-plan",
        "/api/adapter-preview",
        "/api/validation-evidence",
        "/api/readiness",
    ]:
        assert phrase in text
    lowered = text.lower()
    forbidden = ["twine upload", "gh release create", "git tag", "git push"]
    for phrase in forbidden:
        assert phrase not in lowered
