"""PyPI publication readiness checklist checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_pypi_publication_readiness_checklist_tracks_current_gate():
    path = ROOT / "docs" / "pypi_publication_readiness_checklist.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    assert "TestPyPI uploaded: yes" in text
    assert "TestPyPI version: 0.9.0rc6.dev0" in text
    assert "TestPyPI upload for 0.9.0rc9.dev0: not performed" in text
    assert "Clean install from TestPyPI: passed" in text
    assert "PyPI published: no" in text
    assert "PyPI publication approval: not granted" in text
    assert "Upload command authorized for PyPI: no" in text
    assert "v1.0 public contract freeze: approved" in text
    assert "docs/v1_0_public_contract_freeze_status.md" in text
    assert "Explicit maintainer approval" in text
    assert "Quality gates passed" in text
    assert "GitHub Actions CI passed" in text
    assert "`python -m build` passed" in text
    assert "`python -m twine check dist/*` passed" in text
    assert "Validation claims reviewed and kept conservative" in text
    assert "Do not publish PyPI yet" in text
    assert "Prepare PyPI only after a separate explicit publication decision" in text
    assert "docs/rc9_pypi_publication_decision_review.md" in text
    assert "Current recommendation: keep PyPI deferred" in text
    assert "Upload command authorized for PyPI: no" in text


def test_pypi_publication_readiness_checklist_records_risks_and_limits():
    text = (ROOT / "docs" / "pypi_publication_readiness_checklist.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "Package name claim is permanent once published",
        "File/version uploads cannot be freely overwritten",
        "Bad metadata may require a new version",
        "PyPI yanking is possible but not the same as deletion",
        "Production claims must remain conservative",
        "Dependency resolution differs from TestPyPI",
        "does not authorize PyPI publication",
        "formal convergence proof claims",
        "TestPyPI upload for `0.9.0rc9.dev0`: not performed",
    ]:
        assert phrase in text
