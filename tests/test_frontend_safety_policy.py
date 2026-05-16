"""Agent Studio frontend safety policy checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_safety_policy_keeps_mvp_local_and_non_publishing():
    path = ROOT / "docs" / "frontend_safety_policy.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "No default solver execution" in text
    assert "No default external LLM" in text
    assert "No PyPI/TestPyPI upload controls in MVP" in text
    assert "No tag/release controls in MVP" in text
    assert "No proprietary solver default integration" in text
    assert "No production-grade physical validation claim" in text
    assert "No formal convergence proof claim" in text
    assert "Optional solver execution, if ever added, must require explicit approval gates" in text
    assert "demo fixture mode must be labeled as not live validation" in text
    assert "Loading, empty, error, and API disconnected states" in text
