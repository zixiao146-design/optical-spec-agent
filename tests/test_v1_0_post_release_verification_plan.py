"""v1.0.0 post-release verification plan checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_0_post_release_verification_plan_exists_and_bounds_claims():
    path = ROOT / "docs" / "v1_0_post_release_verification_plan.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Verify GitHub tag target" in text
    assert "Verify release notes match the local draft" in text
    assert "Clean install from PyPI if PyPI is published" in text
    assert "Run `optical-spec --help`" in text
    assert "Run `optical-spec adapter-list --json`" in text
    assert "Ensure no production-grade physical validation claim was added" in text

