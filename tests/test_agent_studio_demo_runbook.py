from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agent_studio_demo_runbook_documents_local_walkthrough_and_safety():
    path = ROOT / "docs" / "agent_studio_demo_runbook.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    required = [
        "./scripts/demo_agent_studio.sh",
        "./scripts/bootstrap_demo_env.sh",
        "./scripts/run_quickstart_demo.sh",
        "docs/quickstart.md",
        "Start guided demo",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000/api/health",
        "Dashboard / Readiness",
        "Spec Input",
        "Adapter Matrix",
        "Workflow Plan",
        "Artifact Preview",
        "Validation Evidence",
        "System Status",
        "No solver execution by default",
        "No external LLM call by default",
        "No PyPI/TestPyPI upload controls",
        "No tag/release controls",
        "No production-grade validation claim",
        "No formal convergence proof claim",
    ]
    for phrase in required:
        assert phrase in text
