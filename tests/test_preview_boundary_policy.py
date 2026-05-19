"""Preview boundary policy documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_preview_boundary_policy_docs_cover_all_boundaries():
    en = ROOT / "docs" / "preview_boundary_policy.md"
    zh = ROOT / "docs" / "preview_boundary_policy.zh-CN.md"
    assert en.exists()
    assert zh.exists()
    text = en.read_text(encoding="utf-8")
    zh_text = zh.read_text(encoding="utf-8")
    for phrase in [
        "Materials",
        "Calculators",
        "Application domains",
        "Source/monitor models",
        "Adapter mappings",
        "PyPI publication",
        "would not imply production-grade physical",
        "No production-grade physical validation is claimed",
        "No formal convergence proof is claimed",
    ]:
        assert phrase in text
    assert "Materials" in zh_text
    assert "Calculators" in zh_text
    assert "Adapter mappings" in zh_text
    assert "不代表生产级物理验证" in zh_text

