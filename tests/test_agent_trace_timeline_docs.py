from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agent_trace_timeline_docs_exist_and_document_roles():
    for doc in ("agent_trace_timeline.md", "agent_trace_timeline.zh-CN.md"):
        path = ROOT / "docs" / doc
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        for role in [
            "SpecAgent",
            "MaterialAgent",
            "GeometryAgent",
            "AdapterAgent",
            "WorkflowAgent",
            "EvidenceAgent",
            "SafetyAgent",
            "RecommendationAgent",
        ]:
            assert role in text
        assert "POST /api/examples/{example_id}/agent-trace" in text
        assert "frontend" in text.lower() or "Agent Studio" in text
        assert "No external LLM" in text or "默认不调用外部 LLM" in text
