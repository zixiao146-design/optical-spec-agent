"""Local Agent API launch guide checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_api_local_launch_guide_exists_and_bounds_defaults():
    path = ROOT / "docs" / "api_local_launch_guide.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Local Agent API Launch Guide" in text
    assert "python -m uvicorn optical_spec_agent.api.app:app" in text
    assert "--host 127.0.0.1 --port 8000" in text
    assert "/api/health" in text
    assert "No external solver execution by default" in text
    assert "No external LLM call by default" in text
    assert "No proprietary solver required" in text
    assert "No production-grade physical validation claim" in text
    assert "No formal convergence proof claim" in text
    assert "Future Agent Studio frontend work should call this local API" in text
    assert "shelling out directly to the CLI" in text
