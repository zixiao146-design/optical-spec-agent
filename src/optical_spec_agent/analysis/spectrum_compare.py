"""Lightweight spectrum comparison utilities for local diagnostics.

The implementation intentionally uses only the Python standard library so the
package does not gain a runtime dependency solely for convergence sanity checks.
"""

from __future__ import annotations

import csv
import math
from dataclasses import asdict, dataclass, field
from pathlib import Path


@dataclass(slots=True)
class SpectrumData:
    """Scattering spectrum loaded from a generated CSV artifact."""

    wavelength_nm: list[float]
    flux: list[float]
    source_path: str

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(slots=True)
class SpectrumComparison:
    """JSON-serializable comparison between two spectra."""

    baseline_path: str
    candidate_path: str
    n_points_baseline: int
    n_points_candidate: int
    wavelength_min_nm: float | None
    wavelength_max_nm: float | None
    peak_wavelength_baseline_nm: float | None
    peak_wavelength_candidate_nm: float | None
    peak_shift_nm: float | None
    normalized_l2_difference: float | None
    normalized_max_difference: float | None
    integrated_flux_baseline: float | None
    integrated_flux_candidate: float | None
    integrated_flux_relative_difference: float | None
    finite: bool
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)


def load_scattering_csv(path: Path) -> SpectrumData:
    """Load a generated scattering spectrum CSV and validate numeric values."""
    csv_path = Path(path)
    if not csv_path.exists():
        raise ValueError(f"CSV file does not exist: {csv_path}")

    wavelength_nm: list[float] = []
    flux: list[float] = []
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"CSV file is missing a header: {csv_path}")
        if "wavelength_nm" not in reader.fieldnames:
            raise ValueError(f"CSV file is missing wavelength_nm column: {csv_path}")
        flux_column = _find_flux_column(reader.fieldnames)

        for row_number, row in enumerate(reader, start=2):
            wavelength_nm.append(_parse_finite(row.get("wavelength_nm"), f"wavelength_nm row {row_number}"))
            flux.append(_parse_finite(row.get(flux_column), f"{flux_column} row {row_number}"))

    if not wavelength_nm:
        raise ValueError(f"CSV file has no data rows: {csv_path}")

    pairs = sorted(zip(wavelength_nm, flux), key=lambda item: item[0])
    return SpectrumData(
        wavelength_nm=[item[0] for item in pairs],
        flux=[item[1] for item in pairs],
        source_path=str(csv_path),
    )


