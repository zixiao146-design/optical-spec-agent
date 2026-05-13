"""TestPyPI upload approval record checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPROVAL_RECORD = ROOT / "docs" / "testpypi_upload_approval_v0.9.0rc5.dev0.md"


def test_testpypi_upload_approval_record_exists_and_is_pending():
    assert APPROVAL_RECORD.exists()
    text = APPROVAL_RECORD.read_text(encoding="utf-8")
    assert "TestPyPI upload approval: pending" in text
    assert "Upload command authorized: no" in text
    assert "PyPI publication approval: not granted" in text
    assert "DO NOT RUN WITHOUT APPROVAL" in text


def test_testpypi_upload_approval_record_documents_artifacts_and_token_safety():
    text = APPROVAL_RECORD.read_text(encoding="utf-8")
    assert "optical_spec_agent-0.9.0rc5.dev0-py3-none-any.whl" in text
    assert "optical_spec_agent-0.9.0rc5.dev0.tar.gz" in text
    assert "No token is printed, committed, logged, or pasted into chat" in text
    assert "Do not upload TestPyPI in this task" in text
    assert "Do not publish PyPI in this task" in text


def test_testpypi_upload_approval_record_is_linked_from_gate_docs():
    required_docs = [
        ROOT / "docs" / "testpypi_dry_run_gate.md",
        ROOT / "docs" / "pypi_publication_decision.md",
        ROOT / "docs" / "packaging_gate.md",
        ROOT / "docs" / "release_readiness_current.md",
    ]
    for path in required_docs:
        text = path.read_text(encoding="utf-8")
        assert "docs/testpypi_upload_approval_v0.9.0rc5.dev0.md" in text
        assert "TestPyPI upload approval status: pending" in text
        assert "TestPyPI upload authorized: no" in text
