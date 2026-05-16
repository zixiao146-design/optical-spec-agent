"""v1.0 decision matrix checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_0_decision_matrix_covers_required_decisions():
    path = ROOT / "docs" / "v1_0_decision_matrix.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "TestPyPI upload" in text
    assert "PyPI publication" in text
    assert "Elmer Level 3" in text
    assert "Production-grade physical validation" in text
    assert "Public contract freeze" in text
    assert "Current: completed for 0.9.0rc6.dev0" in text
    assert "Current: not approved" in text
    assert "Current: deferred" in text
    assert "Current: not claimed" in text
    assert "Current: approved" in text
    assert "docs/publication_decision_record.md" in text
    assert "docs/pypi_publication_readiness_checklist.md" in text
    assert "docs/pypi_post_publication_verification_plan.md" in text
    assert "docs/testpypi_status_v0.9.0rc6.dev0.md" in text
    assert "docs/v1_0_public_contract_freeze_checklist.md" in text
    assert "docs/v1_0_public_contract_freeze_confirmation.md" in text
    assert "docs/v1_0_public_contract_freeze_status.md" in text
    assert "docs/v1_0_contract_frozen_surface.md" in text
    assert "docs/v1_0_contract_non_goals.md" in text
    assert "docs/v1_0_breaking_change_policy.md" in text
    assert "Maintainer confirmation: approved" in text
    assert "TestPyPI is completed for `0.9.0rc6.dev0`" in text
    assert "PyPI publication remains not granted" in text
    assert "do not publish PyPI yet" in text
    assert "Public contract freeze is approved for the documented surface" in text
    assert "Trusted Publishing passed for 0.9.0rc6.dev0" in text
    assert "failed\n  with HTTP 403 Forbidden" in text
    assert "with `--no-deps`" in text
