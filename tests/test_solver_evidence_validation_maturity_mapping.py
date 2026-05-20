"""Solver evidence to validation maturity mapping documentation guards."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_solver_evidence_validation_maturity_mapping_docs_are_conservative():
    en = ROOT / "docs" / "solver_evidence_validation_maturity_mapping.md"
    zh = ROOT / "docs" / "solver_evidence_validation_maturity_mapping.zh-CN.md"
    assert en.exists()
    assert zh.exists()

    en_text = en.read_text(encoding="utf-8")
    zh_text = zh.read_text(encoding="utf-8")
    combined = en_text + "\n" + zh_text

    assert "optional manual mesh-generation smoke evidence" in combined
    assert "optional manual ray/path smoke evidence" in combined
    assert "optional manual PyMeep/FDTD smoke evidence" in combined
    assert "optional manual MPB/band-structure smoke evidence" in combined
    assert "default dependency" in en_text
    assert "pytest, smoke, quality, or release gates" in en_text
    assert "No production-grade physical validation is claimed." in en_text
    assert "No production-grade solver validation is claimed." in en_text
    assert "No formal convergence proof is claimed." in en_text
    assert "No optical correctness claim is made." in en_text
    assert "Elmer remains deferred" in en_text
    assert "not Level 3" in combined
