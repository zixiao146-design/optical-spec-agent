"""Adapter-native golden documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_adapter_native_golden_docs_exist_and_document_five_cases():
    for relative in [
        "docs/adapter_native_golden_cases.md",
        "docs/adapter_native_golden_cases.zh-CN.md",
        "docs/adapter_native_golden_coverage_matrix.md",
        "docs/adapter_native_golden_coverage_matrix.zh-CN.md",
    ]:
        path = ROOT / relative
        assert path.exists(), relative
        text = path.read_text(encoding="utf-8")
        for phrase in [
            "meep_nanoparticle_scattering",
            "mpb_photonic_crystal_band",
            "gmsh_mesh_region",
            "elmer_fem_boundary_source",
            "optiland_lens_image_plane",
            "preview",
        ]:
            assert phrase in text
        assert (
            "No production-grade physical validation" in text
            or "不声明生产级物理验证" in text
        )
        assert "No formal convergence proof" in text or "不声明形式化收敛证明" in text
        assert "scripts/check_adapter_native_golden.py" in text
