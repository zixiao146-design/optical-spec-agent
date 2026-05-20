"""Optional solver readiness status documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optional_solver_readiness_status_records_current_boundaries():
    path = ROOT / "docs" / "optional_solver_micro_benchmark_readiness_status.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Current public prerelease: v0.9.0rc7" in text
    assert "Current main development version: 0.9.0rc8.dev0" in text
    assert "v0.9.0rc8 tag: absent" in text
    assert "Solver micro-benchmark default mode: no execution" in text
    assert "Elmer | deferred" in text
    assert "explicit" in text.lower()
    assert "No PyPI upload" in text
    assert "TestPyPI upload" in text
