"""Preview waveguide design estimates."""

from __future__ import annotations

import math

from .models import CalculatorQuality, CalculatorResult


def _waveguide_quality(
    *,
    reference_case: str | None = None,
    assumptions: list[str] | None = None,
    warnings: list[str] | None = None,
) -> CalculatorQuality:
    return CalculatorQuality(
        reference_case=reference_case,
        assumptions=assumptions
        or [
            "Symmetric slab-waveguide scalar V-number preview.",
            "Single-mode threshold uses V < pi as a design-assist convention.",
        ],
        limitations=[
            "Does not solve vector eigenmodes.",
            "Does not account for ridge geometry, asymmetric claddings, leakage, or material dispersion.",
            "Not production-grade physical validation.",
        ],
        warnings=warnings or ["Use a validated mode solver before physical conclusions."],
        valid_input_range={
            "wavelength_nm": "positive",
            "core_thickness_um": "positive",
            "core_n": "greater than cladding_n",
            "cladding_n": "positive",
        },
    )


def slab_waveguide_v_number(
    core_n: float,
    cladding_n: float,
    core_thickness_um: float,
    wavelength_nm: float,
) -> CalculatorResult:
    if wavelength_nm <= 0 or core_thickness_um <= 0:
        raise ValueError("wavelength_nm and core_thickness_um must be positive.")
    if core_n <= 0 or cladding_n <= 0:
        raise ValueError("core_n and cladding_n must be positive.")
    if core_n <= cladding_n:
        raise ValueError("core_n must be greater than cladding_n for a guided slab preview.")
    wavelength_um = wavelength_nm / 1000.0
    numerical_aperture = math.sqrt(core_n**2 - cladding_n**2)
    v_number = (2 * math.pi * core_thickness_um / wavelength_um) * numerical_aperture
    assumptions = [
        "Symmetric slab-waveguide preview.",
        "Uses scalar V-number formula V = (2*pi/lambda) * thickness * sqrt(n_core^2 - n_clad^2).",
        "Single-mode likely means V < pi in this preview convention.",
        "Does not solve vector eigenmodes.",
    ]
    warnings = ["Use MPB/Elmer or another validated mode solver for physical conclusions."]
    return CalculatorResult(
        result={
            "v_number": v_number,
            "single_mode_likely": single_mode_estimate(v_number),
            "core_n": core_n,
            "cladding_n": cladding_n,
            "core_thickness_um": core_thickness_um,
            "wavelength_nm": wavelength_nm,
        },
        assumptions=assumptions,
        diagnostics=warnings,
        warnings=warnings,
        quality=_waveguide_quality(
            reference_case="slab_waveguide_v_number_formula",
            assumptions=assumptions,
            warnings=warnings,
        ),
    )


def single_mode_estimate(v_number: float) -> bool:
    """Return a conservative scalar slab single-mode orientation."""

    return 0 <= v_number < math.pi


def _linspace(start: float, stop: float, points: int) -> list[float]:
    if points < 2:
        raise ValueError("points must be at least 2.")
    if stop <= start:
        raise ValueError("thickness_stop_um must be greater than thickness_start_um.")
    step = (stop - start) / (points - 1)
    return [start + index * step for index in range(points)]


def slab_waveguide_sweep(
    core_n: float,
    cladding_n: float,
    wavelength_nm: float,
    thickness_start_um: float,
    thickness_stop_um: float,
    points: int,
) -> CalculatorResult:
    """Preview slab-waveguide V-number over a thickness range."""

    thicknesses = _linspace(thickness_start_um, thickness_stop_um, points)
    samples = []
    for thickness in thicknesses:
        estimate = slab_waveguide_v_number(core_n, cladding_n, thickness, wavelength_nm)
        samples.append(
            {
                "core_thickness_um": thickness,
                "v_number": estimate.result["v_number"],
                "single_mode_likely": estimate.result["single_mode_likely"],
            }
        )
    single_mode_samples = [sample for sample in samples if sample["single_mode_likely"]]
    assumptions = [
        "Symmetric slab-waveguide scalar V-number sweep.",
        "Single-mode likely means V < pi in this preview convention.",
        "Does not solve vector modes or account for ridge/asymmetric effects.",
    ]
    warnings = ["Use MPB/Elmer or another validated mode solver for physical conclusions."]
    return CalculatorResult(
        result={
            "samples": samples,
            "sample_count": len(samples),
            "single_mode_sample_count": len(single_mode_samples),
            "core_n": core_n,
            "cladding_n": cladding_n,
            "wavelength_nm": wavelength_nm,
            "summary": (
                f"Waveguide preview sampled {len(samples)} thickness values; "
                f"{len(single_mode_samples)} are single-mode likely by scalar V-number."
            ),
        },
        assumptions=assumptions,
        diagnostics=warnings,
        warnings=warnings,
        quality=_waveguide_quality(
            reference_case="slab_waveguide_v_number_sweep",
            assumptions=assumptions,
            warnings=warnings,
        ),
    )


def suggest_single_mode_thickness_range(
    core_n: float,
    cladding_n: float,
    wavelength_nm: float,
) -> CalculatorResult:
    """Suggest a scalar slab thickness range for likely single-mode behavior."""

    if wavelength_nm <= 0:
        raise ValueError("wavelength_nm must be positive.")
    if core_n <= 0 or cladding_n <= 0:
        raise ValueError("core_n and cladding_n must be positive.")
    if core_n <= cladding_n:
        raise ValueError("core_n must be greater than cladding_n for a guided slab preview.")
    wavelength_um = wavelength_nm / 1000.0
    numerical_aperture = math.sqrt(core_n**2 - cladding_n**2)
    max_single_mode_um = wavelength_um / (2 * numerical_aperture)
    lower_bound_um = max(max_single_mode_um * 0.1, 0.01)
    assumptions = [
        "Symmetric slab-waveguide scalar V-number estimate.",
        "Upper bound is from V < pi.",
        "Fabrication limits, vector modes, and asymmetric claddings are not included.",
    ]
    warnings = ["Treat this as a design starting point, not a mode-solver result."]
    return CalculatorResult(
        result={
            "core_n": core_n,
            "cladding_n": cladding_n,
            "wavelength_nm": wavelength_nm,
            "suggested_min_thickness_um": lower_bound_um,
            "suggested_max_thickness_um": max_single_mode_um,
            "cutoff_v_number": math.pi,
            "summary": (
                f"Scalar slab preview suggests thickness below "
                f"{max_single_mode_um:.3f} um for likely single-mode behavior."
            ),
        },
        assumptions=assumptions,
        diagnostics=warnings,
        warnings=warnings,
        quality=_waveguide_quality(
            reference_case="slab_waveguide_single_mode_range",
            assumptions=assumptions,
            warnings=warnings,
        ),
    )
