from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_visual_smoke_plan_documents_future_checks():
    path = ROOT / "docs" / "frontend_visual_smoke_plan.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for phrase in [
        "Agent Studio Frontend Visual Smoke Plan",
        "Dashboard",
        "Spec Input",
        "Adapter Matrix",
        "Workflow Plan",
        "Artifact Preview",
        "Validation Evidence",
        "System Status",
        "API connected state",
        "API disconnected/demo mode state",
        "No upload/release controls",
        "No default solver or external LLM controls",
        "Playwright visual smoke support is now added",
        "manual optional",
        "not part of the default release gate",
        "frontend_visual_smoke_runbook.md",
        "scripts/smoke_frontend_visual.sh",
    ]:
        assert phrase in text
