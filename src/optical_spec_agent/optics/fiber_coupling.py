"""Preview fiber-coupling design helpers."""

from __future__ import annotations

import math

from .models import CalculatorQuality, CalculatorResult


def _fiber_quality(
    *,
    reference_case: str | None = None,
    assumptions: list[str] | None = None,
    warnings: list[str] | None = None,
) -> CalculatorQuality:
    return CalculatorQuality(
        reference_case=reference_case,
        assumptions=assumptions
        or [
            "Input beam and fiber mode are approximated as scalar circular Gaussian modes.",
            "The estimate separates waist mismatch, lateral offset, and angular tilt factors.",
        ],
        limitations=[
            "Scalar Gaussian overlap preview only.",
            "Ignores vector polarization overlap, Fresnel reflections, aberrations, NA clipping, and mode-solver effects.",
            "Not production-grade physical validation.",
        ],
        warnings=warnings
        or [
            "Use a validated mode-overlap or beam-propagation workflow before drawing physical conclusions."
        ],
        valid_input_range={
            "wavelength_nm": "positive",
            "waist_input_um": "positive",
            "waist_fiber_um": "positive",
            "lateral_offset_um": "non-negative preview offset",
            "angular_tilt_mrad": "finite preview tilt",
        },
    )


def gaussian_mode_overlap(
    waist_input_um: float,
    waist_fiber_um: float,
    lateral_offset_um: float = 0.0,
    angular_tilt_mrad: float = 0.0,
    wavelength_nm: float = 1550.0,
) -> CalculatorResult:
    """Estimate Gaussian-to-fiber mode coupling efficiency.

    The model is intentionally lightweight: circular scalar Gaussian modes,
    independent multiplicative penalties for lateral offset and angular tilt,
    and no solver execution. It is useful for design orientation and benchmark
    closure, not production coupling validation.
    """

    if not math.isfinite(waist_input_um) or not math.isfinite(waist_fiber_um):
        raise ValueError("waist_input_um and waist_fiber_um must be finite.")
    if not math.isfinite(wavelength_nm):
        raise ValueError("wavelength_nm must be finite.")
    if not math.isfinite(lateral_offset_um) or not math.isfinite(angular_tilt_mrad):
        raise ValueError("lateral_offset_um and angular_tilt_mrad must be finite.")
    if waist_input_um <= 0 or waist_fiber_um <= 0:
        raise ValueError("waist_input_um and waist_fiber_um must be positive.")
    if wavelength_nm <= 0:
        raise ValueError("wavelength_nm must be positive.")
    if lateral_offset_um < 0:
        raise ValueError("lateral_offset_um must be non-negative.")

    wavelength_um = wavelength_nm / 1000.0
    waist_sum_sq = waist_input_um**2 + waist_fiber_um**2
    mode_mismatch_factor = (2.0 * waist_input_um * waist_fiber_um / waist_sum_sq) ** 2
    offset_factor = math.exp(-2.0 * lateral_offset_um**2 / waist_sum_sq)

    tilt_rad = abs(angular_tilt_mrad) / 1000.0
    effective_waist_um = 2.0 * waist_input_um * waist_fiber_um / math.sqrt(waist_sum_sq)
    tilt_factor = math.exp(-((math.pi * effective_waist_um * tilt_rad / wavelength_um) ** 2))
    coupling_efficiency_estimate = max(
        0.0,
        min(1.0, mode_mismatch_factor * offset_factor * tilt_factor),
    )

    assumptions = [
        "Scalar circular Gaussian field overlap preview.",
        "Mode mismatch factor eta_w = (2 w_in w_f / (w_in^2 + w_f^2))^2.",
        "Lateral offset and angular tilt are modeled as independent Gaussian penalty factors.",
        "Polarization overlap, Fresnel loss, NA clipping, and aberrations are not included.",
    ]
    warnings = [
        "Use a validated mode-overlap calculation or measured alignment data before physical conclusions."
    ]
    reference_case = None
    if (
        math.isclose(waist_input_um, waist_fiber_um, rel_tol=0.0, abs_tol=1e-12)
        and lateral_offset_um == 0
        and abs(angular_tilt_mrad) < 1e-12
    ):
        reference_case = "fiber_gaussian_perfect_overlap"
    elif lateral_offset_um > 0 and abs(angular_tilt_mrad) < 1e-12:
        reference_case = "fiber_gaussian_offset_loss"
    elif lateral_offset_um == 0 and abs(angular_tilt_mrad) > 0:
        reference_case = "fiber_gaussian_tilt_loss"
    elif not math.isclose(waist_input_um, waist_fiber_um, rel_tol=0.0, abs_tol=1e-12):
        reference_case = "fiber_gaussian_waist_mismatch"

    return CalculatorResult(
        result={
            "wavelength_nm": wavelength_nm,
            "waist_input_um": waist_input_um,
            "waist_fiber_um": waist_fiber_um,
            "lateral_offset_um": lateral_offset_um,
            "angular_tilt_mrad": angular_tilt_mrad,
            "mode_mismatch_factor": mode_mismatch_factor,
            "offset_factor": offset_factor,
            "tilt_factor": tilt_factor,
            "coupling_efficiency_estimate": coupling_efficiency_estimate,
            "summary": (
                "Gaussian fiber-coupling preview estimates "
                f"{coupling_efficiency_estimate:.4f} coupling efficiency."
            ),
        },
        assumptions=assumptions,
        diagnostics=[
            "Efficiency is bounded to [0, 1].",
            "Perfect waist match with zero offset/tilt is the local sanity reference.",
        ],
        warnings=warnings,
        quality=_fiber_quality(
            reference_case=reference_case,
            assumptions=assumptions,
            warnings=warnings,
        ),
    )


def suggest_fiber_coupling_inputs() -> dict[str, list[str]]:
    """Return required and optional inputs for the fiber-coupling preview."""

    return {
        "required_inputs": [
            "wavelength_nm",
            "input_beam_waist_um",
            "fiber_mode_field_diameter_or_waist_um",
        ],
        "alignment_inputs": [
            "lateral_offset_um",
            "angular_tilt_mrad",
        ],
        "optional_inputs": [
            "polarization_state",
            "fiber_na",
            "mode_family",
            "fresnel_interface_loss",
        ],
        "recommended_questions": [
            "What wavelength and input beam waist should be used?",
            "What fiber mode field diameter or waist should define the target mode?",
            "What lateral offset, angular tilt, and polarization should be assumed?",
        ],
    }
