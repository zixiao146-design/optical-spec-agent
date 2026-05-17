from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agent_studio_demo_checklist_covers_demo_phases_and_artifacts():
    path = ROOT / "docs" / "agent_studio_demo_checklist.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    required = [
        "Pre-demo",
        "During demo",
        "Post-demo",
        "docs/quickstart.md",
        "./scripts/bootstrap_demo_env.sh",
        "./scripts/run_quickstart_demo.sh",
        "Guided demo panel",
        "git status clean",
        "No upload/tag/release controls visible",
        "Do not commit screenshots unless explicitly approved",
        "API smoke",
        "frontend smoke",
        "optional visual smoke",
        "No solver-run or external LLM controls visible",
    ]
    for phrase in required:
        assert phrase in text
