"""Preview Jones-calculus polarization helpers."""

from __future__ import annotations

import cmath
import math
from typing import Any

from .models import CalculatorQuality, CalculatorResult


JonesVector = list[complex]


def _polarization_quality(
    *,
    reference_case: str | None = None,
    assumptions: list[str] | None = None,
    warnings: list[str] | None = None,
) -> CalculatorQuality:
    return CalculatorQuality(
        reference_case=reference_case,
        assumptions=assumptions
        or [
            "Jones vectors are normalized coherent two-component polarization states.",
            "Optical elements are ideal, lossless unless a polarizer is requested.",
        ],
        limitations=[
            "Jones-calculus preview only.",
            "Does not model depolarization, spatially varying vector fields, dispersion, coatings, or fabrication tolerances.",
            "Not production-grade physical validation.",
        ],
        warnings=warnings
        or [
            "Use full vector EM or measured Jones/Mueller data before physical conclusions."
        ],
        valid_input_range={
            "angle_deg": "finite real angle",
            "retardance_rad": "finite real retardance",
            "input_jones": "two finite complex components",
        },
    )


def linear_polarization(angle_deg: float) -> CalculatorResult:
    """Return a normalized linear-polarization Jones vector."""

    _require_finite(angle_deg, "angle_deg")
    angle_rad = math.radians(angle_deg)
    vector = [complex(math.cos(angle_rad), 0.0), complex(math.sin(angle_rad), 0.0)]
    assumptions = [
        "Linear polarization is represented as [cos(theta), sin(theta)].",
        "Global optical phase is ignored.",
    ]
    reference_case = "jones_linear_polarization"
    if math.isclose((angle_deg % 180.0), 0.0, abs_tol=1e-12):
        reference_case = "jones_linear_0deg"
    elif math.isclose((angle_deg % 180.0), 90.0, abs_tol=1e-12):
        reference_case = "jones_linear_90deg"
    return _polarization_result(
        vector,
        assumptions=assumptions,
        diagnostics=["Linear polarization sanity vector generated."],
        reference_case=reference_case,
    )


def jones_linear_polarizer(input_jones: list[Any], angle_deg: float) -> CalculatorResult:
    """Apply an ideal linear polarizer at angle_deg."""

    _require_finite(angle_deg, "angle_deg")
    vector = _parse_jones_vector(input_jones)
    axis = math.radians(angle_deg)
    c = math.cos(axis)
    s = math.sin(axis)
    projection = c * vector[0] + s * vector[1]
    output = [projection * c, projection * s]
    assumptions = [
        "Ideal linear polarizer using P = |a><a|.",
        "Input and output intensities are normalized Jones-vector powers.",
        "No extinction-ratio, coating, or angular-bandwidth model is included.",
    ]
    reference_case = "jones_linear_polarizer_projection"
    input_intensity = _intensity(vector)
    output_intensity = _intensity(output)
    if input_intensity > 0 and math.isclose(
        output_intensity / input_intensity,
        0.5,
        rel_tol=0.0,
        abs_tol=1e-12,
    ):
        reference_case = "jones_linear_polarizer_malus"
    return _polarization_result(
        output,
        input_jones=vector,
        assumptions=assumptions,
        diagnostics=["Ideal polarizer projection applied."],
        reference_case=reference_case,
    )


def jones_waveplate(
    input_jones: list[Any],
    retardance_rad: float,
    fast_axis_deg: float,
) -> CalculatorResult:
    """Apply an ideal linear retarder / waveplate."""

    _require_finite(retardance_rad, "retardance_rad")
    _require_finite(fast_axis_deg, "fast_axis_deg")
    vector = _parse_jones_vector(input_jones)
    axis = math.radians(fast_axis_deg)
    c = math.cos(axis)
    s = math.sin(axis)
    phase_fast = cmath.exp(-0.5j * retardance_rad)
    phase_slow = cmath.exp(0.5j * retardance_rad)

    # Rotate into the waveplate axes, apply retardance, then rotate back.
    local_x = c * vector[0] + s * vector[1]
    local_y = -s * vector[0] + c * vector[1]
    delayed_x = phase_fast * local_x
    delayed_y = phase_slow * local_y
    output = [
        c * delayed_x - s * delayed_y,
        s * delayed_x + c * delayed_y,
    ]
    assumptions = [
        "Ideal lossless Jones waveplate.",
        "Retardance is spatially uniform and wavelength-independent in this preview.",
        "No depolarization, aperture, coating, or vector-field propagation is modeled.",
    ]
    reference_case = None
    if math.isclose(abs(retardance_rad), math.pi, rel_tol=0.0, abs_tol=1e-9):
        reference_case = "jones_half_waveplate_preview"
    elif math.isclose(abs(retardance_rad), math.pi / 2.0, rel_tol=0.0, abs_tol=1e-9):
        reference_case = "jones_quarter_waveplate_phase_preview"
    return _polarization_result(
        output,
        input_jones=vector,
        assumptions=assumptions,
        diagnostics=["Ideal waveplate Jones matrix applied."],
        reference_case=reference_case,
    )


