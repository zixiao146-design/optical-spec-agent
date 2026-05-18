"""Preview Gaussian beam design helpers."""

from __future__ import annotations

import math

from .models import CalculatorQuality, CalculatorResult


def _gaussian_quality(
    *,
    reference_case: str | None = None,
    assumptions: list[str] | None = None,
    warnings: list[str] | None = None,
) -> CalculatorQuality:
    return CalculatorQuality(
        reference_case=reference_case,
        assumptions=assumptions
        or [
            "Ideal fundamental Gaussian beam.",
            "Paraxial approximation.",
        ],
        limitations=[
            "Scalar Gaussian beam preview only.",
            "Aberrations, truncation, M^2, aperture clipping, and non-vacuum media are not included unless noted.",
            "Not production-grade physical validation.",
        ],
        warnings=warnings or ["Paraxial approximation should be checked for high-NA systems."],
        valid_input_range={
            "wavelength_nm": "positive",
            "waist_um": "positive",
            "z_mm": "finite real preview distance",
        },
    )


def gaussian_beam_parameters(wavelength_nm: float, waist_um: float) -> CalculatorResult:
    if wavelength_nm <= 0 or waist_um <= 0:
        raise ValueError("wavelength_nm and waist_um must be positive.")
    wavelength_um = wavelength_nm / 1000.0
    rayleigh_range_um = math.pi * waist_um**2 / wavelength_um
    assumptions = [
        "Ideal fundamental Gaussian beam.",
        "Paraxial approximation.",
        "Rayleigh range formula z_R = pi * w0^2 / lambda.",
    ]
    warnings = ["Paraxial approximation should be checked for high-NA systems."]
    return CalculatorResult(
        result={
            "wavelength_nm": wavelength_nm,
            "waist_um": waist_um,
            "rayleigh_range_mm": rayleigh_range_um / 1000.0,
            "divergence_half_angle_rad": wavelength_um / (math.pi * waist_um),
        },
        assumptions=assumptions,
        warnings=warnings,
        quality=_gaussian_quality(
            reference_case="gaussian_rayleigh_range_formula",
            assumptions=assumptions,
            warnings=warnings,
        ),
    )


def propagate_gaussian_beam(wavelength_nm: float, waist_um: float, z_mm: float) -> CalculatorResult:
    params = gaussian_beam_parameters(wavelength_nm, waist_um)
    wavelength_um = wavelength_nm / 1000.0
    z_um = z_mm * 1000.0
    rayleigh_range_um = params.result["rayleigh_range_mm"] * 1000.0
    ratio = z_um / rayleigh_range_um
    beam_radius_um = waist_um * math.sqrt(1 + ratio**2)
    radius_of_curvature_mm = None
    if abs(z_um) > 1e-12:
        radius_of_curvature_mm = (z_um * (1 + (rayleigh_range_um / z_um) ** 2)) / 1000.0
    assumptions = [
        "Ideal fundamental Gaussian beam.",
        "Paraxial approximation.",
        "Medium refractive index is assumed to be 1.0.",
        "Beam radius formula w(z) = w0 * sqrt(1 + (z/z_R)^2).",
    ]
    warnings = ["Paraxial approximation should be checked for high-NA systems."]
    reference_case = "gaussian_beam_radius_at_waist" if abs(z_mm) < 1e-12 else None
    if abs(abs(z_um) - rayleigh_range_um) / rayleigh_range_um < 1e-9:
        reference_case = "gaussian_beam_radius_at_rayleigh_range"
    return CalculatorResult(
        result={
            **params.result,
            "z_mm": z_mm,
            "beam_radius_um": beam_radius_um,
            "radius_of_curvature_mm": radius_of_curvature_mm,
            "gouy_phase_rad": math.atan(ratio),
        },
        assumptions=assumptions,
        warnings=warnings,
        quality=_gaussian_quality(
            reference_case=reference_case,
            assumptions=assumptions,
            warnings=warnings,
        ),
    )


