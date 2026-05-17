from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_mvp_qa_checklist_documents_demo_safety_and_verification():
    path = ROOT / "docs" / "frontend_mvp_qa_checklist.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    required = [
        "Agent Studio Frontend MVP QA Checklist",
        "0.9.0rc7.dev0",
        "demo fixture mode",
        "not live validation",
        "Loading state",
        "Empty state",
        "Error state",
        "API disconnected notice",
        "API mode indicator",
        "fixture loading buttons",
        "Diagnostics panels",
        "Recommended next actions",
        "No solver is executed by default.",
        "No external LLM is called by default.",
        "Preview artifacts are not production-grade physical validation.",
        "Formal convergence proof is not claimed.",
        "This UI does not control PyPI/TestPyPI publication or GitHub releases.",
        "aria-live",
        "./scripts/smoke_frontend_mvp.sh",
        "docs/frontend_visual_smoke_plan.md",
        "Do not commit `node_modules`",
        "Do not commit `frontend/dist`",
    ]
    for phrase in required:
        assert phrase in text
