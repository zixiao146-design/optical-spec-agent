from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_example_gallery_docs_exist_and_list_example_families():
    for doc in ("example_gallery.md", "example_gallery.zh-CN.md"):
        path = ROOT / "docs" / doc
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        for example_id in [
            "nanoparticle_plasmonics",
            "thin_film_coating",
            "waveguide_mode",
            "photonic_crystal_band",
            "dielectric_metasurface_preview",
            "lens_raytrace_preview",
        ]:
            assert example_id in text
        assert "No solver" in text or "默认不执行外部求解器" in text
        assert "production-grade" in text or "生产级" in text
