"""Optional solver readiness status documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optional_solver_readiness_status_records_current_boundaries():
    path = ROOT / "docs" / "optional_solver_micro_benchmark_readiness_status.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Current public prerelease: v0.9.0rc8" in text
    assert "Current main development version: 0.9.0rc9.dev0" in text
    assert "v0.9.0rc9 tag: absent" in text
    assert "Solver micro-benchmark default mode: no execution" in text
    assert "optional_solver_micro_benchmark_execution_packet.md" in text
    assert "optional_solver_approval_records/" in text
    assert "Gmsh-only optional micro-benchmark on 2026-05-20" in text
    assert "accepted it as optional manual mesh-generation smoke evidence" in text
    assert "Optiland-only optional micro-benchmark passed on 2026-05-20" in text
    assert "accepted the Optiland result as optional manual ray/path" in text
    assert "validation/optiland/optiland_micro_benchmark_2026-05-20.md" in text
    assert "validation/gmsh/gmsh_micro_benchmark_2026-05-20.md" in text
    assert "gmsh_micro_benchmark_review_2026-05-20.md" in text
    assert "optiland_micro_benchmark_review_2026-05-20.md" in text
    assert "meep_micro_benchmark_decision_packet.md" in text
    assert "mpb_micro_benchmark_decision_packet.md" in text
    assert "meep_micro_benchmark_review_2026-05-20.md" in text
    assert "validation/meep/meep_micro_benchmark_2026-05-20.md" in text
    assert "approved Meep-only optional micro-benchmark" in text
    assert "accepted the Meep result as optional manual PyMeep/FDTD" in text
    assert "future Meep runs require fresh approval" in text
    assert "MPB | Executed/passed for the approved MPB-only optional micro-benchmark on 2026-05-20" in text
    assert "validation/mpb/mpb_micro_benchmark_2026-05-20.md" in text
    assert "mpb_micro_benchmark_approval_2026-05-20.md" in text
    assert "MPB CLI is not required if the Python path is available" in text
    assert "optional manual MPB/band-structure smoke" in text
    assert "future MPB runs require fresh approval" in text
    assert "Elmer | deferred" in text
    assert "Meep and `meep.mpb` are detectable" in text
    assert "explicit" in text.lower()
    assert "OSA_SOLVER_PYTHON" in text
    assert "OSA_SOLVER_READINESS_PROFILE=osa-solvers" in text
    assert "meep.mpb" in text
    assert "optional_solver_environment_profiles.md" in text
    assert "No PyPI upload" in text
    assert "TestPyPI upload" in text
