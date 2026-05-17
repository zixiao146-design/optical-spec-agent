"""Agent Command Center documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agent_command_center_docs_exist_and_describe_task_flow():
    english = (ROOT / "docs" / "agent_command_center.md").read_text(encoding="utf-8")
    chinese = (ROOT / "docs" / "agent_command_center.zh-CN.md").read_text(encoding="utf-8")

    for text in (english, chinese):
        assert "POST /api/agent-session" in text
        assert "user goal -> optical intent -> design case" in text or "用户目标 -> 光学意图 -> 设计案例" in text
        assert "Permission" in text or "权限门控" in text
        assert "No external solver" in text or "默认不执行外部求解器" in text
        assert "No external LLM" in text or "默认不调用外部 LLM" in text
        assert "No PyPI/TestPyPI" in text or "不提供 PyPI/TestPyPI" in text
        assert "No GitHub tag/release" in text or "不提供 GitHub tag/release" in text

