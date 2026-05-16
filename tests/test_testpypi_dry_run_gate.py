"""TestPyPI dry-run gate documentation and release-smoke safety checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_testpypi_dry_run_gate_doc_exists_and_requires_manual_approval():
    text = (ROOT / "docs" / "testpypi_dry_run_gate.md").read_text(encoding="utf-8")
    assert "TestPyPI uploaded: yes, for 0.9.0rc6.dev0" in text
    assert "TestPyPI upload for 0.9.0rc7.dev0: not performed" in text
    assert "PyPI published: no" in text
    assert "Current public prerelease: v0.9.0rc6" in text
    assert "Current main development version: `0.9.0rc7.dev0`" in text
    assert "explicit maintainer approval" in text
    assert "does\nnot authorize PyPI publication" in text
    assert "scripts/testpypi_preflight.sh" in text
    assert "docs/testpypi_upload_approval_v0.9.0rc6.dev0.md" in text
    assert "docs/testpypi_upload_approval_v0.9.0rc6.md" in text
    assert "docs/testpypi_upload_approval_v0.9.0rc7.dev0.md" in text
    assert "docs/testpypi_upload_attempt_v0.9.0rc6.dev0.md" in text
    assert "docs/testpypi_status_v0.9.0rc6.dev0.md" in text
    assert "TestPyPI upload approval status for 0.9.0rc7.dev0: pending" in text
    assert "Upload command authorized for 0.9.0rc7.dev0: no" in text
    assert "Latest TestPyPI upload attempt result: failed with HTTP 403 Forbidden" in text
    assert "TestPyPI Trusted Publishing workflow status: passed for 0.9.0rc6.dev0" in text
    assert "TestPyPI clean install verification: passed" in text
    assert "PyPI publication approval: not granted" in text
    assert "NO UPLOAD PERFORMED" in text
    assert "does not upload" in text
    assert "does not create tags" in text
    if "twine upload" in text:
        assert "HISTORICAL LOCAL TOKEN TEMPLATE FOR 0.9.0rc6.dev0 ONLY" in text
        assert "Do not run this command for PyPI" in text
    assert "Token must never be committed or printed" in text


def test_smoke_release_script_contains_no_publish_or_release_commands():
    script = (ROOT / "scripts" / "smoke_release.sh").read_text(encoding="utf-8")
    lowered = script.lower()
    forbidden = [
        "twine upload",
        "gh release create",
        "pypi upload",
    ]
    for phrase in forbidden:
        assert phrase not in lowered
    assert "OSA_SMOKE_ALLOW_PUBLISH" in script
    assert "OSA_SMOKE_VERIFY_WHEEL" in script


def test_testpypi_preflight_script_contains_no_publish_or_release_commands():
    script = (ROOT / "scripts" / "testpypi_preflight.sh").read_text(encoding="utf-8")
    lowered = script.lower()
    forbidden = [
        "twine upload",
        "gh release create",
        "git push",
    ]
    for phrase in forbidden:
        assert phrase not in lowered
    assert "NO UPLOAD PERFORMED" in script
