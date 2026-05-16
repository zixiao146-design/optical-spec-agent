"""v1.0.0 release criteria documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_0_release_criteria_exists_and_bounds_release_claims():
    path = ROOT / "docs" / "v1_0_release_criteria.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Current public prerelease: v0.9.0rc6" in text
    assert "Current main development version: 0.9.0rc7.dev0" in text
    assert "v1.0 public contract freeze: approved" in text
    assert "PyPI published: no" in text
    assert "v1.0.0 released: no" in text
    assert "Production-grade physical validation is not claimed" in text
    assert "Formal convergence proof is not claimed" in text
    assert "Elmer Level 3 remains deferred" in text
    assert "Deferred/non-blocker" in text
    assert "Frontend/API Agent Studio" in text
    assert "Not a v1.0 blocker" in text
    assert "Agent Studio frontend MVP planning" in text
    assert "docs/frontend_mvp_product_spec.md" in text
    assert "docs/frontend_safety_policy.md" in text
    assert "not a PyPI publication trigger" in text
