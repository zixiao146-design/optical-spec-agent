"""Agent Studio frontend MVP user flow checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_mvp_user_flows_exist_and_include_safety_copy():
    path = ROOT / "docs" / "frontend_mvp_user_flows.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "User Flow 1: Natural language spec to preview artifact" in text
    assert "User Flow 2: JSON spec to adapter preview" in text
    assert "User Flow 3: Readiness and evidence review" in text
    assert "No solver was executed" in text
    assert "No external LLM was called" in text
    assert "No production-grade physical validation is claimed" in text
    assert "Preview artifact only" in text
    assert "Formal convergence proof is not claimed" in text
