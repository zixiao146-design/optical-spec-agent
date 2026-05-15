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
    assert "Current: candidate" in text
    assert "docs/publication_decision_record.md" in text
    assert "docs/testpypi_status_v0.9.0rc6.dev0.md" in text
    assert "docs/v1_0_public_contract_freeze_checklist.md" in text
    assert "TestPyPI is completed for `0.9.0rc6.dev0`" in text
    assert "PyPI publication\nremains not granted" in text
    assert "Trusted Publishing passed for 0.9.0rc6.dev0" in text
    assert "failed\n  with HTTP 403 Forbidden" in text
    assert "with `--no-deps`" in text
