"""Publication decision record checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_publication_decision_record_authorizes_testpypi_only():
    path = ROOT / "docs" / "publication_decision_record.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "TestPyPI uploaded: yes, for 0.9.0rc6.dev0" in text
    assert "TestPyPI upload for 0.9.0rc7: not performed" in text
    assert "PyPI published: no" in text
    assert "TestPyPI upload approval for 0.9.0rc7: pending" in text
    assert "PyPI publication approval: not granted" in text
    assert "Upload command authorized for 0.9.0rc7: no" in text
    assert "Latest TestPyPI upload attempt result: failed with HTTP 403 Forbidden" in text
    assert "docs/testpypi_status_v0.9.0rc6.dev0.md" in text
    assert "TestPyPI Trusted Publishing result: completed" in text
    assert "TestPyPI clean install verification: passed" in text
    assert ".github/workflows/testpypi-trusted-publish.yml" in text
    assert "TestPyPI Trusted Publishing workflow status: passed for 0.9.0rc6.dev0" in text
    assert "docs/pypi_publication_readiness_checklist.md" in text
    assert "docs/pypi_post_publication_verification_plan.md" in text
    assert "v1.0 public contract freeze: approved" in text
    assert "docs/v1_0_public_contract_freeze_status.md" in text
    assert "Possible publication paths" in text
    assert "Required before Future TestPyPI Upload" in text
    assert "Required before PyPI publication" in text
    assert "Final version chosen and not previously uploaded to PyPI" in text
    assert "Quality gates, CI, build, and `twine check` passed" in text
    assert "Post-publication verification plan prepared" in text
    assert "TestPyPI upload and clean-install verification\nare completed" in text
    assert "the v1.0 public contract freeze is\napproved" in text
    assert "do not publish PyPI yet" in text
    assert "unrelated `FASTAPI` package" in text
    assert "with `--no-deps`" in text
    assert "docs/testpypi_trusted_publishing.md" in text
    assert "does not\nauthorize PyPI publication" in text
