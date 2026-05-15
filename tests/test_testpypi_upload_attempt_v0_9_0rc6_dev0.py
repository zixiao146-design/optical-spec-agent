"""TestPyPI upload attempt status checks for 0.9.0rc6.dev0."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ATTEMPT_DOC = ROOT / "docs" / "testpypi_upload_attempt_v0.9.0rc6.dev0.md"


def test_testpypi_upload_attempt_records_failed_upload_without_pypi_publish():
    assert ATTEMPT_DOC.exists()
    text = ATTEMPT_DOC.read_text(encoding="utf-8")

    assert "TestPyPI upload: attempted, not completed" in text
    assert "TestPyPI upload approval: granted for 0.9.0rc6.dev0 only" in text
    assert "Upload command authorized: TestPyPI only" in text
    assert "TestPyPI uploaded: no" in text
    assert "PyPI published: no" in text
    assert "PyPI publication approval: not granted" in text
    assert "GitHub tag created: no" in text
    assert "GitHub release created: no" in text
    assert "HTTP 403 Forbidden" in text
    assert "token cleanup: yes" in text
    assert "token printed, saved, or committed: no" in text
    assert "clean install from TestPyPI: not run because upload failed" in text
    assert "no production-grade physical validation" in text
    assert "no formal convergence proof" in text
