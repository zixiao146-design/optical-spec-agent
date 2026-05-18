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
        assert "quarter-wave" in text or "四分之一波长" in text
        assert "Gaussian" in text or "高斯" in text
        assert "two-lens" in text or "双透镜" in text
        assert "waveguide" in text or "波导" in text
        assert "sanity_checked_preview" in text
        assert "reference" in text or "参考" in text
        assert "production-grade" in text or "生产级" in text
        assert "No external solver" in text or "默认不执行外部求解器" in text


def test_optics_calculator_examples_exist_and_are_safe():
    examples_dir = ROOT / "examples" / "optics_calculators"
    assert (examples_dir / "README.md").exists()
    for filename in [
        "thin_film_ar_coating.json",
        "thin_film_spectrum_ar_coating.json",
        "quarter_wave_ar_design.json",
        "paraxial_lens_imaging.json",
        "paraxial_two_lens_relay.json",
        "gaussian_beam_propagation.json",
        "gaussian_beam_series.json",
        "gaussian_beam_focus.json",
        "slab_waveguide_v_number.json",
        "waveguide_sweep.json",
        "waveguide_single_mode_range.json",
    ]:
        text = (examples_dir / filename).read_text(encoding="utf-8")
        assert "external_solver_executed" in text
        assert "production_grade_validation_claimed" in text
