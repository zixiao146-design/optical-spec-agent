"""Post-v0.9.0rc8 rc9 development-state documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_rc9_development_readiness_doc_records_post_rc8_state():
    text = _read("docs/release_readiness_v0.9.0rc9.md")
    required = [
        "Current public prerelease: v0.9.0rc8",
        "Current main development version: 0.9.0rc9.dev0",
        "0.9.0rc9.dev0 is not itself a\npublic release",
        "v0.9.0rc9 tag: not created",
        "v1.0.0 tag: not created",
        "PyPI: not published",
        "TestPyPI uploaded and verified only for 0.9.0rc6.dev0",
        "TestPyPI upload for 0.9.0rc9.dev0: not performed",
        "PyPI publication approval: not granted",
        "Optional solver evidence closed for Gmsh, Optiland, Meep, and MPB",
        "Elmer remains deferred and not Level 3",
        "Do not claim production-grade physical validation",
        "Do not claim production-grade solver validation",
        "Do not claim formal convergence proof",
        "Do not claim optical correctness",
    ]
    for snippet in required:
        assert snippet in text


def test_rc9_testpypi_approval_record_is_pending_and_no_upload():
    text = _read("docs/testpypi_upload_approval_v0.9.0rc9.dev0.md")
    required = [
        "TestPyPI upload approval: pending",
        "PyPI publication approval: not granted",
        "Upload command authorized: no",
        "Current public prerelease: v0.9.0rc8",
        "Current main development version: 0.9.0rc9.dev0",
        "v0.9.0rc9 tag: not created",
        "TestPyPI upload for 0.9.0rc9.dev0: not performed",
        "DO NOT RUN WITHOUT APPROVAL",
        "No token should be printed, committed, logged, or pasted into chat",
    ]
    for snippet in required:
        assert snippet in text
