"""Agent Studio frontend roadmap documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_agent_studio_frontend_roadmap_exists_and_is_future_work():
    path = ROOT / "docs" / "agent_studio_frontend_roadmap.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Not part of v1.0.0 release criteria" in text
    assert "Should follow API readiness" in text
    assert "API response models exist" in text
    assert "examples/api/" in text
    assert "Frontend implementation is not started" in text
    assert "Spec input" in text
    assert "Adapter matrix" in text
    assert "Workflow plan" in text
    assert "Artifact preview" in text
    assert "Validation evidence view" in text
    assert "No default solver execution" in text
    assert "No cloud requirement" in text
