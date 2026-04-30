"""Manual/local v0.6 physical stability pre-study probe.

This script is intentionally not part of default CI. It runs a bounded set of
research-preview Meep profiles to diagnose why library Au configurations fail
with NaN/Inf or timeout. It records artifacts under
runs/physical-stability-probe/<matrix_run_id>/<case_name>/.
"""

from __future__ import annotations

import argparse
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
from optical_spec_agent.execution import check_meep_available, run_meep_script
from optical_spec_agent.services.spec_service import SpecService


CORE_MEEP_CASE = (
    "用 Meep FDTD 仿真 80 nm 金纳米球放在 100 nm 金膜上，中间 SiO2 gap 为 5 nm，"
    "平面波正入射，波长范围 400-900 nm，输出散射谱，提取共振波长和 FWHM。"
)


@dataclass(frozen=True)
class ProbeCase:
    case_name: str
    diagnostic_profile: str
    source_component: str
    boundary_type: str
    material_mode: str
    flux_mode: str
    courant: float | None
    eps_averaging: bool | None
    resolution: int
    freq_points: int
    stop_strategy: str
    fixed_run_time: float | None
    decay_threshold: float | None
    expected_mode: str = "research-preview"
    physical_interpretation_level: str = "diagnostic"


def _make_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"physical-probe-{timestamp}-{uuid4().hex[:8]}"


def _probe_cases() -> list[ProbeCase]:
    return [
        ProbeCase(
            case_name="low-cost-dielectric-sanity-control",
            diagnostic_profile="low_cost",
            source_component="Ez",
            boundary_type="absorber",
            material_mode="dielectric_sanity",
            flux_mode="closed_box",
            courant=0.25,
            eps_averaging=None,
            resolution=8,
            freq_points=5,
            stop_strategy="fixed",
            fixed_run_time=30,
            decay_threshold=1e-3,
            physical_interpretation_level="none",
        ),
        ProbeCase(
            case_name="source-ex-absorber-library-courant-025-fixed-50",
            diagnostic_profile="physical_probe",
            source_component="Ex",
            boundary_type="absorber",
            material_mode="library",
            flux_mode="closed_box",
            courant=0.25,
            eps_averaging=None,
            resolution=12,
            freq_points=10,
            stop_strategy="fixed",
            fixed_run_time=50,
            decay_threshold=1e-3,
            physical_interpretation_level="physical_candidate",
        ),
        ProbeCase(
            case_name="source-ex-absorber-library-courant-01-fixed-50",
            diagnostic_profile="physical_probe",
            source_component="Ex",
            boundary_type="absorber",
            material_mode="library",
            flux_mode="closed_box",
            courant=0.1,
            eps_averaging=None,
            resolution=12,
            freq_points=10,
            stop_strategy="fixed",
            fixed_run_time=50,
            decay_threshold=1e-3,
            physical_interpretation_level="physical_candidate",
        ),
        ProbeCase(
            case_name="source-ex-absorber-library-epsavg-false-fixed-50",
            diagnostic_profile="physical_probe",
            source_component="Ex",
            boundary_type="absorber",
            material_mode="library",
            flux_mode="closed_box",
            courant=0.25,
            eps_averaging=False,
            resolution=12,
            freq_points=10,
            stop_strategy="fixed",
            fixed_run_time=50,
            decay_threshold=1e-3,
            physical_interpretation_level="physical_candidate",
        ),
        ProbeCase(
            case_name="source-ex-absorber-library-single-plane-fixed-50",
            diagnostic_profile="physical_probe",
            source_component="Ex",
            boundary_type="absorber",
            material_mode="library",
            flux_mode="single_plane",
            courant=0.25,
            eps_averaging=None,
            resolution=12,
            freq_points=10,
            stop_strategy="fixed",
            fixed_run_time=50,
            decay_threshold=1e-3,
            physical_interpretation_level="diagnostic",
        ),
        ProbeCase(
            case_name="particle-library-film-dielectric-fixed-50",
            diagnostic_profile="physical_probe",
            source_component="Ex",
            boundary_type="absorber",
            material_mode="particle_library_film_dielectric",
            flux_mode="closed_box",
            courant=0.25,
            eps_averaging=None,
            resolution=12,
            freq_points=10,
            stop_strategy="fixed",
            fixed_run_time=50,
            decay_threshold=1e-3,
            physical_interpretation_level="diagnostic",
        ),
        ProbeCase(
            case_name="particle-dielectric-film-library-fixed-50",
            diagnostic_profile="physical_probe",
            source_component="Ex",
            boundary_type="absorber",
            material_mode="particle_dielectric_film_library",
            flux_mode="closed_box",
            courant=0.25,
            eps_averaging=None,
            resolution=12,
            freq_points=10,
            stop_strategy="fixed",
            fixed_run_time=50,
            decay_threshold=1e-3,
            physical_interpretation_level="diagnostic",
        ),
        ProbeCase(
            case_name="lower-resolution-library-fixed-50",
            diagnostic_profile="physical_probe",
            source_component="Ex",
            boundary_type="absorber",
            material_mode="library",
            flux_mode="closed_box",
            courant=0.25,
            eps_averaging=None,
            resolution=8,
            freq_points=5,
            stop_strategy="fixed",
            fixed_run_time=50,
            decay_threshold=1e-3,
            physical_interpretation_level="physical_candidate",
        ),
    ]


