"""Frontend Agent Command Center guard tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend" / "src"


def _frontend_source() -> str:
    return "\n".join(
        path.read_text(encoding="utf-8")
        for path in FRONTEND.rglob("*")
        if path.suffix in {".ts", ".tsx"}
    )


def test_frontend_agent_command_center_page_exists_and_calls_api():
    page = FRONTEND / "pages" / "AgentCommandCenterPage.tsx"
    assert page.exists()
    source = _frontend_source()
    required = [
        "AgentCommandCenterPage",
        "Agent Command Center",
        "Agent 命令中心",
        "\"/api/agent-session\"",
        "agent-command-goal",
        "permission_gates",
        "artifacts",
        "AgentPlanPanel",
        "PermissionGatePanel",
        "AgentArtifactPanel",
    ]
    for phrase in required:
        assert phrase in source


def test_frontend_agent_command_center_keeps_forbidden_controls_absent():
    source = _frontend_source().lower()
    forbidden = [
        "twine upload",
        "gh release create",
        "git tag",
        "upload to pypi",
        "upload to testpypi",
        "create tag",
        "create release",
        "run solver",
        "external llm provider",
    ]
    for phrase in forbidden:
        assert phrase not in source

