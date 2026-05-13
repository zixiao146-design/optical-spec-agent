"""v1.0 stability gate documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_0_stability_gate_doc_exists_and_bounds_claims():
    text = (ROOT / "docs" / "v1_0_stability_gate.md").read_text(encoding="utf-8")
    assert "v1.0.0 not ready yet" in text
    assert "Production-grade physical validation not claimed" in text
    assert "Formal convergence proof not claimed" in text
    assert "External solver validation is optional/manual" in text
    assert "External LLM is optional and not required by default" in text


def test_v1_0_stability_gate_references_required_gate_areas():
    text = (ROOT / "docs" / "v1_0_stability_gate.md").read_text(encoding="utf-8")
    required = [
        "CLI contract",
        "Schema contract",
        "Adapter support matrix",
        "Workflow preview contract",
        "Validation boundary",
        "Packaging gate",
        "TestPyPI/PyPI decision",
        "Token/security policy",
        "Release rollback policy",
    ]
    for phrase in required:
        assert phrase in text
