"""Frontend Playwright visual smoke script checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_frontend_visual_script_exists_and_is_safe():
    path = ROOT / "scripts" / "smoke_frontend_visual.sh"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for phrase in [
        "npx playwright install chromium",
        "npm run visual:smoke",
        "trap cleanup EXIT",
        "python -m uvicorn optical_spec_agent.api.app:app",
        "NO SOLVER EXECUTION PERFORMED",
        "NO EXTERNAL LLM CALLED",
        "NO UPLOAD PERFORMED",
        "NO TAG CREATED",
        "NO RELEASE CREATED",
        "test-results",
        "playwright-report",
    ]:
        assert phrase in text

    lowered = text.lower()
    for phrase in ["twine upload", "gh release create", "git tag", "git push"]:
        assert phrase not in lowered
