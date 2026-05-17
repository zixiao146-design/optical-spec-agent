from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend" / "src"


def test_frontend_agent_collaboration_page_exists_and_shows_sub_agents():
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in FRONTEND.rglob("*")
        if path.suffix in {".ts", ".tsx"}
    )
    assert (FRONTEND / "pages" / "AgentCollaborationPage.tsx").exists()
    assert "Agent Collaboration" in source
    assert "子智能体协作" in source
    assert "/api/agent-trace" in source
    for name in ["SpecAgent", "MaterialAgent", "AdapterAgent", "SafetyAgent"]:
        assert name in source
    assert "Upload to TestPyPI" not in source
    assert "Create tag" not in source
    assert "Run solver" not in source