def compare_spectra(baseline: SpectrumData, candidate: SpectrumData) -> SpectrumComparison:
    """Compare spectra over their shared wavelength range."""
    warnings: list[str] = []
    overlap_min = max(min(baseline.wavelength_nm), min(candidate.wavelength_nm))
    overlap_max = min(max(baseline.wavelength_nm), max(candidate.wavelength_nm))
    if overlap_min > overlap_max:
        warnings.append("No overlapping wavelength range.")
        return _empty_comparison(baseline, candidate, warnings)

    grid = [wl for wl in baseline.wavelength_nm if overlap_min <= wl <= overlap_max]
    if not grid:
        grid = [overlap_min, overlap_max] if overlap_min < overlap_max else [overlap_min]
        warnings.append("Baseline grid had no points in overlap; using overlap endpoints.")
    if len(grid) < 2:
        warnings.append("Comparison grid has fewer than two points; integrated flux may be null.")

    baseline_flux = [_interp(baseline.wavelength_nm, baseline.flux, wl) for wl in grid]
    candidate_flux = [_interp(candidate.wavelength_nm, candidate.flux, wl) for wl in grid]

    baseline_norm, baseline_norm_warning = _normalize_flux(baseline_flux)
    candidate_norm, candidate_norm_warning = _normalize_flux(candidate_flux)
    warnings.extend([item for item in [baseline_norm_warning, candidate_norm_warning] if item])

    norm_l2 = None
    norm_max = None
    if baseline_norm is not None and candidate_norm is not None:
        diffs = [cand - base for base, cand in zip(baseline_norm, candidate_norm)]
        norm_l2 = math.sqrt(sum(diff * diff for diff in diffs) / len(diffs))
        norm_max = max(abs(diff) for diff in diffs)

    baseline_integral = _trapz(grid, baseline_flux)
    candidate_integral = _trapz(grid, candidate_flux)
    integral_rel_diff = None
    if baseline_integral is not None and candidate_integral is not None:
        denom = abs(baseline_integral)
        if denom <= 1e-15:
            warnings.append("Baseline integrated flux is near zero; relative difference is null.")
        else:
            integral_rel_diff = abs(candidate_integral - baseline_integral) / denom

    peak_base = _peak_wavelength(grid, baseline_flux)
    peak_candidate = _peak_wavelength(grid, candidate_flux)
    peak_shift = None
    if peak_base is not None and peak_candidate is not None:
        peak_shift = peak_candidate - peak_base

    return SpectrumComparison(
        baseline_path=baseline.source_path,
        candidate_path=candidate.source_path,
        n_points_baseline=len(baseline.wavelength_nm),
        n_points_candidate=len(candidate.wavelength_nm),
        wavelength_min_nm=overlap_min,
        wavelength_max_nm=overlap_max,
        peak_wavelength_baseline_nm=peak_base,
        peak_wavelength_candidate_nm=peak_candidate,
        peak_shift_nm=peak_shift,
        normalized_l2_difference=norm_l2,
        normalized_max_difference=norm_max,
        integrated_flux_baseline=baseline_integral,
        integrated_flux_candidate=candidate_integral,
        integrated_flux_relative_difference=integral_rel_diff,
        finite=_all_finite([*baseline_flux, *candidate_flux]),
        warnings=warnings,
    )


def summarize_comparisons(comparisons: list[SpectrumComparison]) -> dict:
    """Return a JSON-serializable summary of comparison metrics."""
    comparison_dicts = [comparison.to_dict() for comparison in comparisons]
    finite_count = sum(1 for comparison in comparisons if comparison.finite)
    return {
        "comparison_count": len(comparisons),
        "finite_count": finite_count,
        "max_abs_peak_shift_nm": _max_abs(
            comparison.peak_shift_nm for comparison in comparisons
        ),
        "max_normalized_l2_difference": _max_optional(
            comparison.normalized_l2_difference for comparison in comparisons
        ),
        "max_integrated_flux_relative_difference": _max_optional(
            comparison.integrated_flux_relative_difference for comparison in comparisons
        ),
        "comparisons": comparison_dicts,
    }


def analyze_flux_signal(spectrum: SpectrumData, *, near_zero_threshold: float = 1e-15) -> dict:
    """Return lightweight diagnostic signal-strength metrics for one spectrum.

    The default threshold is only a conservative diagnostic heuristic. It is not
    a physical standard for deciding whether a Meep observable is meaningful.
    """
    flux_values = spectrum.flux
    abs_values = [abs(value) for value in flux_values]
    max_abs_flux = max(abs_values) if abs_values else 0.0
    mean_abs_flux = sum(abs_values) / len(abs_values) if abs_values else 0.0
    integrated_abs_flux = _trapz(spectrum.wavelength_nm, abs_values)
    integrated_signed_flux = _trapz(spectrum.wavelength_nm, flux_values)
    nonzero_abs = [value for value in abs_values if value > 0.0]
    dynamic_range = None
    if nonzero_abs:
        min_nonzero_abs = min(nonzero_abs)
        if min_nonzero_abs > 0:
            dynamic_range = max_abs_flux / min_nonzero_abs
    near_zero_signal = (
        max_abs_flux < near_zero_threshold
        or integrated_abs_flux is None
        or integrated_abs_flux < near_zero_threshold
    )
    return {
        "source_path": spectrum.source_path,
        "n_points": len(spectrum.wavelength_nm),
        "max_abs_flux": max_abs_flux,
        "mean_abs_flux": mean_abs_flux,
        "integrated_abs_flux": integrated_abs_flux,
        "integrated_signed_flux": integrated_signed_flux,
        "dynamic_range": dynamic_range,
        "near_zero_signal": near_zero_signal,
        "near_zero_threshold": near_zero_threshold,
    }


