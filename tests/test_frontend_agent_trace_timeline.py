from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend" / "src"


def test_frontend_agent_trace_timeline_is_visible_and_safe():
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in FRONTEND.rglob("*")
        if path.suffix in {".ts", ".tsx"}
    )
    assert "Agent Trace Timeline" in source
    assert "多智能体协作轨迹" in source
    for name in [
        "SpecAgent",
        "MaterialAgent",
        "GeometryAgent",
        "AdapterAgent",
        "WorkflowAgent",
        "EvidenceAgent",
        "SafetyAgent",
        "RecommendationAgent",
    ]:
        assert name in source
    assert "final_recommendation" in source
    assert "safety_notes" in source
    assert "/api/examples/" in source
    assert "solver-run" not in source
    assert "external LLM provider" not in source
