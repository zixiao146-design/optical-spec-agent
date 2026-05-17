"""Preview waveguide design estimates."""

from __future__ import annotations

import math

from .models import CalculatorResult


def slab_waveguide_v_number(
    core_n: float,
    cladding_n: float,
    core_thickness_um: float,
    wavelength_nm: float,
) -> CalculatorResult:
    if wavelength_nm <= 0 or core_thickness_um <= 0:
        raise ValueError("wavelength_nm and core_thickness_um must be positive.")
    if core_n <= cladding_n:
        raise ValueError("core_n must be greater than cladding_n for a guided slab preview.")
    wavelength_um = wavelength_nm / 1000.0
    numerical_aperture = math.sqrt(core_n**2 - cladding_n**2)
    v_number = (2 * math.pi * core_thickness_um / wavelength_um) * numerical_aperture
    return CalculatorResult(
        result={
            "v_number": v_number,
            "single_mode_likely": single_mode_estimate(v_number),
            "core_n": core_n,
            "cladding_n": cladding_n,
            "core_thickness_um": core_thickness_um,
            "wavelength_nm": wavelength_nm,
        },
        assumptions=[
            "Symmetric slab-waveguide preview.",
            "Uses scalar V-number orientation only.",
            "Does not solve vector eigenmodes.",
        ],
        diagnostics=[
            "Use MPB/Elmer or another validated mode solver for physical conclusions."
        ],
    )


def single_mode_estimate(v_number: float) -> bool:
    """Return a conservative scalar slab single-mode orientation."""

    return 0 <= v_number < math.pi