def _find_flux_column(fieldnames: list[str]) -> str:
    candidates = [
        "particle_induced_flux_relative",
        "scattering_flux",
        "scattering_flux_relative",
        "flux",
    ]
    for candidate in candidates:
        if candidate in fieldnames:
            return candidate
    raise ValueError(f"CSV file is missing a supported flux column; found {fieldnames}")


def _parse_finite(raw_value: str | None, label: str) -> float:
    if raw_value is None or raw_value == "":
        raise ValueError(f"{label} is missing")
    try:
        value = float(raw_value)
    except ValueError as exc:
        raise ValueError(f"{label} is not numeric: {raw_value!r}") from exc
    if math.isnan(value):
        raise ValueError(f"{label} is NaN")
    if math.isinf(value):
        raise ValueError(f"{label} is Inf")
    return value


def _interp(x_values: list[float], y_values: list[float], x: float) -> float:
    if x <= x_values[0]:
        return y_values[0]
    if x >= x_values[-1]:
        return y_values[-1]
    for idx in range(1, len(x_values)):
        x0 = x_values[idx - 1]
        x1 = x_values[idx]
        if x0 <= x <= x1:
            y0 = y_values[idx - 1]
            y1 = y_values[idx]
            if x1 == x0:
                return y0
            t = (x - x0) / (x1 - x0)
            return y0 + t * (y1 - y0)
    return y_values[-1]


def _normalize_flux(values: list[float]) -> tuple[list[float] | None, str | None]:
    scale = max((abs(value) for value in values), default=0.0)
    if scale <= 1e-15:
        return None, "Flux is all zero or near zero; normalized difference is null."
    return [value / scale for value in values], None


def _trapz(x_values: list[float], y_values: list[float]) -> float | None:
    if len(x_values) < 2:
        return None
    total = 0.0
    for idx in range(1, len(x_values)):
        total += 0.5 * (y_values[idx - 1] + y_values[idx]) * (x_values[idx] - x_values[idx - 1])
    return total


def _peak_wavelength(wavelength_nm: list[float], flux: list[float]) -> float | None:
    if not wavelength_nm:
        return None
    peak_idx = max(range(len(flux)), key=lambda idx: flux[idx])
    return wavelength_nm[peak_idx]


def _all_finite(values: list[float]) -> bool:
    return all(math.isfinite(value) for value in values)


def _max_optional(values) -> float | None:
    concrete = [value for value in values if value is not None]
    return max(concrete) if concrete else None


def _max_abs(values) -> float | None:
    concrete = [abs(value) for value in values if value is not None]
    return max(concrete) if concrete else None


def _empty_comparison(
    baseline: SpectrumData,
    candidate: SpectrumData,
    warnings: list[str],
) -> SpectrumComparison:
    return SpectrumComparison(
        baseline_path=baseline.source_path,
        candidate_path=candidate.source_path,
        n_points_baseline=len(baseline.wavelength_nm),
        n_points_candidate=len(candidate.wavelength_nm),
        wavelength_min_nm=None,
        wavelength_max_nm=None,
        peak_wavelength_baseline_nm=None,
        peak_wavelength_candidate_nm=None,
        peak_shift_nm=None,
        normalized_l2_difference=None,
        normalized_max_difference=None,
        integrated_flux_baseline=None,
        integrated_flux_candidate=None,
        integrated_flux_relative_difference=None,
        finite=False,
        warnings=warnings,
    )
