"""Agent Studio frontend MVP implementation planning checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_mvp_implementation_plan_tracks_implemented_mvp_scope():
    path = ROOT / "docs" / "frontend_mvp_implementation_plan.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "React + Vite or equivalent lightweight frontend" in text
    assert "TypeScript recommended" in text
    assert "API base URL config" in text
    assert "MVP scaffold now exists under `frontend/`" in text
    assert "Scaffold frontend. Completed." in text
    assert "Connect health/version/readiness. Completed." in text
    assert "Adapter matrix. Completed." in text
    assert "Spec input / validate. Completed." in text
    assert "Loading / empty / error / API disconnected state hardening. Completed." in text
    assert "Demo fixture mode for local walkthroughs when API is unavailable. Completed." in text
    assert "Frontend smoke script and QA checklist. Completed." in text
    assert "Keep `VITE_API_BASE_URL` local by default" in text
    assert "Demo fixture mode must be visibly labeled as not live validation" in text
    assert "Do not commit `node_modules` or frontend build artifacts" in text
    assert (ROOT / "frontend").exists()