def summarize_polarization_state(jones_vector: list[Any]) -> CalculatorResult:
    """Summarize a Jones vector without applying an element."""

    return _polarization_result(
        _parse_jones_vector(jones_vector),
        assumptions=["Jones-vector state summary only."],
        diagnostics=["State normalized for preview diagnostics."],
        reference_case="jones_state_summary",
    )


def _polarization_result(
    output: JonesVector,
    *,
    input_jones: JonesVector | None = None,
    assumptions: list[str],
    diagnostics: list[str],
    reference_case: str | None,
) -> CalculatorResult:
    input_intensity = _intensity(input_jones) if input_jones is not None else None
    intensity = _intensity(output)
    normalized = _normalize(output)
    summary = _summary(normalized, intensity)
    warnings = ["Jones calculus is a coherent, two-component preview model only."]
    return CalculatorResult(
        result={
            "input_jones": _serialize_vector(input_jones) if input_jones is not None else None,
            "output_jones": _serialize_vector(output),
            "intensity": intensity,
            "input_intensity": input_intensity,
            "normalized_state": _serialize_vector(normalized),
            "relative_phase_rad": _relative_phase(normalized),
            "summary": summary,
        },
        assumptions=assumptions,
        diagnostics=diagnostics,
        warnings=warnings,
        quality=_polarization_quality(
            reference_case=reference_case,
            assumptions=assumptions,
            warnings=warnings,
        ),
    )


def _parse_jones_vector(values: list[Any]) -> JonesVector:
    if len(values) != 2:
        raise ValueError("input_jones must contain exactly two components.")
    vector = [_parse_complex(component) for component in values]
    if not all(math.isfinite(item.real) and math.isfinite(item.imag) for item in vector):
        raise ValueError("input_jones components must be finite.")
    if _intensity(vector) <= 0:
        raise ValueError("input_jones must have non-zero intensity.")
    return vector


def _require_finite(value: float, field_name: str) -> None:
    if not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise ValueError(f"{field_name} must be finite.")


def _parse_complex(value: Any) -> complex:
    if isinstance(value, complex):
        return value
    if isinstance(value, (int, float)):
        return complex(float(value), 0.0)
    if isinstance(value, dict):
        return complex(float(value.get("real", 0.0)), float(value.get("imag", 0.0)))
    if isinstance(value, (list, tuple)) and len(value) == 2:
        return complex(float(value[0]), float(value[1]))
    raise ValueError("Jones components must be numbers, [real, imag], or {real, imag}.")


def _intensity(vector: JonesVector | None) -> float:
    if vector is None:
        return 0.0
    return float(sum(abs(component) ** 2 for component in vector))


def _normalize(vector: JonesVector) -> JonesVector:
    intensity = _intensity(vector)
    if intensity <= 0:
        return [0j, 0j]
    scale = math.sqrt(intensity)
    return [component / scale for component in vector]


def _serialize_vector(vector: JonesVector | None) -> list[dict[str, float]] | None:
    if vector is None:
        return None
    return [{"real": component.real, "imag": component.imag} for component in vector]


def _relative_phase(vector: JonesVector) -> float | None:
    if abs(vector[0]) < 1e-12 or abs(vector[1]) < 1e-12:
        return None
    return math.atan2(vector[1].imag, vector[1].real) - math.atan2(vector[0].imag, vector[0].real)


def _summary(vector: JonesVector, intensity: float) -> str:
    amplitudes = [abs(component) for component in vector]
    return (
        "Jones polarization preview with normalized amplitudes "
        f"({amplitudes[0]:.3f}, {amplitudes[1]:.3f}) and intensity {intensity:.3f}."
    )
