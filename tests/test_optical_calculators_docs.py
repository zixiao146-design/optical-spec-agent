"""Optical calculator docs tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optical_calculator_docs_exist_and_document_limitations():
    for path in [
        ROOT / "docs" / "optical_calculators.md",
        ROOT / "docs" / "optical_calculators.zh-CN.md",
    ]:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "thin-film" in text or "薄膜" in text
        assert "Gaussian" in text or "高斯" in text
        assert "waveguide" in text or "波导" in text
        assert "production-grade" in text or "生产级" in text
        assert "No external solver" in text or "默认不执行外部求解器" in text


def test_optics_calculator_examples_exist_and_are_safe():
    examples_dir = ROOT / "examples" / "optics_calculators"
    assert (examples_dir / "README.md").exists()
    for filename in [
        "thin_film_ar_coating.json",
        "paraxial_lens_imaging.json",
        "gaussian_beam_propagation.json",
        "slab_waveguide_v_number.json",
    ]:
        text = (examples_dir / filename).read_text(encoding="utf-8")
        assert "external_solver_executed" in text
        assert "production_grade_validation_claimed" in text

