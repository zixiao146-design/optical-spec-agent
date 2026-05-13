"""TestPyPI dry-run gate documentation and release-smoke safety checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_testpypi_dry_run_gate_doc_exists_and_requires_manual_approval():
    text = (ROOT / "docs" / "testpypi_dry_run_gate.md").read_text(encoding="utf-8")
    assert "TestPyPI uploaded: no" in text
    assert "PyPI published: no" in text
    assert "Current public prerelease: v0.9.0rc3" in text
    assert "Current main development version: 0.9.0rc4.dev0" in text
    assert "explicit maintainer approval" in text
    assert "does not authorize upload" in text
    if "twine upload" in text:
        assert "DO NOT RUN WITHOUT APPROVAL" in text
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

