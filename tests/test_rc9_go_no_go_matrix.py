"""rc9 go/no-go matrix checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_rc9_go_no_go_matrix_lists_required_decisions():
    path = ROOT / "docs" / "rc9_go_no_go_matrix.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    for phrase in [
        "Prepare v0.9.0rc9 release draft",
        "Publish TestPyPI",
        "Publish PyPI",
        "Prepare v1.0.0 planning package",
        "Create v1.0.0 release",
        "Resume frontend polish",
        "Continue backend hardening",
    ]:
        assert phrase in text


def test_rc9_go_no_go_matrix_records_current_recommendations():
    text = (ROOT / "docs" / "rc9_go_no_go_matrix.md").read_text(encoding="utf-8")

    for phrase in [
        "| Publish PyPI | No |",
        "| Create v1.0.0 release | No |",
        "| Continue backend hardening | Yes |",
        "Do not create tag/release",
        "Elmer remains deferred and not Level 3",
    ]:
        assert phrase in text
