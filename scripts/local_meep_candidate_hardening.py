"""Manual/local v0.6 physical candidate hardening matrix.

This script is intentionally not part of default CI. It stress-tests the
current v0.6 physical-candidate profile with bounded repeatability,
runtime, modest resolution/frequency, and polarization checks.
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
from optical_spec_agent.execution import check_csv_numeric_sanity, check_meep_available, run_meep_script
from optical_spec_agent.execution.meep_runner import parse_postprocess_results
from optical_spec_agent.services.spec_service import SpecService


CORE_MEEP_CASE = (
    "用 Meep FDTD 仿真 80 nm 金纳米球放在 100 nm 金膜上，中间 SiO2 gap 为 5 nm，"
    "平面波正入射，波长范围 400-900 nm，输出散射谱，提取共振波长和 FWHM。"
)


@dataclass(frozen=True)
class HardeningCase:
    case_name: str
    source_component: str = "Ex"
    boundary_type: str = "absorber"
    material_mode: str = "library"
    flux_mode: str = "closed_box"
    courant: float = 0.1
    resolution: int = 12
    freq_points: int = 10
    fixed_run_time: float = 50
    physical_interpretation_level: str = "physical_candidate"


def _make_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"candidate-hardening-{timestamp}-{uuid4().hex[:8]}"


def _hardening_cases() -> list[HardeningCase]:
    return [
        HardeningCase(case_name="repeat-1"),
        HardeningCase(case_name="repeat-2"),
        HardeningCase(case_name="repeat-3"),
        HardeningCase(case_name="runtime-100", fixed_run_time=100),
        HardeningCase(case_name="runtime-200", fixed_run_time=200),
        HardeningCase(case_name="resolution-16-freq-10", resolution=16, freq_points=10),
        HardeningCase(case_name="resolution-12-freq-20", resolution=12, freq_points=20),
        HardeningCase(case_name="resolution-16-freq-20", resolution=16, freq_points=20),
        HardeningCase(case_name="polarization-ey", source_component="Ey"),
    ]


def _select_cases(args: argparse.Namespace) -> list[HardeningCase]:
    cases = _hardening_cases()
    if args.repeatability_only:
        cases = [case for case in cases if case.case_name.startswith("repeat-")]
    if args.only:
        cases = [case for case in cases if case.case_name == args.only]
    return cases


def _postprocess_json_valid_object(workdir: Path) -> bool:
    try:
        parsed = parse_postprocess_results(workdir)
    except (OSError, json.JSONDecodeError):
        return False
    return isinstance(parsed, dict)


def _write_summary(path: Path, summary: dict) -> None:
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local/manual v0.6 candidate hardening matrix.")
    parser.add_argument("--timeout", type=int, default=900, help="Per-case timeout in seconds.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT / "runs" / "candidate-hardening",
        help="Root directory for candidate hardening artifacts.",
    )
    parser.add_argument("--repeatability-only", action="store_true", help="Run only repeat-1/2/3 cases.")
    parser.add_argument(
        "--only",
        choices=[case.case_name for case in _hardening_cases()],
        help="Run one selected hardening case.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the selected matrix without importing or running Meep.",
    )
    args = parser.parse_args(argv)

    matrix_run_id = _make_run_id()
    run_root = args.output_root / matrix_run_id
    run_root.mkdir(parents=True, exist_ok=True)
    summary_path = run_root / "candidate_hardening_summary.json"
    selected_cases = _select_cases(args)

    summary: dict = {
        "schema_version": "meep_candidate_hardening.v0.1",
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
                "csv_has_nan_or_inf": None,
                "csv_sanity": None,
                "postprocess_json_valid_object": None,
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
        print("Meep is not available; candidate hardening skipped.", file=sys.stderr)
        return 2

    spec = SpecService().process(CORE_MEEP_CASE, task_id=matrix_run_id)
    adapter = MeepAdapter()

    for case in selected_cases:
        case_dir = run_root / case.case_name
        case_dir.mkdir(parents=True, exist_ok=True)
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
        csv_sanity = check_csv_numeric_sanity(case_dir / "scattering_spectrum.csv").to_dict()
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
            "csv_has_nan_or_inf": any("NaN" in err or "Inf" in err for err in csv_sanity["errors"]),
            "csv_sanity": csv_sanity,
            "postprocess_json_valid_object": _postprocess_json_valid_object(case_dir),
        }
        summary["cases"].append(case_summary)
        _write_summary(summary_path, summary)

    _write_summary(summary_path, summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
