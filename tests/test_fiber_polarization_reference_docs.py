"""Docs coverage for fiber/polarization reference sanity cases."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_fiber_polarization_reference_docs_exist_and_preserve_limits():
    docs = [
        ROOT / "docs" / "fiber_polarization_reference_cases.md",
        ROOT / "docs" / "fiber_polarization_reference_cases.zh-CN.md",
    ]
    for path in docs:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "fiber_gaussian_perfect_overlap" in text
        assert "jones_linear_polarizer_malus" in text
        assert "jones_quarter_waveplate_phase_preview" in text
        assert "preview/design-assist" in text
        assert "production-grade" in text or "生产级" in text
        assert "formal convergence" in text or "形式化收敛" in text
        assert "external solver" in text or "外部求解器" in text


def test_fiber_polarization_reference_example_files_exist():
    expected = [
        ROOT / "examples" / "optics_reference_cases" / "fiber_coupling" / "README.md",
        ROOT
        / "examples"
        / "optics_reference_cases"
        / "fiber_coupling"
        / "perfect_gaussian_match.json",
        ROOT
        / "examples"
        / "optics_reference_cases"
        / "fiber_coupling"
        / "gaussian_waist_mismatch.json",
        ROOT
        / "examples"
        / "optics_reference_cases"
        / "fiber_coupling"
        / "gaussian_offset_loss.json",
        ROOT
        / "examples"
        / "optics_reference_cases"
        / "fiber_coupling"
        / "gaussian_tilt_loss.json",
        ROOT / "examples" / "optics_reference_cases" / "polarization" / "README.md",
        ROOT
        / "examples"
        / "optics_reference_cases"
        / "polarization"
        / "linear_polarizer_malus.json",
        ROOT
        / "examples"
        / "optics_reference_cases"
        / "polarization"
        / "half_wave_plate_rotation.json",
        ROOT
        / "examples"
        / "optics_reference_cases"
        / "polarization"
        / "quarter_wave_plate_phase.json",
    ]
    for path in expected:
        assert path.exists()
