from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agent_studio_demo_feedback_records_review_without_overclaiming():
    path = ROOT / "docs" / "agent_studio_demo_feedback.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    required = [
        "Current public prerelease: v0.9.0rc7",
        "Current main development version: 0.9.0rc8.dev0",
        "Latest localized frontend commit reviewed: 212b880",
        "Demo was run locally: yes",
        "MilesLee",
        "五月十七日",
        "还是很粗糙简陋",
        "公开演示前必须增加中文手把手教程",
        "Page-by-page feedback has not been provided yet",
        "frontend_hardening_backlog.md",
        "No upload controls",
        "No tag/release controls",
        "No default solver execution",
        "No default external LLM",
        "No production-grade validation claim",
        "No formal convergence proof claim",
        "PyPI published: no",
        "GitHub release action approved: no",
    ]
    for phrase in required:
        assert phrase in text
