"""Backend validation maturity documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_backend_validation_maturity_docs_exist_and_bound_claims():
    en = ROOT / "docs" / "backend_validation_maturity_matrix.md"
    zh = ROOT / "docs" / "backend_validation_maturity_matrix.zh-CN.md"
    assert en.exists()
    assert zh.exists()
    text = en.read_text(encoding="utf-8")
    zh_text = zh.read_text(encoding="utf-8")
    for phrase in [
        "documented_preview",
        "fixture_guarded_preview",
        "sanity_checked_preview",
        "benchmark_checked_preview",
        "production_grade_not_claimed",
        "No production-grade physical validation is claimed",
        "No formal convergence proof is claimed",
        "No real solver monitor result is claimed by default",
    ]:
        assert phrase in text
    assert "sanity_checked_preview" in zh_text
    assert "不声称生产级物理验证" in zh_text
    assert "不声称形式化收敛证明" in zh_text

