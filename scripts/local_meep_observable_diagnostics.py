"""Manual/local v0.6 observable diagnostics for Meep research-preview scripts.

This script is intentionally not part of default CI. It runs a small bounded
matrix to diagnose whether the current flux observable produces interpretable
signals for the v0.6 physical-candidate profile.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from optical_spec_agent.adapters.meep import MeepAdapter
from optical_spec_agent.analysis import analyze_flux_signal, load_scattering_csv
from optical_spec_agent.execution import check_meep_available, run_meep_script
from optical_spec_agent.execution.meep_runner import parse_postprocess_results
from optical_spec_agent.services.spec_service import SpecService


CORE_MEEP_CASE = (
    "用 Meep FDTD 仿真 80 nm 金纳米球放在 100 nm 金膜上，中间 SiO2 gap 为 5 nm，"
    "平面波正入射，波长范围 400-900 nm，输出散射谱，提取共振波长和 FWHM。"
)


@dataclass(frozen=True)
class ObservableCase:
    case_name: str
    flux_mode: str
    supported: bool = True
    source_component: str = "Ex"
    boundary_type: str = "absorber"
    material_mode: str = "library"
    courant: float = 0.1
    resolution: int = 12
    freq_points: int = 10
    fixed_run_time: float = 50
    note: str = ""


def _make_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"observable-diagnostics-{timestamp}-{uuid4().hex[:8]}"


def _observable_cases() -> list[ObservableCase]:
    return [
        ObservableCase(case_name="closed-box-baseline", flux_mode="closed_box"),
        ObservableCase(case_name="top-plane", flux_mode="top_plane"),
        ObservableCase(
            case_name="closed-box-larger-clearance",
            flux_mode="closed_box",
            supported=False,
            note="unsupported until flux_box_padding/flux_box_scale is exposed",
        ),
        ObservableCase(case_name="single-plane", flux_mode="single_plane"),
    ]


def _select_cases(args: argparse.Namespace) -> list[ObservableCase]:
    cases = _observable_cases()
    if args.only:
        cases = [case for case in cases if case.case_name == args.only]
    return cases


def _read_postprocess(workdir: Path) -> dict:
    try:
        parsed = parse_postprocess_results(workdir)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {}
    return parsed if isinstance(parsed, dict) else {}


def _analyze_flux_surfaces(path: Path) -> dict:
    if not path.exists():
        return {"available": False}
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        return {"available": True, "rows": 0, "surfaces": {}, "cancellation_ratio": None}

    surface_columns = [
        column for column in rows[0]
        if column not in ("wavelength_nm", "flux_total")
    ]
    surfaces: dict[str, dict] = {}
    component_abs_sum = 0.0
    total_abs_sum = 0.0
    for column in surface_columns:
        values = [
            float(row[column])
            for row in rows
            if row.get(column) not in (None, "")
        ]
        if not values:
            continue
        surfaces[column] = {
            "max_abs_flux": max(abs(value) for value in values),
            "signed_sum": sum(values),
            "abs_sum": sum(abs(value) for value in values),
        }
        component_abs_sum += surfaces[column]["abs_sum"]

    total_values = [
        float(row["flux_total"])
        for row in rows
        if row.get("flux_total") not in (None, "")
    ]
    if total_values:
        total_abs_sum = sum(abs(value) for value in total_values)

    cancellation_ratio = None
    if component_abs_sum > 0.0:
        cancellation_ratio = total_abs_sum / component_abs_sum

    return {
        "available": True,
        "rows": len(rows),
        "surfaces": surfaces,
        "total_abs_sum": total_abs_sum,
        "component_abs_sum": component_abs_sum,
        "cancellation_ratio": cancellation_ratio,
    }


def _summarize_successful_case(case: ObservableCase, case_dir: Path, result) -> dict:
    spectrum_path = case_dir / "scattering_spectrum.csv"
    postprocess = _read_postprocess(case_dir)
    geometry = postprocess.get("geometry_diagnostics", {})
    flux_signal = {}
    if spectrum_path.exists():
        try:
            flux_signal = analyze_flux_signal(load_scattering_csv(spectrum_path))
        except ValueError as exc:
            flux_signal = {"error": str(exc)}

    return {
        **asdict(case),
        "success": result.success,
        "returncode": result.returncode,
        "outputs": result.outputs,
        "missing_outputs": result.missing_outputs,
        "errors": result.errors,
        "warnings": result.warnings,
        "artifact_dir": str(case_dir),
        "max_abs_flux": flux_signal.get("max_abs_flux"),
        "integrated_abs_flux": flux_signal.get("integrated_abs_flux"),
        "integrated_signed_flux": flux_signal.get("integrated_signed_flux"),
        "flux_total_near_zero": flux_signal.get("near_zero_signal"),
        "flux_signal": flux_signal,
        "has_flux_surfaces_csv": (case_dir / "flux_surfaces.csv").exists(),
        "flux_surfaces": _analyze_flux_surfaces(case_dir / "flux_surfaces.csv"),
        "flux_box_intersects_film": geometry.get("flux_box_intersects_film"),
        "flux_box_intersects_particle": geometry.get("flux_box_intersects_particle"),
        "flux_box_encloses_particle": geometry.get("flux_box_encloses_particle"),
        "geometry_diagnostics": geometry,
    }


def _unsupported_summary(case: ObservableCase, case_dir: Path, timeout: int) -> dict:
    return {
        **asdict(case),
        "timeout": timeout,
        "success": None,
        "returncode": None,
        "outputs": {},
        "missing_outputs": [],
        "errors": ["unsupported observable diagnostic profile"],
        "warnings": [case.note] if case.note else [],
        "artifact_dir": str(case_dir),
        "max_abs_flux": None,
        "integrated_abs_flux": None,
        "integrated_signed_flux": None,
        "flux_total_near_zero": None,
        "has_flux_surfaces_csv": False,
        "flux_box_intersects_film": None,
    }


def _write_summary(path: Path, summary: dict) -> None:
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local/manual v0.6 observable diagnostics.")
    parser.add_argument("--timeout", type=int, default=900, help="Per-case timeout in seconds.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT / "runs" / "observable-diagnostics",
        help="Root directory for observable diagnostics artifacts.",
    )
    parser.add_argument(
        "--only",
        choices=[case.case_name for case in _observable_cases()],
        help="Run one selected observable diagnostic case.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the selected observable matrix without importing or running Meep.",
    )
    args = parser.parse_args(argv)

    matrix_run_id = _make_run_id()
    run_root = args.output_root / matrix_run_id
    run_root.mkdir(parents=True, exist_ok=True)
    summary_path = run_root / "observable_diagnostics_summary.json"
    selected_cases = _select_cases(args)

    summary: dict = {
        "schema_version": "meep_observable_diagnostics.v0.1",
        "matrix_run_id": matrix_run_id,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "core_input": CORE_MEEP_CASE,
        "output_root": str(run_root),
        "dry_run": args.dry_run,
        "cases": [],
    }

    if args.dry_run:
        summary["cases"] = [
            {
                **asdict(case),
                "timeout": args.timeout,
                "success": None,
                "returncode": None,
                "outputs": {},
                "missing_outputs": [],
                "errors": [] if case.supported else ["unsupported observable diagnostic profile"],
                "warnings": [case.note] if case.note else [],
                "artifact_dir": str(run_root / case.case_name),
            }
            for case in selected_cases
        ]
        _write_summary(summary_path, summary)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0

    availability = check_meep_available()
    summary["meep_available"] = availability.available
    summary["meep_command"] = availability.command
    if not availability.available:
        summary["errors"] = availability.errors
        summary["warnings"] = availability.warnings
        _write_summary(summary_path, summary)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        print("Meep is not available; observable diagnostics skipped.", file=sys.stderr)
        return 2

    spec = SpecService().process(CORE_MEEP_CASE, task_id=matrix_run_id)
    adapter = MeepAdapter()

    for case in selected_cases:
        case_dir = run_root / case.case_name
        case_dir.mkdir(parents=True, exist_ok=True)

        if not case.supported:
            summary["cases"].append(_unsupported_summary(case, case_dir, args.timeout))
            _write_summary(summary_path, summary)
            continue

        script = adapter.generate(
            spec,
            script_mode="research-preview",
            diagnostic_profile="physical_probe",
            source_component=case.source_component,
            boundary_type=case.boundary_type,
            material_mode=case.material_mode,
            flux_mode=case.flux_mode,
            courant=case.courant,
            resolution=case.resolution,
            freq_points=case.freq_points,
            stop_strategy="fixed",
            fixed_run_time=case.fixed_run_time,
            decay_threshold=1e-3,
        ).content
        script_path = case_dir / "generated_script.py"
        script_path.write_text(script, encoding="utf-8")

        result = run_meep_script(
            script_path=script_path,
            workdir=case_dir,
            timeout=args.timeout,
            expected_mode="research-preview",
            save_artifacts=True,
            run_id=f"{matrix_run_id}-{case.case_name}",
        )
        case_summary = _summarize_successful_case(case, case_dir, result)
        case_summary["timeout"] = args.timeout
        summary["cases"].append(case_summary)
        _write_summary(summary_path, summary)

    _write_summary(summary_path, summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
