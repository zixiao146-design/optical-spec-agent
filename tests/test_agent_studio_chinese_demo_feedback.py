from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_real_chinese_demo_feedback_is_recorded_without_placeholder_or_invention():
    text = (ROOT / "docs" / "agent_studio_demo_feedback.md").read_text(encoding="utf-8")
    assert "[在这里粘贴我的观察]" not in text
    required = [
        "MilesLee",
        "五月十七日",
        "还是很粗糙简陋",
        "手把手教程",
        "P1: 待进一步 demo 反馈确认",
        "P2: 待进一步 demo 反馈确认",
        "Page-by-page feedback has not been provided yet",
        "Do not invent detailed page feedback",
    ]
    for phrase in required:
        assert phrase in text
