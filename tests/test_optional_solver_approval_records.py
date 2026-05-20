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


def test_gmsh_approved_execution_record_is_separate_from_pending_template():
    path = RECORD_DIR / "gmsh_micro_benchmark_approval_2026-05-20.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Approval status: approved for this Gmsh run" in text
    assert "Execution authorized: yes, Gmsh only" in text
    assert "Solver execution performed: yes, Gmsh only" in text
    assert "Other solvers authorized: no" in text
    assert "PyPI publication authorized: no" in text
    assert "TestPyPI upload authorized: no" in text
    assert "Tag or GitHub release creation authorized: no" in text
    assert "validation/gmsh/gmsh_micro_benchmark_2026-05-20.md" in text


def test_gmsh_review_record_accepts_evidence_without_new_authorization():
    path = RECORD_DIR / "gmsh_micro_benchmark_review_2026-05-20.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Review status: accepted as optional manual mesh-generation smoke evidence" in text
    assert "Other solvers executed: no" in text
    assert "PyPI/TestPyPI upload: no" in text
    assert "Tag/release action: no" in text
    assert "does not authorize any further solver execution" in text
    assert "Optiland may be considered next, but requires separate explicit approval" in text


def test_optiland_approved_execution_record_is_separate_from_pending_template():
    path = RECORD_DIR / "optiland_micro_benchmark_approval_2026-05-20.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Approval status: approved for this Optiland run" in text
    assert "Execution authorized: yes, Optiland only" in text
    assert "Other solvers authorized: no" in text
    assert "PyPI/TestPyPI/tag/release authorized: no" in text
    assert "DO NOT RUN WITHOUT APPROVAL" not in text
    assert "validation/optiland/optiland_micro_benchmark_2026-05-20.md" not in text
    assert "no production-grade physical validation" in text
    assert "no formal convergence proof" in text
    assert "no optical correctness claim" in text


def test_optiland_review_record_accepts_evidence_without_new_authorization():
    path = RECORD_DIR / "optiland_micro_benchmark_review_2026-05-20.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Review status: accepted as optional manual ray/path smoke evidence" in text
    assert "Gmsh rerun in this task: no" in text
    assert "Meep executed: no" in text
    assert "MPB executed: no" in text
    assert "Elmer executed: no" in text
    assert "PyPI/TestPyPI upload: no" in text
    assert "Tag/release action: no" in text
    assert "does not authorize any further solver execution" in text
    assert "requires explicit OSA_SOLVER_PYTHON profile and separate approval" in text


def test_meep_pending_record_references_decision_packet_without_authorization():
    pending = RECORD_DIR / "meep_micro_benchmark_approval_pending.md"
    packet = RECORD_DIR / "meep_micro_benchmark_decision_packet.md"
    assert pending.exists()
    assert packet.exists()
    text = pending.read_text(encoding="utf-8")
    assert "Approval status: pending" in text
    assert "Execution authorized: no" in text
    assert "Solver execution performed: no" in text
    assert "meep_micro_benchmark_decision_packet.md" in text
    assert "OSA_SOLVER_PYTHON" in text
    assert "OSA_SOLVER_READINESS_PROFILE=osa-solvers" in text
    assert "does not authorize MPB execution, Meep execution, uploads, tags, or releases" in text


def test_meep_approved_execution_record_is_separate_from_pending_template():
    path = RECORD_DIR / "meep_micro_benchmark_approval_2026-05-20.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Approval status: approved for this Meep run" in text
    assert "Execution authorized: yes, Meep only" in text
    assert (
        "OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python"
        in text
    )
    assert "MPB authorized: no" in text
    assert "Gmsh authorized: no" in text
    assert "Optiland authorized: no" in text
    assert "Elmer authorized: no" in text
    assert "PyPI/TestPyPI/tag/release authorized: no" in text
    assert "no production-grade FDTD validation" in text
    assert "no formal convergence proof" in text
    assert "no optical correctness claim" in text


def test_meep_review_record_accepts_evidence_without_new_authorization():
    path = RECORD_DIR / "meep_micro_benchmark_review_2026-05-20.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Review status: accepted as optional manual PyMeep/FDTD smoke evidence" in text
    assert "Meep / PyMeep version: 1.33.0" in text
    assert "External solver/package executed: yes, Meep only" in text
    assert "MPB executed: no" in text
    assert "Gmsh rerun in this task: no" in text
    assert "Optiland rerun in this task: no" in text
    assert "Elmer executed: no" in text
    assert "PyPI/TestPyPI upload: no" in text
    assert "Tag/release action: no" in text
    assert "Production-grade FDTD validation claimed: no" in text
    assert "does not authorize any further solver execution" in text
    assert "does not authorize MPB execution" in text
    assert "MPB approval must remain separate from Meep" in text
