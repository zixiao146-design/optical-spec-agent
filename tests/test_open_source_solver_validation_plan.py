"""Optional open-source solver validation plan checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_open_source_solver_validation_plan_exists_and_names_candidate_families():
    path = ROOT / "docs" / "open_source_solver_validation_plan.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for name in ["Meep", "Gmsh", "Elmer", "MPB"]:
        assert name in text
    assert "Optiland" in text


def test_open_source_solver_validation_plan_is_optional_manual_and_skipped_by_default():
    text = (ROOT / "docs" / "open_source_solver_validation_plan.md").read_text(encoding="utf-8")
    for phrase in [
        "optional solver-backed validation",
        "No external solver is run by default",
        "No proprietary license required",
        "No network required by default",
        "Tests are skipped by default unless enabled",
        "not be part of default `pytest`",
        "not be part of default `scripts/smoke_release.sh`",
    ]:
        assert phrase in text
