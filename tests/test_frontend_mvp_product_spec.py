"""Agent Studio frontend MVP product spec checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_mvp_product_spec_exists_and_bounds_mvp_scope():
    path = ROOT / "docs" / "frontend_mvp_product_spec.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Agent Studio Frontend MVP Product Spec" in text
    assert "Current public prerelease: v0.9.0rc7" in text
    assert "Current main release draft: 0.9.0rc8" in text
    assert "API contract version: 0.1" in text
    assert "Frontend implementation: MVP implemented under `frontend/`" in text
    assert "make the project feel like an agent" in text.lower()
    assert "Expose spec parsing and validation visually" in text
    assert "Show adapter maturity and validation evidence" in text
    assert "Show workflow plan steps" in text
    assert "Show generated preview artifacts" in text
    assert "No external solver execution by default" in text
    assert "No external LLM call by default" in text
    assert "No production-grade validation claim" in text
    assert "No formal convergence proof" in text
    assert "React + Vite + TypeScript scaffold exists in `frontend/`" in text
    assert "docs/frontend_mvp_runbook.md" in text
    assert "Loading, empty, error, API disconnected, and demo fixture states" in text
    assert "Demo fixture mode is labeled as not live validation" in text
