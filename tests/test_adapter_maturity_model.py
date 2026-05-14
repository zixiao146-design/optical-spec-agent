"""Adapter maturity model documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_adapter_maturity_model_exists_and_bounds_claims():
    path = ROOT / "docs" / "adapter_maturity_model.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for level in ["Level 0", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5"]:
        assert level in text
    for adapter in ["Meep", "Gmsh", "Elmer", "MPB", "Optiland"]:
        assert adapter in text
    assert "External solver required by default" in text
    assert "| Gmsh | Level 2" in text
    assert "pilot path toward Level 3" in text
    assert "no | no | no" in text
    assert "No production-grade physical validation claim" in text
    assert "No formal convergence proof" in text
