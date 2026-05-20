"""Optional solver approval matrix documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optional_solver_approval_matrix_docs_exist_and_bound_execution():
    paths = [
        ROOT / "docs" / "optional_solver_micro_benchmark_approval_matrix.md",
        ROOT / "docs" / "optional_solver_micro_benchmark_approval_matrix.zh-CN.md",
    ]
    for path in paths:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        for solver in ["Gmsh", "Meep", "MPB", "Optiland", "Elmer"]:
            assert solver in text
        assert "explicit approval" in text.lower() or "明确批准" in text
        assert "Default execution" in text or "默认执行" in text
        assert "no" in text.lower()
        assert "production-grade physical validation" in text or "生产级物理验证" in text
        assert "formal convergence" in text.lower() or "形式化收敛" in text
        assert "PyPI/TestPyPI" in text
        assert "Elmer remains deferred" in text or "Elmer 仍是" in text