def _linspace(start: float, stop: float, points: int) -> list[float]:
    if points < 2:
        raise ValueError("points must be at least 2.")
    if stop <= start:
        raise ValueError("z_stop_mm must be greater than z_start_mm.")
    step = (stop - start) / (points - 1)
    return [start + index * step for index in range(points)]


def propagate_gaussian_beam_series(
    wavelength_nm: float,
    waist_um: float,
    z_start_mm: float,
    z_stop_mm: float,
    points: int,
) -> CalculatorResult:
    """Preview Gaussian beam propagation over a z range."""

    z_values = _linspace(z_start_mm, z_stop_mm, points)
    samples = []
    max_radius = 0.0
    for z_mm in z_values:
        result = propagate_gaussian_beam(wavelength_nm, waist_um, z_mm)
        beam_radius = float(result.result["beam_radius_um"])
        max_radius = max(max_radius, beam_radius)
        samples.append(
            {
                "z_mm": z_mm,
                "beam_radius_um": beam_radius,
                "radius_of_curvature_mm": result.result["radius_of_curvature_mm"],
                "gouy_phase_rad": result.result["gouy_phase_rad"],
            }
        )
    params = gaussian_beam_parameters(wavelength_nm, waist_um)
    assumptions = [
        "Ideal fundamental Gaussian beam.",
        "Paraxial approximation.",
        "Medium refractive index is assumed to be 1.0.",
    ]
    warnings = ["Paraxial approximation should be checked for high-NA systems."]
    return CalculatorResult(
        result={
            "samples": samples,
            "sample_count": len(samples),
            "wavelength_nm": wavelength_nm,
            "waist_um": waist_um,
            "rayleigh_range_mm": params.result["rayleigh_range_mm"],
            "max_beam_radius_um": max_radius,
            "summary": (
                f"Gaussian beam preview sampled {len(samples)} points from "
                f"{z_start_mm} mm to {z_stop_mm} mm."
            ),
        },
        assumptions=assumptions,
        warnings=warnings,
        quality=_gaussian_quality(
            reference_case="gaussian_beam_series_preview",
            assumptions=assumptions,
            warnings=warnings,
        ),
    )


def focus_gaussian_beam_thin_lens(
    wavelength_nm: float,
    input_waist_um: float,
    focal_length_mm: float,
) -> CalculatorResult:
    """Preview diffraction-limited focus from a collimated Gaussian beam."""

    if wavelength_nm <= 0 or input_waist_um <= 0:
        raise ValueError("wavelength_nm and input_waist_um must be positive.")
    if focal_length_mm <= 0:
        raise ValueError("focal_length_mm must be positive.")
    wavelength_um = wavelength_nm / 1000.0
    focal_length_um = focal_length_mm * 1000.0
    focused_waist_um = wavelength_um * focal_length_um / (math.pi * input_waist_um)
    focused_params = gaussian_beam_parameters(wavelength_nm, focused_waist_um)
    input_params = gaussian_beam_parameters(wavelength_nm, input_waist_um)
    assumptions = [
        "Collimated Gaussian beam at a thin lens.",
        "Diffraction-limited paraxial focus estimate.",
        "Approximate focus formula w_f = lambda * f / (pi * w_in).",
        "Aberrations, truncation, M^2, and aperture clipping are not included.",
    ]
    warnings = ["High-NA focusing requires a vector diffraction model, not this preview estimate."]
    return CalculatorResult(
        result={
            "wavelength_nm": wavelength_nm,
            "input_waist_um": input_waist_um,
            "focal_length_mm": focal_length_mm,
            "approx_focused_waist_um": focused_waist_um,
            "focused_rayleigh_range_mm": focused_params.result["rayleigh_range_mm"],
            "input_rayleigh_range_mm": input_params.result["rayleigh_range_mm"],
            "summary": (
                f"Thin-lens Gaussian focus preview estimates waist "
                f"{focused_waist_um:.3f} um."
            ),
        },
        assumptions=assumptions,
        warnings=warnings,
        quality=_gaussian_quality(
            reference_case="gaussian_thin_lens_focus_preview",
            assumptions=assumptions,
            warnings=warnings,
        ),
    )
