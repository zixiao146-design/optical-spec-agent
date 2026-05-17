"""Agent Studio frontend MVP acceptance criteria checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_mvp_acceptance_criteria_cover_functional_safety_and_technical_scope():
    path = ROOT / "docs" / "frontend_mvp_acceptance_criteria.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Functional criteria" in text
    assert "Safety criteria" in text
    assert "Technical criteria" in text
    assert "Can call all frontend-ready endpoints" in text
    assert "Can render Agent Command Center" in text
    assert "POST /api/agent-session" in text
    assert "permission gates" in text
    assert "Can render adapter matrix" in text
    assert "Can render workflow plan" in text
    assert "Can show loading, empty, error, and API disconnected states" in text
    assert "Can show demo fixture mode" in text
    assert "UI must not expose PyPI/TestPyPI upload button" in text
    assert "UI must not expose tag/release button" in text
    assert "UI must not imply production-grade validation" in text
    assert "UI must not imply formal convergence proof" in text
    assert "API base configurable" in text
    assert "Uses API contract version 0.1" in text
    assert "No generated build artifacts committed" in text
    assert "LoadingState" in text
    assert "ApiDisconnectedNotice" in text
    assert "aria-live" in text
