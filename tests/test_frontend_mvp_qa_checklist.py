from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_mvp_qa_checklist_documents_demo_safety_and_verification():
    path = ROOT / "docs" / "frontend_mvp_qa_checklist.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    required = [
        "Agent Studio Frontend MVP QA Checklist",
        "0.9.0rc8",
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
        "./scripts/demo_agent_studio.sh",
        "./scripts/smoke_frontend_visual.sh",
        "docs/frontend_visual_smoke_plan.md",
        "docs/frontend_visual_smoke_runbook.md",
        "docs/agent_studio_demo_storyboard.md",
        "docs/agent_studio_demo_troubleshooting.md",
        "docs/agent_studio_demo_feedback.md",
        "docs/frontend_hardening_backlog.md",
        "docs/quickstart.md",
        "docs/quickstart.zh-CN.md",
        "./scripts/bootstrap_demo_env.sh",
        "./scripts/run_quickstart_demo.sh",
        "guided demo panel",
        "quickstart completion checklist",
        "Do not commit `node_modules`",
        "Do not commit `frontend/dist`",
        "Do not commit `frontend/test-results`",
        "Do not commit `frontend/playwright-report`",
    ]
    for phrase in required:
        assert phrase in text
