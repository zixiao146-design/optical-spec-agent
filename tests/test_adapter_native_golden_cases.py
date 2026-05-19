"""Adapter-native golden case file tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = ROOT / "examples" / "adapter_native_golden"
CASES = [
    "meep_nanoparticle_scattering",
    "mpb_photonic_crystal_band",
    "gmsh_mesh_region",
    "elmer_fem_boundary_source",
    "optiland_lens_image_plane",
]
REQUIRED_FILES = [
    "request.json",
    "source_model.json",
    "monitor_model.json",
    "observable_diagnostics.json",
    "adapter_mapping.json",
    "expected_metadata.json",
    "expected_preview_fragments.txt",
    "README.md",
]


def test_adapter_native_golden_case_directories_have_required_files():
    for case in CASES:
        case_dir = CASE_ROOT / case
        assert case_dir.exists(), case
        for filename in REQUIRED_FILES:
            assert (case_dir / filename).exists(), f"{case}/{filename}"


def test_adapter_native_golden_expected_fragments_and_safety_copy():
    for case in CASES:
        case_dir = CASE_ROOT / case
        fragments = [
            line.strip()
            for line in (case_dir / "expected_preview_fragments.txt").read_text(
                encoding="utf-8"
            ).splitlines()
            if line.strip() and not line.startswith("#")
        ]
        assert fragments, case
        readme = (case_dir / "README.md").read_text(encoding="utf-8")
        assert "No solver execution is performed." in readme
        assert "No external LLM is called." in readme
        assert "preview/design-assist metadata only" in readme
        assert "No production-grade physical validation is claimed." in readme
        assert "No formal convergence proof is claimed." in readme
