"""Post-hoc physical diagnostics for local Meep artifact reviews.

These helpers are intentionally lightweight and conservative. They do not run
Meep and they do not claim physical validation; they read an ``OpticalSpec`` and
available local artifacts, then write auditable CSV/JSON/PNG summaries.
"""

from __future__ import annotations

import csv
import json
import math
import re
import struct
import zlib
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from pydantic import BaseModel

from optical_spec_agent.analysis.mesh_sanity import MeshSanityResult, analyze_mesh_resolution
from optical_spec_agent.analysis.spectrum_compare import (
    SpectrumData,
    analyze_flux_signal,
    load_scattering_csv,
)
from optical_spec_agent.models.base import StatusField
from optical_spec_agent.models.spec import OpticalSpec


DIAGNOSTICS_SCHEMA_VERSION = "physical_diagnostics.v0.1"
CORE_HERO_TASK = (
    "用 Meep FDTD 仿真 80 nm 金纳米球放在 100 nm 金膜上，中间 SiO2 gap 为 5 nm，"
    "平面波正入射，波长范围 400-900 nm，输出散射谱，提取共振波长和 FWHM。"
)


@dataclass(slots=True)
class FluxMonitorSummary:
    """Aggregate signal metrics for one flux-monitor column."""

    monitor: str
    n_points: int
    mean_flux: float | None = None
    max_abs_flux: float | None = None
    integrated_abs_flux: float | None = None
    integrated_signed_flux: float | None = None
    near_zero_signal: bool | None = None
    anomaly: bool = False
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class PhysicalDiagnosticsResult:
    """Top-level JSON-serializable diagnostics result."""

    schema_version: str
    generated_at: str
    created_at: str
    spec_path: str
    output_dir: str
    run_dir: str | None
    status: str
    generated_outputs: dict[str, str]
    task: dict[str, Any]
    extracted_config: dict[str, Any]
    mesh_diagnostics: dict[str, Any] | None
    flux_diagnostics: list[dict[str, Any]]
    execution_diagnostics: dict[str, Any]
    warnings: list[str]
    errors: list[str]
    missing_artifacts: list[str]
    nan_detected: bool
    inf_detected: bool
    timeout_detected: bool
    notes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def generate_physical_diagnostics(
    *,
    spec_path: Path,
    output_dir: Path,
    artifact_dir: Path | None = None,
    execution_result_path: Path | None = None,
    spectrum_path: Path | None = None,
    flux_surfaces_path: Path | None = None,
    resolution_px_per_um: float = 12.0,
    create_preview: bool = True,
) -> PhysicalDiagnosticsResult:
    """Generate mesh, flux, execution, and preview diagnostics under ``output_dir``."""
    output_dir.mkdir(parents=True, exist_ok=True)
    warnings: list[str] = []
    errors: list[str] = []

    spec = load_optical_spec(spec_path)
    config = extract_diagnostic_config(spec, resolution_px_per_um=resolution_px_per_um)

    if config["mesh"].get("resolution_source") == "diagnostic_default":
        warnings.append("Mesh resolution missing in spec; using diagnostic default resolution.")

    mesh_result: MeshSanityResult | None = None
    try:
        mesh_result = analyze_mesh_resolution(
            resolution_px_per_um=float(config["mesh"]["resolution_px_per_um"]),
            gap_thickness_nm=float(config["geometry"]["gap_thickness_nm"]),
            particle_radius_nm=float(config["geometry"]["particle_radius_nm"]),
            film_thickness_nm=float(config["geometry"]["film_thickness_nm"]),
        )
        warnings.extend(mesh_result.warnings)
    except (TypeError, ValueError) as exc:
        errors.append(f"Mesh diagnostics unavailable: {exc}")

    artifact_paths = resolve_artifact_paths(
        artifact_dir=artifact_dir,
        execution_result_path=execution_result_path,
        spectrum_path=spectrum_path,
        flux_surfaces_path=flux_surfaces_path,
        output_dir=output_dir,
    )
    flux_summaries = analyze_flux_artifacts(
        flux_surfaces_path=artifact_paths.get("flux_surfaces"),
        spectrum_path=artifact_paths.get("spectrum"),
    )
    if not flux_summaries:
        warnings.append("No flux artifacts found; flux_report.csv records missing monitor data.")
        flux_summaries = [
            FluxMonitorSummary(
                monitor="missing",
                n_points=0,
                anomaly=True,
                notes=["No flux_surfaces.csv or scattering_spectrum.csv was available."],
            )
        ]
    for summary in flux_summaries:
        if summary.anomaly:
            warnings.extend(summary.notes)

    execution_diagnostics = analyze_execution_artifacts(
        execution_result_path=artifact_paths.get("execution_result"),
        artifact_dir=artifact_dir,
    )
    warnings.extend(execution_diagnostics.get("warnings_detected", []))
    errors.extend(execution_diagnostics.get("errors_detected", []))
    missing_artifacts = execution_diagnostics.get("missing_artifacts", [])

    generated_outputs: dict[str, str] = {}
    mesh_report_path = output_dir / "mesh_report.csv"
    write_mesh_report(mesh_report_path, mesh_result, config)
    generated_outputs["mesh_report.csv"] = str(mesh_report_path)

    flux_report_path = output_dir / "flux_report.csv"
    write_flux_report(flux_report_path, flux_summaries)
    generated_outputs["flux_report.csv"] = str(flux_report_path)

    preview_path = output_dir / "diagnostic_preview.png"
    if create_preview:
        preview_warning = write_diagnostic_preview(
            preview_path,
            spectrum_path=artifact_paths.get("spectrum"),
            config=config,
        )
        generated_outputs["diagnostic_preview.png"] = str(preview_path)
        if preview_warning:
            warnings.append(preview_warning)

    warnings = _dedupe(warnings)
    errors = _dedupe(errors)
    status = _diagnostic_status(errors=errors, warnings=warnings, missing_artifacts=missing_artifacts)
    generated_at = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    result = PhysicalDiagnosticsResult(
        schema_version=DIAGNOSTICS_SCHEMA_VERSION,
        generated_at=generated_at,
        created_at=generated_at,
        spec_path=str(spec_path),
        output_dir=str(output_dir),
        run_dir=str(artifact_dir) if artifact_dir else None,
        status=status,
        generated_outputs=generated_outputs,
        task=config["task"],
        extracted_config=config,
        mesh_diagnostics=mesh_result.to_dict() if mesh_result else None,
        flux_diagnostics=[summary.to_dict() for summary in flux_summaries],
        execution_diagnostics=execution_diagnostics,
        warnings=warnings,
        errors=errors,
        missing_artifacts=missing_artifacts,
        nan_detected=bool(execution_diagnostics.get("nan_detected")),
        inf_detected=bool(execution_diagnostics.get("inf_detected")),
        timeout_detected=bool(execution_diagnostics.get("timeout_detected")),
        notes=[
            "Post-hoc diagnostics only; not production-grade physical validation.",
            "diagnostic_preview.png is a readability artifact, not a scientific figure.",
        ],
    )

    diagnostics_path = output_dir / "execution_diagnostics.json"
    diagnostics_path.write_text(
        json.dumps(result.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    result.generated_outputs["execution_diagnostics.json"] = str(diagnostics_path)
    diagnostics_path.write_text(
        json.dumps(result.to_dict(), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return result


def prepare_diagnostic_spec(
    spec_path: Path,
    *,
    create_demo_spec_if_missing: bool,
) -> tuple[Path, bool]:
    """Ensure a diagnostics spec exists, optionally creating the core demo spec."""
    spec_path = Path(spec_path)
    if spec_path.exists():
        return spec_path, False
    if not create_demo_spec_if_missing:
        raise FileNotFoundError(
            f"Spec file not found: {spec_path}. "
            "Pass --create-demo-spec-if-missing for a traceable demo spec."
        )

    from optical_spec_agent.services.spec_service import SpecService
    from optical_spec_agent.utils.format import spec_to_json

    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec = SpecService().process(CORE_HERO_TASK, task_id="diagnostic-demo")
    spec_path.write_text(spec_to_json(spec), encoding="utf-8")
    return spec_path, True


def load_optical_spec(path: Path) -> OpticalSpec:
    """Load an ``OpticalSpec`` JSON file."""
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return OpticalSpec.model_validate(data)


def extract_diagnostic_config(
    spec: OpticalSpec,
    *,
    resolution_px_per_um: float,
) -> dict[str, Any]:
    """Extract task, geometry, source, mesh, and monitor configuration."""
    particle = _unwrap(spec.geometry_material.particle_info) or {}
    film = _unwrap(spec.geometry_material.substrate_or_film_info) or {}
    source = _unwrap(spec.simulation.source_setting) or {}
    mesh = _unwrap(spec.simulation.mesh_setting) or {}
    monitor = _unwrap(spec.simulation.monitor_setting) or {}

    particle_dimensions = _model_or_dict_get(particle, "dimensions", {}) or {}
    diameter_nm = _first_numeric(
        _dict_get_any(particle_dimensions, ["diameter_nm", "diameter", "直径"])
    )
    edge_length_nm = _first_numeric(
        _dict_get_any(particle_dimensions, ["edge_length_nm", "edge_length", "边长"])
    )
    particle_radius_nm = (diameter_nm or edge_length_nm or 80.0) / 2.0

    key_parameters = _unwrap(spec.geometry_material.key_parameters) or []
    gap_thickness_nm = (
        _gap_from_key_parameters(key_parameters)
        or _gap_from_sweep(_unwrap(spec.simulation.sweep_plan))
        or 5.0
    )
    film_thickness_nm = _first_numeric(_model_or_dict_get(film, "film_thickness", "")) or 100.0

    mesh_resolution, mesh_source = _extract_mesh_resolution(mesh, resolution_px_per_um)

    return {
        "task": {
            "task_id": spec.task.task_id,
            "task_type": _unwrap(spec.task.task_type),
            "task_name": _unwrap(spec.task.task_name),
            "research_goal": _unwrap(spec.task.research_goal),
        },
        "geometry": {
            "physical_system": _unwrap(spec.physics.physical_system),
            "structure_type": _unwrap(spec.physics.structure_type),
            "particle_type": _model_or_dict_get(particle, "particle_type", ""),
            "particle_material": _model_or_dict_get(particle, "material", ""),
            "particle_dimensions": _jsonable(particle_dimensions),
            "particle_radius_nm": particle_radius_nm,
            "film_material": _model_or_dict_get(film, "film_material", ""),
            "film_thickness_nm": film_thickness_nm,
            "gap_medium": _unwrap(spec.geometry_material.gap_medium),
            "gap_thickness_nm": gap_thickness_nm,
            "key_parameters": key_parameters,
        },
        "mesh": {
            "mesh_setting": _jsonable(mesh),
            "resolution_px_per_um": mesh_resolution,
            "resolution_source": mesh_source,
        },
        "source": {
            "excitation_source": _unwrap(spec.simulation.excitation_source),
            "incident_direction": _unwrap(spec.simulation.incident_direction),
            "polarization": _unwrap(spec.simulation.polarization),
            "source_setting": _jsonable(source),
            "wavelength_range": _model_or_dict_get(source, "wavelength_range", ""),
        },
        "flux_monitor": {
            "monitor_setting": _jsonable(monitor),
            "monitor_type": _model_or_dict_get(monitor, "monitor_type", ""),
            "frequency_points": _model_or_dict_get(monitor, "frequency_points", None),
            "locations": _model_or_dict_get(monitor, "locations", []),
        },
        "provenance": {
            "confirmed_fields": spec.confirmed_fields,
            "inferred_fields": spec.inferred_fields,
            "missing_fields": spec.missing_fields,
            "assumption_log": spec.assumption_log,
        },
    }


def resolve_artifact_paths(
    *,
    artifact_dir: Path | None,
    execution_result_path: Path | None,
    spectrum_path: Path | None,
    flux_surfaces_path: Path | None,
    output_dir: Path,
) -> dict[str, Path | None]:
    """Resolve optional execution artifacts from explicit paths or a run directory."""
    base = artifact_dir or output_dir
    return {
        "execution_result": _existing_path(execution_result_path)
        or _existing_path(base / "execution_result.json"),
        "spectrum": _existing_path(spectrum_path) or _existing_path(base / "scattering_spectrum.csv"),
        "flux_surfaces": _existing_path(flux_surfaces_path) or _existing_path(base / "flux_surfaces.csv"),
    }


def analyze_flux_artifacts(
    *,
    flux_surfaces_path: Path | None,
    spectrum_path: Path | None,
) -> list[FluxMonitorSummary]:
    """Aggregate per-surface flux CSVs, falling back to scattering_spectrum.csv."""
    if flux_surfaces_path and flux_surfaces_path.exists():
        return _analyze_flux_surfaces_csv(flux_surfaces_path)
    if spectrum_path and spectrum_path.exists():
        try:
            spectrum = load_scattering_csv(spectrum_path)
        except ValueError as exc:
            return [
                FluxMonitorSummary(
                    monitor="scattering_spectrum",
                    n_points=0,
                    anomaly=True,
                    notes=[f"Could not parse scattering spectrum: {exc}"],
                )
            ]
        metrics = analyze_flux_signal(spectrum)
        return [
            FluxMonitorSummary(
                monitor="scattering_spectrum",
                n_points=metrics["n_points"],
                mean_flux=_mean(spectrum.flux),
                max_abs_flux=metrics["max_abs_flux"],
                integrated_abs_flux=metrics["integrated_abs_flux"],
                integrated_signed_flux=metrics["integrated_signed_flux"],
                near_zero_signal=metrics["near_zero_signal"],
                anomaly=bool(metrics["near_zero_signal"]),
                notes=["near-zero flux signal"] if metrics["near_zero_signal"] else [],
            )
        ]
    return []


def analyze_execution_artifacts(
    *,
    execution_result_path: Path | None,
    artifact_dir: Path | None,
) -> dict[str, Any]:
    """Read execution_result/stdout/stderr artifacts and detect runtime anomalies."""
    diagnostics: dict[str, Any] = {
        "execution_result_path": str(execution_result_path) if execution_result_path else None,
        "run_dir": str(artifact_dir) if artifact_dir else None,
        "success": None,
        "available": None,
        "returncode": None,
        "run_id": None,
        "outputs": {},
        "nan_detected": False,
        "inf_detected": False,
        "nan_or_inf_detected": False,
        "timeout_detected": False,
        "missing_artifacts": _missing_run_artifacts(artifact_dir),
        "stderr_excerpt": "",
        "stdout_excerpt": "",
        "warnings_detected": [],
        "errors_detected": [],
    }
    text_blobs: list[str] = []
    if execution_result_path and execution_result_path.exists():
        try:
            data = json.loads(execution_result_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            diagnostics["errors_detected"].append(f"Could not parse execution_result.json: {exc}")
        else:
            diagnostics.update(
                {
                    "success": data.get("success"),
                    "available": data.get("available"),
                    "returncode": data.get("returncode"),
                    "run_id": data.get("run_id"),
                    "outputs": data.get("outputs", {}),
                    "errors": data.get("errors", []),
                    "warnings": data.get("warnings", []),
                    "typed_postprocess_results": data.get("typed_postprocess_results"),
                }
            )
            text_blobs.extend(
                [
                    str(data.get("stdout") or ""),
                    str(data.get("stderr") or ""),
                    " ".join(str(item) for item in data.get("errors", [])),
                    " ".join(str(item) for item in data.get("warnings", [])),
                ]
            )
    else:
        diagnostics["warnings_detected"].append("execution_result.json was not found.")

    if artifact_dir:
        stdout_path = artifact_dir / "stdout.txt"
        stderr_path = artifact_dir / "stderr.txt"
        if stdout_path.exists():
            stdout_text = stdout_path.read_text(encoding="utf-8", errors="replace")
            diagnostics["stdout_excerpt"] = stdout_text[-1000:]
            text_blobs.append(stdout_text)
        if stderr_path.exists():
            stderr_text = stderr_path.read_text(encoding="utf-8", errors="replace")
            diagnostics["stderr_excerpt"] = stderr_text[-1000:]
            text_blobs.append(stderr_text)
        if diagnostics["missing_artifacts"]:
            diagnostics["warnings_detected"].append(
                "Missing execution artifacts: " + ", ".join(diagnostics["missing_artifacts"])
            )

    combined = "\n".join(text_blobs).lower()
    diagnostics["nan_detected"] = bool(re.search(r"\bnan\b", combined))
    diagnostics["inf_detected"] = bool(re.search(r"\binf\b", combined))
    if diagnostics["nan_detected"] or diagnostics["inf_detected"]:
        diagnostics["nan_or_inf_detected"] = True
        diagnostics["warnings_detected"].append("NaN/Inf detected in execution logs or errors.")
    if "timeout" in combined or "timed out" in combined:
        diagnostics["timeout_detected"] = True
        diagnostics["warnings_detected"].append("Timeout detected in execution logs or errors.")

    return diagnostics


def write_mesh_report(
    path: Path,
    mesh_result: MeshSanityResult | None,
    config: dict[str, Any],
) -> None:
    """Write mesh sanity report as metric/value/status rows."""
    rows: list[dict[str, Any]] = []
    if mesh_result is None:
        rows.append(
            {
                "check_name": "mesh_diagnostics",
                "value": "",
                "threshold": "",
                "unit": "",
                "status": "error",
                "message": "mesh diagnostics unavailable",
            }
        )
    else:
        data = mesh_result.to_dict()
        for metric, value in data.items():
            if metric == "warnings":
                continue
            threshold = ""
            if metric == "gap_cells":
                threshold = f">= {mesh_result.min_recommended_gap_cells}"
            rows.append(
                {
                    "check_name": metric,
                    "value": value,
                    "threshold": threshold,
                    "unit": _mesh_unit(metric),
                    "status": "warn"
                    if metric == "gap_cells" and not mesh_result.physically_resolved
                    else "ok",
                    "message": "; ".join(mesh_result.warnings)
                    if metric == "gap_cells" and mesh_result.warnings
                    else "",
                }
            )
    rows.append(
        {
            "check_name": "resolution_source",
            "value": config["mesh"]["resolution_source"],
            "threshold": "",
            "unit": "",
            "status": "info",
            "message": "source of resolution used for diagnostics",
        }
    )
    _write_csv(path, ["check_name", "value", "threshold", "unit", "status", "message"], rows)


def write_flux_report(path: Path, summaries: list[FluxMonitorSummary]) -> None:
    """Write per-monitor flux report."""
    rows = [
        {
            "monitor_name": _monitor_base_name(item.monitor),
            "surface": _monitor_surface_name(item.monitor),
            "value": item.max_abs_flux,
            "unit": "relative_flux",
            "status": "warn" if item.anomaly else "ok",
            "message": "; ".join(item.notes),
            "n_points": item.n_points,
            "mean_flux": item.mean_flux,
            "max_abs_flux": item.max_abs_flux,
            "integrated_abs_flux": item.integrated_abs_flux,
            "integrated_signed_flux": item.integrated_signed_flux,
            "near_zero_signal": item.near_zero_signal,
            "anomaly": item.anomaly,
        }
        for item in summaries
    ]
    _write_csv(
        path,
        [
            "monitor_name",
            "surface",
            "value",
            "unit",
            "status",
            "message",
            "n_points",
            "mean_flux",
            "max_abs_flux",
            "integrated_abs_flux",
            "integrated_signed_flux",
            "near_zero_signal",
            "anomaly",
        ],
        rows,
    )


def write_diagnostic_preview(
    path: Path,
    *,
    spectrum_path: Path | None,
    config: dict[str, Any],
) -> str:
    """Write a PNG preview using matplotlib when available, with a stdlib fallback."""
    spectrum: SpectrumData | None = None
    if spectrum_path and spectrum_path.exists():
        try:
            spectrum = load_scattering_csv(spectrum_path)
        except ValueError:
            spectrum = None

    try:
        import matplotlib.pyplot as plt  # type: ignore[import-not-found]
    except Exception:
        _write_simple_png_preview(path, spectrum=spectrum, config=config)
        return "matplotlib unavailable; wrote fallback diagnostic preview PNG."

    fig, ax = plt.subplots(figsize=(7, 4), dpi=120)
    if spectrum:
        ax.plot(spectrum.wavelength_nm, spectrum.flux, marker="o", linewidth=1.5)
        ax.set_xlabel("wavelength (nm)")
        ax.set_ylabel("flux")
        ax.set_title("Diagnostic spectrum preview")
    else:
        gap = config["geometry"]["gap_thickness_nm"]
        radius = config["geometry"]["particle_radius_nm"]
        film = config["geometry"]["film_thickness_nm"]
        ax.add_patch(plt.Rectangle((-80, 0), 160, film, color="#c19a39", alpha=0.8))
        ax.add_patch(plt.Circle((0, film + gap + radius), radius, color="#d8a300", alpha=0.9))
        ax.set_aspect("equal", adjustable="box")
        ax.set_title("Diagnostic geometry preview")
        ax.set_xlabel("x (nm)")
        ax.set_ylabel("z (nm)")
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)
    return ""


def _analyze_flux_surfaces_csv(path: Path) -> list[FluxMonitorSummary]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            return [
                FluxMonitorSummary(
                    monitor="flux_surfaces",
                    n_points=0,
                    anomaly=True,
                    notes=["flux_surfaces.csv is missing a header."],
                )
            ]
        wavelength_column = "wavelength_nm" if "wavelength_nm" in reader.fieldnames else ""
        flux_columns = [name for name in reader.fieldnames if name.startswith("flux_")]
        values: dict[str, list[float]] = {name: [] for name in flux_columns}
        wavelengths: list[float] = []
        notes: dict[str, list[str]] = {name: [] for name in flux_columns}
        for row_number, row in enumerate(reader, start=2):
            if wavelength_column:
                parsed_wavelength = _parse_optional_float(row.get(wavelength_column))
                if parsed_wavelength is not None:
                    wavelengths.append(parsed_wavelength)
            for column in flux_columns:
                parsed = _parse_optional_float(row.get(column))
                if parsed is None:
                    notes[column].append(f"non-numeric value at row {row_number}")
                elif math.isnan(parsed) or math.isinf(parsed):
                    notes[column].append(f"NaN/Inf at row {row_number}")
                else:
                    values[column].append(parsed)

    summaries: list[FluxMonitorSummary] = []
    for column, column_values in values.items():
        integrated_abs = None
        integrated_signed = None
        if len(wavelengths) == len(column_values) and len(wavelengths) > 1:
            pairs = sorted(zip(wavelengths, column_values), key=lambda item: item[0])
            sorted_wavelengths = [item[0] for item in pairs]
            sorted_values = [item[1] for item in pairs]
            integrated_abs = _trapz(sorted_wavelengths, [abs(value) for value in sorted_values])
            integrated_signed = _trapz(sorted_wavelengths, sorted_values)
        max_abs = max((abs(value) for value in column_values), default=None)
        near_zero = max_abs is not None and max_abs < 1e-15
        anomaly = near_zero or bool(notes[column])
        column_notes = notes[column].copy()
        if near_zero:
            column_notes.append("near-zero flux signal")
        summaries.append(
            FluxMonitorSummary(
                monitor=column,
                n_points=len(column_values),
                mean_flux=_mean(column_values),
                max_abs_flux=max_abs,
                integrated_abs_flux=integrated_abs,
                integrated_signed_flux=integrated_signed,
                near_zero_signal=near_zero,
                anomaly=anomaly,
                notes=column_notes,
            )
        )
    return summaries


def _write_simple_png_preview(
    path: Path,
    *,
    spectrum: SpectrumData | None,
    config: dict[str, Any],
) -> None:
    width = 900
    height = 520
    image = bytearray([255, 255, 255] * width * height)

    def draw_pixel(x: int, y: int, color: tuple[int, int, int]) -> None:
        if 0 <= x < width and 0 <= y < height:
            idx = (y * width + x) * 3
            image[idx:idx + 3] = bytes(color)

    def draw_line(x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]) -> None:
        dx = abs(x1 - x0)
        dy = -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            draw_pixel(x0, y0, color)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def draw_rect(x0: int, y0: int, x1: int, y1: int, color: tuple[int, int, int]) -> None:
        for y in range(max(0, y0), min(height, y1)):
            for x in range(max(0, x0), min(width, x1)):
                draw_pixel(x, y, color)

    def draw_circle(cx: int, cy: int, radius: int, color: tuple[int, int, int]) -> None:
        r2 = radius * radius
        for y in range(cy - radius, cy + radius + 1):
            for x in range(cx - radius, cx + radius + 1):
                if (x - cx) * (x - cx) + (y - cy) * (y - cy) <= r2:
                    draw_pixel(x, y, color)

    axis_color = (40, 40, 40)
    if spectrum:
        x0, y0, x1, y1 = 80, 420, 840, 70
        draw_line(x0, y0, x1, y0, axis_color)
        draw_line(x0, y0, x0, y1, axis_color)
        min_wl, max_wl = min(spectrum.wavelength_nm), max(spectrum.wavelength_nm)
        min_flux, max_flux = min(spectrum.flux), max(spectrum.flux)
        if max_flux == min_flux:
            max_flux = min_flux + 1.0
        points: list[tuple[int, int]] = []
        for wl, flux in zip(spectrum.wavelength_nm, spectrum.flux):
            px = x0 + int((wl - min_wl) / (max_wl - min_wl or 1.0) * (x1 - x0))
            py = y0 - int((flux - min_flux) / (max_flux - min_flux) * (y0 - y1))
            points.append((px, py))
        for start, end in zip(points, points[1:]):
            draw_line(start[0], start[1], end[0], end[1], (0, 92, 175))
    else:
        draw_rect(120, 360, 780, 430, (190, 154, 57))
        radius = max(24, min(90, int(config["geometry"]["particle_radius_nm"])))
        draw_circle(450, 250, radius, (218, 163, 0))
        draw_line(350, 345, 550, 345, (0, 92, 175))
    _write_png_rgb(path, width, height, bytes(image))


def _write_png_rgb(path: Path, width: int, height: int, rgb: bytes) -> None:
    def chunk(chunk_type: bytes, data: bytes) -> bytes:
        return (
            struct.pack(">I", len(data))
            + chunk_type
            + data
            + struct.pack(">I", zlib.crc32(chunk_type + data) & 0xFFFFFFFF)
        )

    raw = b"".join(
        b"\x00" + rgb[y * width * 3:(y + 1) * width * 3]
        for y in range(height)
    )
    path.write_bytes(
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + chunk(b"IDAT", zlib.compress(raw, level=6))
        + chunk(b"IEND", b"")
    )


def _write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, Any]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def _existing_path(path: Path | None) -> Path | None:
    if path is None:
        return None
    path = Path(path)
    return path if path.exists() else None


def _unwrap(value: Any) -> Any:
    if isinstance(value, StatusField):
        return value.value
    return value


def _jsonable(value: Any) -> Any:
    value = _unwrap(value)
    if isinstance(value, BaseModel):
        return value.model_dump()
    if isinstance(value, list):
        return [_jsonable(item) for item in value]
    if isinstance(value, dict):
        return {key: _jsonable(item) for key, item in value.items()}
    return value


def _model_or_dict_get(value: Any, key: str, default: Any = None) -> Any:
    value = _unwrap(value)
    if isinstance(value, BaseModel):
        return getattr(value, key, default)
    if isinstance(value, dict):
        return value.get(key, default)
    return default


def _dict_get_any(value: Any, keys: list[str]) -> Any:
    if not isinstance(value, dict):
        return None
    for key in keys:
        if key in value:
            return value[key]
    return None


def _first_numeric(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    match = re.search(r"(-?\d+(?:\.\d+)?)", str(value))
    return float(match.group(1)) if match else None


def _gap_from_key_parameters(values: Any) -> float | None:
    if not isinstance(values, list):
        return None
    for item in values:
        text = str(item).lower()
        if "gap" in text or "间隙" in text:
            parsed = _first_numeric(text)
            if parsed is not None:
                return parsed
    return None


def _gap_from_sweep(value: Any) -> float | None:
    variable = _model_or_dict_get(value, "variable", "")
    if variable == "gap_nm":
        return _model_or_dict_get(value, "range_start", None)
    return None


def _extract_mesh_resolution(mesh: Any, fallback: float) -> tuple[float, str]:
    description = str(_model_or_dict_get(mesh, "description", ""))
    parsed = _first_numeric(description)
    if parsed is not None and ("px/um" in description or "px/μm" in description):
        return parsed, "spec.mesh_setting.description"
    return fallback, "diagnostic_default"


def _parse_optional_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def _trapz(x_values: list[float], y_values: list[float]) -> float | None:
    if len(x_values) < 2:
        return None
    return sum(
        0.5 * (y_values[idx] + y_values[idx - 1]) * (x_values[idx] - x_values[idx - 1])
        for idx in range(1, len(x_values))
    )


def _mesh_unit(metric: str) -> str:
    if metric == "resolution_px_per_um" or metric.startswith("recommended_resolution"):
        return "px/um"
    if metric.endswith("_nm"):
        return "nm"
    if metric.endswith("_um"):
        return "um"
    if metric.endswith("_cells"):
        return "cells"
    return ""


def _missing_run_artifacts(artifact_dir: Path | None) -> list[str]:
    if artifact_dir is None:
        return []
    required = ["stdout.txt", "stderr.txt", "execution_result.json", "run_manifest.json"]
    return [name for name in required if not (artifact_dir / name).exists()]


def _diagnostic_status(
    *,
    errors: list[str],
    warnings: list[str],
    missing_artifacts: list[str],
) -> str:
    if errors:
        return "error"
    if warnings or missing_artifacts:
        return "warning"
    return "success"


def _monitor_base_name(name: str) -> str:
    if name.startswith("flux_"):
        return "flux"
    return name


def _monitor_surface_name(name: str) -> str:
    if name.startswith("flux_"):
        return name.removeprefix("flux_")
    return name


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result
