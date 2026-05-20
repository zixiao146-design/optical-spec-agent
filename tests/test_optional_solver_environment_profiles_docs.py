"""Optional solver environment profile documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optional_solver_environment_profiles_docs_exist_and_bound_execution():
    paths = [
        ROOT / "docs" / "optional_solver_environment_profiles.md",
        ROOT / "docs" / "optional_solver_environment_profiles.zh-CN.md",
    ]
    for path in paths:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "OSA_SOLVER_PYTHON" in text
        assert "OSA_SOLVER_READINESS_PROFILE" in text
        assert "osa-solvers" in text
        assert "current" in text
        assert "homebrew-cli" in text
        assert "deferred-elmer" in text
        assert "meep.mpb" in text
        assert "Gmsh" in text
        assert "Elmer" in text
        assert "no solver execution" in text.lower() or "不会执行 solver" in text
        assert "PyPI" in text
        assert "formal convergence" in text.lower() or "形式化收敛" in text
