"""Optional solver evidence summary documentation guards."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optional_solver_evidence_summary_docs_exist_and_close_loop():
    en = ROOT / "docs" / "optional_solver_evidence_summary.md"
    zh = ROOT / "docs" / "optional_solver_evidence_summary.zh-CN.md"
    assert en.exists()
    assert zh.exists()

    en_text = en.read_text(encoding="utf-8")
    zh_text = zh.read_text(encoding="utf-8")
    combined = en_text + "\n" + zh_text

    for solver in ["Gmsh", "Optiland", "Meep", "MPB"]:
        assert solver in combined
    assert combined.count("executed / passed") >= 8
    assert combined.count("reviewed / accepted") >= 8
    assert "optional manual mesh-generation smoke evidence" in combined
    assert "optional manual ray/path smoke evidence" in combined
    assert "optional manual PyMeep/FDTD smoke evidence" in combined
    assert "optional manual MPB/band-structure smoke evidence" in combined
    assert "Elmer" in combined
    assert "not Level 3" in combined
    assert "deferred" in combined
    assert "No production-grade physical validation is claimed." in en_text
    assert "No production-grade solver validation is claimed." in en_text
    assert "No formal convergence proof is claimed." in en_text
    assert "No optical correctness claim is made." in en_text
    assert "No PyPI readiness decision is implied." in en_text
    assert "不声明 production-grade physical validation" in zh_text
    assert "不声明 formal convergence proof" in zh_text
    assert "不声明 optical correctness" in zh_text