def _select_cases(args: argparse.Namespace) -> list[ProbeCase]:
    cases = _probe_cases()
    if args.quick:
        quick_names = {
            "low-cost-dielectric-sanity-control",
            "source-ex-absorber-library-courant-025-fixed-50",
            "source-ex-absorber-library-courant-01-fixed-50",
            "source-ex-absorber-library-epsavg-false-fixed-50",
            "source-ex-absorber-library-single-plane-fixed-50",
        }
        cases = [case for case in cases if case.case_name in quick_names]
    if args.only:
        cases = [case for case in cases if case.case_name == args.only]
    return cases


def _recommended_next_step(case: ProbeCase, success: bool, errors: list[str]) -> str:
    if success and case.physical_interpretation_level == "physical_candidate":
        return "repeat this profile once to check reproducibility"
    if success:
        return "use as diagnostic evidence only; do not interpret physically"
    if any("NaN" in err or "Inf" in err for err in errors):
        return "inspect source/material/boundary stability for field blow-up"
    if any("timed out" in err for err in errors):
        return "try lower resolution, fewer frequency points, or shorter fixed_run_time"
    return "inspect stderr and generated script"


def _write_summary(path: Path, summary: dict) -> None:
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local/manual v0.6 physical stability probes.")
    parser.add_argument("--timeout", type=int, default=900, help="Per-case timeout in seconds.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT / "runs" / "physical-stability-probe",
        help="Root directory for physical stability probe artifacts.",
    )
    parser.add_argument("--quick", action="store_true", help="Run the bounded quick probe subset.")
    parser.add_argument(
        "--only",
        choices=[case.case_name for case in _probe_cases()],
        help="Run one selected probe case.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the selected probe matrix without importing or running Meep.",
    )
    args = parser.parse_args(argv)

    matrix_run_id = _make_run_id()
    run_root = args.output_root / matrix_run_id
    run_root.mkdir(parents=True, exist_ok=True)
    summary_path = run_root / "physical_stability_summary.json"

    selected_cases = _select_cases(args)
    summary: dict = {
        "schema_version": "meep_physical_stability_probe.v0.1",
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
                "missing_outputs": [],
                "outputs": {},
                "errors": [],
                "warnings": [],
                "artifact_dir": str(run_root / case.case_name),
                "recommended_next_step": "dry run only",
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
        print("Meep is not available; physical stability probe skipped.", file=sys.stderr)
        return 2

    spec = SpecService().process(CORE_MEEP_CASE, task_id=matrix_run_id)
    adapter = MeepAdapter()

    for case in selected_cases:
        case_dir = run_root / case.case_name
        case_dir.mkdir(parents=True, exist_ok=True)
        script = adapter.generate(
            spec,
            script_mode="research-preview",
            boundary_type=case.boundary_type,
            courant=case.courant,
            eps_averaging=case.eps_averaging,
            material_mode=case.material_mode,
            diagnostic_profile=case.diagnostic_profile,
            source_component=case.source_component,
            stop_strategy=case.stop_strategy,
            fixed_run_time=case.fixed_run_time,
            decay_threshold=case.decay_threshold,
            flux_mode=case.flux_mode,
            resolution=case.resolution,
            freq_points=case.freq_points,
        ).content
        script_path = case_dir / "generated_script.py"
        script_path.write_text(script, encoding="utf-8")

        result = run_meep_script(
            script_path=script_path,
            workdir=case_dir,
            timeout=args.timeout,
            expected_mode=case.expected_mode,
            save_artifacts=True,
            run_id=f"{matrix_run_id}-{case.case_name}",
        )
        case_summary = {
            **asdict(case),
            "timeout": args.timeout,
            "success": result.success,
            "returncode": result.returncode,
            "missing_outputs": result.missing_outputs,
            "outputs": result.outputs,
            "errors": result.errors,
            "warnings": result.warnings,
            "artifact_dir": str(case_dir),
            "recommended_next_step": _recommended_next_step(case, result.success, result.errors),
        }
        summary["cases"].append(case_summary)
        _write_summary(summary_path, summary)

    _write_summary(summary_path, summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
