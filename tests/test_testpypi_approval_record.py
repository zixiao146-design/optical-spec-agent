"""TestPyPI upload approval record checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
APPROVAL_RECORD = ROOT / "docs" / "testpypi_upload_approval_v0.9.0rc6.dev0.md"
RC6_APPROVAL_RECORD = ROOT / "docs" / "testpypi_upload_approval_v0.9.0rc6.md"
RC7_APPROVAL_RECORD = ROOT / "docs" / "testpypi_upload_approval_v0.9.0rc7.dev0.md"


def test_testpypi_upload_approval_record_exists_and_grants_testpypi_only():
    assert APPROVAL_RECORD.exists()
    assert RC6_APPROVAL_RECORD.exists()
    assert RC7_APPROVAL_RECORD.exists()
    text = APPROVAL_RECORD.read_text(encoding="utf-8")
    assert "TestPyPI upload approval: granted for 0.9.0rc6.dev0 only" in text
    assert "Upload command authorized: TestPyPI only" in text
    assert "PyPI publication approval: not granted" in text
    assert "AUTHORIZED FOR TESTPYPI ONLY FOR 0.9.0rc6.dev0" in text
    rc6_text = RC6_APPROVAL_RECORD.read_text(encoding="utf-8")
    assert "TestPyPI upload approval for 0.9.0rc6: pending" in rc6_text
    assert "Upload command authorized for rc6: no" in rc6_text
    assert "PyPI publication approval: not granted" in rc6_text
    rc7_text = RC7_APPROVAL_RECORD.read_text(encoding="utf-8")
    assert "TestPyPI upload approval: pending" in rc7_text
    assert "Upload command authorized: no" in rc7_text
    assert "Current main development version: 0.9.0rc7.dev0" in rc7_text
    assert "TestPyPI upload for 0.9.0rc7.dev0: not performed" in rc7_text


def test_testpypi_upload_approval_record_documents_artifacts_and_token_safety():
    text = APPROVAL_RECORD.read_text(encoding="utf-8")
    assert "optical_spec_agent-0.9.0rc6.dev0-py3-none-any.whl" in text
    assert "optical_spec_agent-0.9.0rc6.dev0.tar.gz" in text
    assert "No token is printed, committed, logged, or pasted into chat" in text
    assert "TestPyPI upload is authorized only for `0.9.0rc6.dev0`" in text
    assert "Do not publish PyPI in this task" in text
    assert "GitHub release/tag creation remains prohibited" in text


def test_testpypi_upload_approval_record_is_linked_from_gate_docs():
    required_docs = [
        ROOT / "docs" / "testpypi_dry_run_gate.md",
        ROOT / "docs" / "pypi_publication_decision.md",
        ROOT / "docs" / "packaging_gate.md",
        ROOT / "docs" / "release_readiness_current.md",
    ]
    for path in required_docs:
        text = path.read_text(encoding="utf-8")
        assert "docs/testpypi_upload_approval_v0.9.0rc7.dev0.md" in text
        assert "pending" in text
        assert "docs/testpypi_status_v0.9.0rc6.dev0.md" in text
