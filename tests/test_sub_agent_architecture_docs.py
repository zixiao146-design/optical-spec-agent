from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_sub_agent_architecture_docs_exist_and_document_roles():
    for relative in ["docs/sub_agent_architecture.md", "docs/sub_agent_architecture.zh-CN.md"]:
        path = ROOT / relative
        assert path.exists()
        text = path.read_text(encoding="utf-8")
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
            assert name in text
        assert "No external LLM" in text or "默认不调用外部 LLM" in text
        assert "No external solver" in text or "默认不执行外部求解器" in text
