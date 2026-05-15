"""Publication decision record checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_publication_decision_record_authorizes_testpypi_only():
    path = ROOT / "docs" / "publication_decision_record.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "TestPyPI uploaded: no" in text
    assert "PyPI published: no" in text
    assert "TestPyPI upload approval: granted for 0.9.0rc6.dev0 only" in text
    assert "PyPI publication approval: not granted" in text
    assert "Upload command authorized: TestPyPI only" in text
    assert "Latest TestPyPI upload attempt result: failed with HTTP 403 Forbidden" in text
    assert "Possible publication paths" in text
    assert "Required before TestPyPI upload" in text
    assert "Required before PyPI publication" in text
    assert "upload `0.9.0rc6.dev0` to TestPyPI only" in text
    assert "TestPyPI\nremains not uploaded" in text
    assert "does not\nauthorize PyPI publication" in text
