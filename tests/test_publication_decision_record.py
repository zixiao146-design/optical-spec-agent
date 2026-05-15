"""Publication decision record checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_publication_decision_record_keeps_upload_and_publish_unapproved():
    path = ROOT / "docs" / "publication_decision_record.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "TestPyPI uploaded: no" in text
    assert "PyPI published: no" in text
    assert "TestPyPI upload approval: pending" in text
    assert "PyPI publication approval: not granted" in text
    assert "Upload command authorized: no" in text
    assert "Possible publication paths" in text
    assert "Required before TestPyPI upload" in text
    assert "Required before PyPI publication" in text
    assert "Recommended current state: keep TestPyPI/PyPI pending" in text
    assert "does not authorize `twine upload`" in text
