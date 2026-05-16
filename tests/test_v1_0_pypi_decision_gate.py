"""v1.0 PyPI decision gate checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_0_pypi_decision_gate_exists_and_requires_explicit_approval():
    path = ROOT / "docs" / "v1_0_pypi_decision_gate.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "TestPyPI verified: yes" in text
    assert "PyPI published: no" in text
    assert "PyPI approval: not granted" in text
    assert "GitHub-only v1.0" in text
    assert "PyPI after v1.0 GitHub release" in text
    assert "I approve PyPI publication for optical-spec-agent version X." in text

