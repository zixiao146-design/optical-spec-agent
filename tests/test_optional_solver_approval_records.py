"""Tests for pending optional solver approval records."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RECORD_DIR = ROOT / "docs" / "optional_solver_approval_records"


def test_optional_solver_approval_records_are_pending_or_deferred():
    expected = {
        "gmsh_micro_benchmark_approval_pending.md": "pending",
        "optiland_micro_benchmark_approval_pending.md": "pending",
        "meep_micro_benchmark_approval_pending.md": "pending",
        "mpb_micro_benchmark_approval_pending.md": "pending",
        "elmer_micro_benchmark_deferred.md": "deferred",
    }
    assert RECORD_DIR.exists()
    for filename, status in expected.items():
        path = RECORD_DIR / filename
        assert path.exists(), filename
        text = path.read_text(encoding="utf-8")
        assert f"Approval status: {status}" in text
        assert "Execution authorized: no" in text
        assert "Solver execution performed: no" in text
        assert "DO NOT RUN WITHOUT APPROVAL" in text
        assert "PyPI publication: not approved" in text
        assert "TestPyPI upload: not approved" in text
        assert "Tag or GitHub release creation: not approved" in text
        assert "Production-grade physical validation: not claimed" in text
        assert "Formal convergence proof: not claimed" in text
    elmer = (RECORD_DIR / "elmer_micro_benchmark_deferred.md").read_text(
        encoding="utf-8"
    )
    assert "not Level 3" in elmer
    assert "maintainable install route" in elmer

