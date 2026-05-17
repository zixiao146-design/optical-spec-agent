from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agent_studio_demo_storyboard_links_workflow_api_and_safety():
    path = ROOT / "docs" / "agent_studio_demo_storyboard.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    required = [
        "agent-like workflow",
        "GET /api/readiness",
        "POST /api/parse",
        "POST /api/validate",
        "POST /api/workflow-plan",
        "POST /api/adapter-preview",
        "GET /api/validation-evidence",
        "safety note",
        "Validation Evidence",
        "local-first",
        "open-source-solver-first",
        "preview-first",
        "No solver is executed by default",
        "No external LLM is called by default",
        "No production-grade physical validation",
    ]
    for phrase in required:
        assert phrase in text
