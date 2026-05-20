"""v1.0 readiness gap audit checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_v1_0_gap_audit_tracks_current_baseline_and_blockers():
    path = ROOT / "docs" / "v1_0_gap_audit.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "Current public prerelease: v0.9.0rc8" in text
    assert "Current main development version: 0.9.0rc9.dev0" in text
    assert "v0.9.0rc9 tag: not created" in text
    assert "PyPI: not published" in text
    assert "TestPyPI: uploaded for 0.9.0rc6.dev0" in text
    assert "TestPyPI upload for 0.9.0rc9.dev0: not performed" in text
    assert "TestPyPI upload approval for 0.9.0rc9.dev0: pending" in text
    assert "Elmer Level 3 validation deferred" in text
    assert "Production-grade physical validation not claimed" in text
    assert "Formal convergence proof not claimed" in text
    assert "Public contract freeze" in text
    assert "Satisfied for documented surface" in text
    assert "TestPyPI upload completed for 0.9.0rc6.dev0 via Trusted Publishing" in text
    assert "docs/testpypi_status_v0.9.0rc6.dev0.md" in text
    assert "docs/testpypi_upload_attempt_v0.9.0rc6.dev0.md" in text
    assert "HTTP 403\n  Forbidden" in text
    assert "The 0.9.0rc6.dev0 upload and clean install verification are complete" in text
    assert "PyPI publication not approved" in text
    assert "docs/v1_0_public_contract_freeze_checklist.md" in text
    assert "docs/v1_0_public_contract_freeze_confirmation.md" in text
    assert "docs/v1_0_contract_frozen_surface.md" in text
    assert "docs/v1_0_contract_non_goals.md" in text
    assert "docs/v1_0_breaking_change_policy.md" in text
    assert "docs/v1_0_public_contract_freeze_status.md" in text
    assert "public contract freeze is approved" in text
    assert "docs/publication_decision_record.md" in text
    assert "docs/pypi_publication_readiness_checklist.md" in text
    assert "docs/pypi_post_publication_verification_plan.md" in text
    assert "v1.0.0 release criteria" in text
    assert "v1.0.0 release plan" in text
    assert "RC to v1.0.0 transition path" in text
    assert "v1.0 PyPI decision gate" in text
    assert "v1.0.0 post-release verification plan" in text
    assert "Agent Studio frontend roadmap" in text
    assert "not\n  a v1.0 blocker" in text
    assert "yanking-policy review" in text
    assert "post-publication verification planning" in text
