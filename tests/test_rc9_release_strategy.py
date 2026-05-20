"""rc9 release strategy checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_rc9_release_strategy_records_active_dev_and_no_release_action():
    path = ROOT / "docs" / "rc9_release_strategy.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")

    for phrase in [
        "`0.9.0rc9.dev0` is active development",
        "Do not create a GitHub release now",
        "Keep PyPI publication as a separate decision",
        "Keep v1.0.0 planning and release approval as separate decisions",
        "Do not create a v0.9.0rc9 tag",
    ]:
        assert phrase in text


def test_rc9_release_strategy_lists_future_release_draft_checks():
    text = (ROOT / "docs" / "rc9_release_strategy.md").read_text(encoding="utf-8")

    for phrase in [
        "Validation claim audit",
        "Application benchmarks",
        "Optional solver wrapper default no-execute",
        "Backend evidence pack",
        "Quality gates",
        "Wheel smoke",
        "Pytest",
        "build",
        "make check",
        "CLI examples",
    ]:
        assert phrase in text
