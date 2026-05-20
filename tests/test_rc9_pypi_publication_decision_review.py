"""rc9 PyPI publication decision review checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_rc9_pypi_publication_decision_review_keeps_publication_deferred():
    path = ROOT / "docs" / "rc9_pypi_publication_decision_review.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    for phrase in [
        "PyPI published: no",
        "PyPI approval: not granted",
        "TestPyPI only 0.9.0rc6.dev0 verified",
        "Current main dev: 0.9.0rc9.dev0",
        "Current public prerelease: v0.9.0rc8",
        "Keep PyPI deferred",
        "No upload command is authorized",
    ]:
        assert phrase in text


def test_rc9_pypi_publication_decision_review_lists_decision_paths():
    text = (ROOT / "docs" / "rc9_pypi_publication_decision_review.md").read_text(
        encoding="utf-8"
    )

    for phrase in [
        "GitHub-only continue",
        "TestPyPI latest preflight/upload",
        "PyPI pre-release publication",
        "PyPI stable only after v1.0.0 approval",
        "PyPI publication must not imply production-grade validation",
    ]:
        assert phrase in text
