"""Preview Gaussian beam design helpers."""

from __future__ import annotations

import math

from .models import CalculatorResult


def gaussian_beam_parameters(wavelength_nm: float, waist_um: float) -> CalculatorResult:
    if wavelength_nm <= 0 or waist_um <= 0:
        raise ValueError("wavelength_nm and waist_um must be positive.")
    wavelength_um = wavelength_nm / 1000.0
    rayleigh_range_um = math.pi * waist_um**2 / wavelength_um
    return CalculatorResult(
        result={
            "wavelength_nm": wavelength_nm,
            "waist_um": waist_um,
            "rayleigh_range_mm": rayleigh_range_um / 1000.0,
            "divergence_half_angle_rad": wavelength_um / (math.pi * waist_um),
        },
        assumptions=[
            "Ideal fundamental Gaussian beam.",
            "Paraxial approximation.",
        ],
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
    return CalculatorResult(
        result={
            **params.result,
            "z_mm": z_mm,
            "beam_radius_um": beam_radius_um,
            "radius_of_curvature_mm": radius_of_curvature_mm,
            "gouy_phase_rad": math.atan(ratio),
        },
        assumptions=[
            "Ideal fundamental Gaussian beam.",
            "Paraxial approximation.",
            "Medium refractive index is assumed to be 1.0.",
        ],
    )
