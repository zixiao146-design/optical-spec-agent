"""v0.9.0rc8 release-draft documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def _read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_rc8_github_release_draft_exists_and_keeps_boundaries():
    text = _read("docs/github_release_draft_v0.9.0rc8.md")
    required = [
        "v0.9.0rc8 is the eighth release candidate",
        "Application domain benchmarks: 19 pass / 0 warn / 0 fail",
        "Gmsh: executed, passed, reviewed, accepted",
        "Optiland: executed, passed, reviewed, accepted",
        "Meep: executed, passed, reviewed, accepted",
        "MPB: executed, passed, reviewed, accepted",
        "Elmer remains deferred and not Level 3",
        "No PyPI publish",
        "No TestPyPI upload for 0.9.0rc8",
        "No production-grade physical validation",
        "No production-grade solver validation",
        "No formal convergence proof",
        "No optical correctness claim",
        "v0.9.0rc8 tag should be created only after maintainer approval",
    ]
    for phrase in required:
        assert phrase in text


def test_rc8_release_readiness_doc_is_release_draft_ready():
    text = _read("docs/release_readiness_v0.9.0rc8.md")
    required = [
        "Current public prerelease: v0.9.0rc7",
        "Current main release draft: v0.9.0rc8",
        "v0.9.0rc8 tag: not created",
        "GitHub release: not created",
        "PyPI publication approval: not granted",
        "TestPyPI upload for 0.9.0rc8: not performed",
        "Optional solver evidence closed for Gmsh / Optiland / Meep / MPB",
        "Elmer deferred and not Level 3",
        "`project.version == 0.9.0rc8`",
        "`__version__ == 0.9.0rc8`",
        "no PyPI upload",
        "no TestPyPI upload for rc8",
        "no tag/release until approval",
    ]
    for phrase in required:
        assert phrase in text


def test_rc8_release_notes_exist_and_state_not_created_yet():
    text = _read("docs/release_notes_v0.9.0rc8.md")
    required = [
        "v0.9.0rc8 is a backend-readiness release candidate draft",
        "The v0.9.0rc8 tag and GitHub release have not been created",
        "TestPyPI upload for 0.9.0rc8 has not been performed",
        "PyPI publication is not approved",
        "Application domain benchmarks report 19 pass / 0 warn / 0 fail",
        "Optional solver evidence is summarized and reviewed for Gmsh, Optiland, Meep",
        "Elmer remains deferred and not Level 3",
        "No production-grade solver validation",
        "No formal convergence proof",
        "No optical correctness claim",
    ]
    for phrase in required:
        assert phrase in text


def test_rc8_testpypi_approval_record_is_pending_and_safe():
    text = _read("docs/testpypi_upload_approval_v0.9.0rc8.md")
    required = [
        "TestPyPI upload approval for 0.9.0rc8: pending",
        "TestPyPI already uploaded and verified only for 0.9.0rc6.dev0: yes",
        "PyPI publication approval: not granted",
        "Upload command authorized for rc8: no",
        "Current main release draft: v0.9.0rc8",
        "TestPyPI upload for rc8: not performed",
        "DO NOT RUN WITHOUT APPROVAL",
        "No token should be printed, committed, logged, or pasted into chat",
    ]
    for phrase in required:
        assert phrase in text
