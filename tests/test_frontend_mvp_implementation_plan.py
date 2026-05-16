"""Agent Studio frontend MVP implementation planning checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_mvp_implementation_plan_is_planning_only():
    path = ROOT / "docs" / "frontend_mvp_implementation_plan.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "React + Vite or equivalent lightweight frontend" in text
    assert "TypeScript recommended" in text
    assert "API base URL config" in text
    assert "This task does not implement frontend code" in text
    assert "This task does not create the `frontend/` directory" in text
    assert "This task does not create the directory and does not implement frontend" in text
    assert "Scaffold frontend" in text
    assert "Connect health/version/readiness" in text
    assert "Do not commit `node_modules` or frontend build artifacts" in text
    assert not (ROOT / "frontend").exists()
