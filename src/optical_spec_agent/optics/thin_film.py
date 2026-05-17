"""Preview thin-film stack calculator."""

from __future__ import annotations

import cmath
import math
from typing import Any

from .models import CalculatorResult, ThinFilmLayer


def _matmul(a: tuple[complex, complex, complex, complex], b: tuple[complex, complex, complex, complex]) -> tuple[complex, complex, complex, complex]:
    return (
        a[0] * b[0] + a[1] * b[2],
        a[0] * b[1] + a[1] * b[3],
        a[2] * b[0] + a[3] * b[2],
        a[2] * b[1] + a[3] * b[3],
    )


def calculate_thin_film_stack(
    layers: list[dict[str, Any] | ThinFilmLayer],
    wavelength_nm: float,
    *,
    incident_n: float = 1.0,
    substrate_n: float = 1.5,
    incidence_angle_deg: float = 0.0,
    polarization: str = "s",
) -> CalculatorResult:
    """Estimate normal/near-normal thin-film reflectance with a transfer matrix.

    The implementation intentionally uses a compact preview model. Oblique
    incidence and polarization are recorded as assumptions unless the angle is
    near normal.
    """

    if wavelength_nm <= 0:
        raise ValueError("wavelength_nm must be positive.")
    parsed_layers = [
        layer if isinstance(layer, ThinFilmLayer) else ThinFilmLayer.model_validate(layer)
        for layer in layers
    ]
    if any(layer.thickness_nm < 0 for layer in parsed_layers):
        raise ValueError("Layer thickness must be non-negative.")
    angle = abs(incidence_angle_deg)
    assumptions = [
        "Coherent planar stack preview.",
        "Material n/k values are caller-provided preview values.",
        "Normal-incidence transfer matrix is used for the numerical estimate.",
    ]
    diagnostics: list[str] = []
    if angle > 1e-6:
        diagnostics.append(
            f"incidence_angle_deg={incidence_angle_deg} recorded, but preview calculation uses normal incidence."
        )
    if polarization.lower() not in {"s", "p"}:
        diagnostics.append(f"Unknown polarization '{polarization}', treated as preview metadata only.")

    matrix = (1 + 0j, 0 + 0j, 0 + 0j, 1 + 0j)
    for layer in parsed_layers:
        n_complex = complex(layer.n, layer.k)
        delta = 2 * math.pi * n_complex * layer.thickness_nm / wavelength_nm
        cos_delta = cmath.cos(delta)
        sin_delta = cmath.sin(delta)
        eta = n_complex
        layer_matrix = (
            cos_delta,
            1j * sin_delta / eta,
            1j * eta * sin_delta,
            cos_delta,
        )
        matrix = _matmul(matrix, layer_matrix)

    eta0 = complex(incident_n, 0.0)
    etas = complex(substrate_n, 0.0)
    b_term = matrix[0] + matrix[1] * etas
    c_term = matrix[2] + matrix[3] * etas
    denominator = eta0 * b_term + c_term
    if abs(denominator) == 0:
        raise ValueError("Degenerate thin-film matrix denominator.")
    reflection = (eta0 * b_term - c_term) / denominator
    transmission = 2 * eta0 / denominator
    reflectance = max(0.0, min(1.0, abs(reflection) ** 2))
    transmittance_raw = (etas.real / eta0.real) * abs(transmission) ** 2 if eta0.real else 0.0
    transmittance = max(0.0, min(1.0, transmittance_raw))
    absorptance = max(0.0, min(1.0, 1.0 - reflectance - transmittance))

    return CalculatorResult(
        result={
            "reflectance": reflectance,
            "transmittance": transmittance,
            "absorptance_estimate": absorptance,
            "wavelength_nm": wavelength_nm,
            "incident_n": incident_n,
            "substrate_n": substrate_n,
            "layer_count": len(parsed_layers),
        },
        assumptions=assumptions,
        diagnostics=diagnostics,
    )
