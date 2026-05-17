from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_material_library_docs_exist_and_warn_about_preview_data():
    for relative in ["docs/material_library.md", "docs/material_library.zh-CN.md"]:
        path = ROOT / relative
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "preview" in text.lower() or "预览" in text
        assert "not a production-grade" in text or "not production-grade" in text or "不是生产级" in text
        assert "sio2" in text
        assert "au" in text
        assert "ag" in text
        assert "No external LLM" in text or "默认不调用外部 LLM" in text
