"""rc8 backend readiness review documentation guards."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_rc8_backend_readiness_review_docs_are_conservative():
    en = ROOT / "docs" / "rc8_backend_readiness_review.md"
    zh = ROOT / "docs" / "rc8_backend_readiness_review.zh-CN.md"
    assert en.exists()
    assert zh.exists()

    en_text = en.read_text(encoding="utf-8")
    zh_text = zh.read_text(encoding="utf-8")
    combined = en_text + "\n" + zh_text

    assert "Gmsh, Optiland, Meep, and MPB" in en_text
    assert "Gmsh、Optiland、Meep、MPB" in zh_text
    assert "Application domain benchmarks: 19 pass / 0 warn / 0 fail" in combined
    assert "PyPI: not published" in combined
    assert "TestPyPI: only `0.9.0rc6.dev0` uploaded and verified" in en_text
    assert "does not authorize PyPI publication" in en_text
    assert "v0.9.0rc9 tag" in en_text
    assert "does not authorize" in en_text
    assert "PyPI publication remains a separate maintainer decision" in en_text
    assert "Elmer: deferred, not Level 3, not executed" in combined
    assert "production-grade validation" in combined
    assert "formal convergence proof" in combined
    assert "optical correctness" in combined
