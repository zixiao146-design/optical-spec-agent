"""Frontend visual smoke runbook checks."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_visual_smoke_runbook_documents_manual_optional_playwright():
    path = ROOT / "docs" / "frontend_visual_smoke_runbook.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for phrase in [
        "Frontend Visual Smoke Runbook",
        "manual / optional",
        "./scripts/smoke_frontend_visual.sh",
        "npx playwright install chromium",
        "npm run visual:smoke",
        "Dashboard",
        "Spec Input",
        "Adapter Matrix",
        "Workflow Plan",
        "Artifact Preview",
        "Validation Evidence",
        "System Status",
        "No solver execution",
        "No external LLM call",
        "No package upload",
        "No tag creation",
        "No GitHub release creation",
        "frontend/test-results/",
        "frontend/playwright-report/",
    ]:
        assert phrase in text
