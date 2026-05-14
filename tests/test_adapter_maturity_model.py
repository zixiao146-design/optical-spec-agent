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
    assert "| Meep | Level 3" in text
    assert "| Gmsh | Level 3" in text
    assert "| MPB | Level 3" in text
    assert "| Optiland | Level 3" in text
    assert "validation/meep/meep_validation_pilot_2026-05-14.md" in text
    assert "validation/gmsh/gmsh_validation_pilot_2026-05-14.md" in text
    assert "validation/mpb/mpb_validation_pilot_2026-05-14.md" in text
    assert "validation/optiland/optiland_validation_pilot_2026-05-14.md" in text
    assert "Default tests, smoke, quality gates, CI, and release validation still do not run Meep" in text
    assert "Default tests, smoke, quality gates, and release validation still do not run Gmsh" in text
    assert "does not require MPB CLI" in text
    assert "does not make Optiland a default dependency" in text
    assert "no | no | no" in text
    assert "No production-grade physical validation claim" in text
    assert "No formal convergence proof" in text
