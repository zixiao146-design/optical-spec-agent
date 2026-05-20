"""Docs tests for optional solver execution sequencing."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optional_solver_execution_sequence_docs_define_order_and_stops():
    en = ROOT / "docs" / "optional_solver_execution_sequence.md"
    zh = ROOT / "docs" / "optional_solver_execution_sequence.zh-CN.md"
    assert en.exists()
    assert zh.exists()
    text = en.read_text(encoding="utf-8")
    assert "Gmsh first" in text
    assert "Optiland second" in text
    assert "Meep third" in text
    assert "MPB fourth" in text
    assert "Elmer deferred" in text
    assert "OSA_SOLVER_PYTHON" in text
    assert "Stop Conditions" in text
    assert "Do not batch all solvers without separate approval" in text
    assert "not Level 3" in text
    zh_text = zh.read_text(encoding="utf-8")
    assert "Gmsh first" in zh_text
    assert "Optiland second" in zh_text
    assert "OSA_SOLVER_PYTHON" in zh_text
    assert "Elmer deferred" in zh_text
