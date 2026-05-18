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


def _linspace(start: float, stop: float, points: int) -> list[float]:
    if points < 2:
        raise ValueError("points must be at least 2.")
    if stop <= start:
        raise ValueError("stop value must be greater than start value.")
    step = (stop - start) / (points - 1)
    return [start + index * step for index in range(points)]


def calculate_thin_film_spectrum(
    layers: list[dict[str, Any] | ThinFilmLayer],
    wavelength_start_nm: float,
    wavelength_stop_nm: float,
    points: int,
    *,
    incident_n: float = 1.0,
    substrate_n: float = 1.5,
    incidence_angle_deg: float = 0.0,
    polarization: str = "s",
) -> CalculatorResult:
    """Preview a wavelength sweep for a thin-film stack."""

    wavelengths = _linspace(wavelength_start_nm, wavelength_stop_nm, points)
    samples: list[dict[str, float]] = []
    diagnostics: list[str] = []
    assumptions = [
        "Wavelength sweep reuses the normal-incidence preview transfer matrix at each point.",
        "Material dispersion is not modeled unless caller changes n/k externally.",
        "Use this as design-assist orientation only.",
    ]
    min_reflectance = 1.0
    min_wavelength = wavelengths[0]
    for wavelength in wavelengths:
        result = calculate_thin_film_stack(
            layers,
            wavelength,
            incident_n=incident_n,
            substrate_n=substrate_n,
            incidence_angle_deg=incidence_angle_deg,
            polarization=polarization,
        )
        diagnostics.extend(item for item in result.diagnostics if item not in diagnostics)
        reflectance = float(result.result["reflectance"])
        transmittance = float(result.result["transmittance"])
        absorptance = float(result.result["absorptance_estimate"])
        if reflectance < min_reflectance:
            min_reflectance = reflectance
            min_wavelength = wavelength
        samples.append(
            {
                "wavelength_nm": wavelength,
                "reflectance": reflectance,
                "transmittance": transmittance,
                "absorptance_estimate": absorptance,
            }
        )

    return CalculatorResult(
        result={
            "samples": samples,
            "sample_count": len(samples),
            "wavelength_start_nm": wavelength_start_nm,
            "wavelength_stop_nm": wavelength_stop_nm,
            "minimum_reflectance": min_reflectance,
            "minimum_reflectance_wavelength_nm": min_wavelength,
            "incident_n": incident_n,
            "substrate_n": substrate_n,
            "layer_count": len(layers),
            "summary": (
                f"Preview sweep found minimum reflectance {min_reflectance:.4f} "
                f"near {min_wavelength:.1f} nm."
            ),
        },
        assumptions=assumptions,
        diagnostics=diagnostics,
    )


def design_quarter_wave_ar_coating(
    substrate_n: float,
    target_wavelength_nm: float,
    *,
    incident_n: float = 1.0,
    coating_n: float | None = None,
) -> CalculatorResult:
    """Return a simple quarter-wave anti-reflection coating preview."""

    if substrate_n <= 0 or incident_n <= 0:
        raise ValueError("incident_n and substrate_n must be positive.")
    if target_wavelength_nm <= 0:
        raise ValueError("target_wavelength_nm must be positive.")
    ideal_n = math.sqrt(incident_n * substrate_n)
    selected_n = coating_n or ideal_n
    if selected_n <= 0:
        raise ValueError("coating_n must be positive when provided.")
    thickness_nm = target_wavelength_nm / (4 * selected_n)
    coating = {"n": selected_n, "k": 0.0, "thickness_nm": thickness_nm}
    stack = calculate_thin_film_stack(
        [coating],
        target_wavelength_nm,
        incident_n=incident_n,
        substrate_n=substrate_n,
    )
    diagnostics = list(stack.diagnostics)
    if coating_n is not None and abs(coating_n - ideal_n) / ideal_n > 0.05:
        diagnostics.append(
            "Provided coating_n differs from the ideal sqrt(incident_n * substrate_n) by more than 5%."
        )
    return CalculatorResult(
        result={
            "incident_n": incident_n,
            "substrate_n": substrate_n,
            "ideal_coating_n": ideal_n,
            "selected_coating_n": selected_n,
            "target_wavelength_nm": target_wavelength_nm,
            "quarter_wave_thickness_nm": thickness_nm,
            "coating_layer": coating,
            "estimated_target_reflectance": stack.result["reflectance"],
            "summary": (
                f"Quarter-wave AR preview: n={selected_n:.3f}, "
                f"thickness={thickness_nm:.2f} nm at {target_wavelength_nm:.1f} nm."
            ),
        },
        assumptions=[
            "Single-layer quarter-wave AR design at normal incidence.",
            "Coating material is treated as lossless unless caller later supplies k.",
            "Substrate and incident media are non-dispersive preview indices.",
        ],
        diagnostics=diagnostics,
    )


def summarize_thin_film_result(result: CalculatorResult) -> dict[str, Any]:
    """Create a compact human-readable summary payload for thin-film results."""

    payload = result.result
    if "samples" in payload:
        return {
            "summary": payload.get("summary", "Thin-film spectrum preview generated."),
            "sample_count": payload.get("sample_count"),
            "minimum_reflectance": payload.get("minimum_reflectance"),
            "minimum_reflectance_wavelength_nm": payload.get("minimum_reflectance_wavelength_nm"),
            "assumption_count": len(result.assumptions),
            "diagnostic_count": len(result.diagnostics),
        }
    if "quarter_wave_thickness_nm" in payload:
        return {
            "summary": payload.get("summary", "Quarter-wave AR preview generated."),
            "quarter_wave_thickness_nm": payload.get("quarter_wave_thickness_nm"),
            "selected_coating_n": payload.get("selected_coating_n"),
            "estimated_target_reflectance": payload.get("estimated_target_reflectance"),
            "assumption_count": len(result.assumptions),
            "diagnostic_count": len(result.diagnostics),
        }
    return {
        "summary": (
            f"Thin-film preview at {payload.get('wavelength_nm')} nm: "
            f"R={payload.get('reflectance')}, T={payload.get('transmittance')}."
        ),
        "reflectance": payload.get("reflectance"),
        "transmittance": payload.get("transmittance"),
        "absorptance_estimate": payload.get("absorptance_estimate"),
        "assumption_count": len(result.assumptions),
        "diagnostic_count": len(result.diagnostics),
    }
