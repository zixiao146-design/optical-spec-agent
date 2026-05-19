"""Optional solver micro-benchmark documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_solver_validation_micro_benchmark_docs_exist_and_bound_claims():
    en = ROOT / "docs" / "solver_validation_micro_benchmarks.md"
    zh = ROOT / "docs" / "solver_validation_micro_benchmarks.zh-CN.md"
    for path in [en, zh]:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "OSA_RUN_OPTIONAL_GMSH_VALIDATION=1" in text
        assert "OSA_RUN_OPTIONAL_MEEP_VALIDATION=1" in text
        assert "OSA_RUN_OPTIONAL_MPB_VALIDATION=1" in text
        assert "OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1" in text
        assert "Elmer" in text
        assert "deferred" in text
        assert "production-grade" in text
        assert "formal convergence" in text or "形式化收敛" in text
        assert "default" in text.lower()
