"""Adapter-native source/monitor mapping documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_adapter_native_mapping_docs_exist_and_cover_all_adapters():
    for doc_name in [
        "adapter_native_source_monitor_mapping.md",
        "adapter_native_source_monitor_mapping.zh-CN.md",
    ]:
        path = ROOT / "docs" / doc_name
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        for adapter in ["Meep", "MPB", "Gmsh", "Elmer", "Optiland"]:
            assert adapter in text
        assert "preview" in text.lower() or "预览" in text
        assert "solver" in text.lower() or "求解器" in text
        assert "No production-grade physical validation" in text or "不声明生产级物理验证" in text
        assert "No formal convergence proof" in text or "不声明形式化收敛证明" in text
