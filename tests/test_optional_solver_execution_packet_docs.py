"""Docs tests for optional solver execution approval packet."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optional_solver_execution_packet_docs_exist_and_are_conservative():
    en = ROOT / "docs" / "optional_solver_micro_benchmark_execution_packet.md"
    zh = ROOT / "docs" / "optional_solver_micro_benchmark_execution_packet.zh-CN.md"
    assert en.exists()
    assert zh.exists()
    text = en.read_text(encoding="utf-8")
    zh_text = zh.read_text(encoding="utf-8")
    combined = f"{text}\n{zh_text}"
    assert "one solver at a time" in text
    assert "Recommended Execution Order" in text
    assert "Gmsh first" in text
    assert "Optiland second" in text
    assert "Meep third" in text
    assert "MPB fourth" in text
    assert "Elmer deferred" in text
    assert "PyPI publication" in combined
    assert "TestPyPI upload" in combined
    assert "Tag or GitHub release creation" in text
    assert "not approve execution by itself" in text
    assert "no production-grade physical validation" in text
    assert "no formal convergence proof" in text

