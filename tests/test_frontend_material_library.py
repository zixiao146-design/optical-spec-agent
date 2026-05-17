from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend" / "src"


def test_frontend_material_library_page_exists_and_keeps_preview_claims():
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in FRONTEND.rglob("*")
        if path.suffix in {".ts", ".tsx"}
    )
    assert (FRONTEND / "pages" / "MaterialLibraryPage.tsx").exists()
    assert "Material Library" in source
    assert "材料库" in source
    assert "/api/materials" in source
    assert "/api/materials/suggest" in source
    assert "not production-grade optical constants" in source
    assert "不声明生产级材料常数" in source
    assert "Upload to PyPI" not in source
    assert "Create release" not in source
