from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend" / "src"


def test_frontend_example_gallery_page_exists_and_is_safe():
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in FRONTEND.rglob("*")
        if path.suffix in {".ts", ".tsx"}
    )
    assert (FRONTEND / "pages" / "ExampleGalleryPage.tsx").exists()
    assert "Example Gallery" in source
    assert "示例库" in source
    assert "/api/examples" in source
    assert "getExampleAgentTrace" in source
    assert "Upload to PyPI" not in source
    assert "Upload to TestPyPI" not in source
    assert "Create tag" not in source
    assert "Create release" not in source
    assert "Run solver" not in source
