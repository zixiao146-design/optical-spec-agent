"""Manual/local Meep stability diagnostics matrix.

This script is intentionally not part of the default CI gate. It generates a
small matrix of Meep scripts for the core nanoparticle-on-film case and runs
them through the optional execution harness. Research-preview failures are
reported as diagnostics by default rather than hidden or promoted to success.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
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
class StabilityCase:
    case_id: str
    script_mode: str
    expected_mode: str
    boundary_type: str = "pml"
    material_mode: str = "library"
    diagnostic_profile: str = "normal"
    courant: float | None = None
    eps_averaging: bool | None = None
    resolution: int = 50
    freq_points: int = 200
    physical_interpretation: bool = False
    timeout_kind: str = "research"


def _make_run_id() -> str:
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    return f"stability-matrix-{timestamp}-{uuid4().hex[:8]}"


def _matrix_cases() -> list[StabilityCase]:
    return [
        StabilityCase(
            case_id="smoke",
            script_mode="smoke",
            expected_mode="smoke",
            timeout_kind="smoke",
        ),
        StabilityCase(
            case_id="research_preview_pml_library",
            script_mode="research-preview",
            expected_mode="research-preview",
            boundary_type="pml",
            material_mode="library",
            physical_interpretation=True,
        ),
        StabilityCase(
            case_id="research_preview_absorber_library",
            script_mode="research-preview",
            expected_mode="research-preview",
            boundary_type="absorber",
            material_mode="library",
            physical_interpretation=True,
        ),
        StabilityCase(
            case_id="research_preview_absorber_library_courant_025",
            script_mode="research-preview",
            expected_mode="research-preview",
            boundary_type="absorber",
            material_mode="library",
            courant=0.25,
            physical_interpretation=True,
        ),
        StabilityCase(
            case_id="research_preview_absorber_dielectric_sanity",
            script_mode="research-preview",
            expected_mode="research-preview",
            boundary_type="absorber",
            material_mode="dielectric_sanity",
        ),
        StabilityCase(
            case_id="research_preview_low_cost_dielectric_sanity",
            script_mode="research-preview",
            expected_mode="research-preview",
            boundary_type="absorber",
            material_mode="dielectric_sanity",
            diagnostic_profile="low_cost",
            courant=0.25,
            resolution=8,
            freq_points=5,
        ),
    ]


def _select_cases(args: argparse.Namespace) -> list[StabilityCase]:
    cases = _matrix_cases()
    if args.skip_research:
        cases = [case for case in cases if case.expected_mode == "smoke"]
    if args.only:
        aliases = {
            "smoke": "smoke",
            "pml-library": "research_preview_pml_library",
            "absorber-library": "research_preview_absorber_library",
            "absorber-library-courant-025": "research_preview_absorber_library_courant_025",
            "dielectric-sanity": "research_preview_absorber_dielectric_sanity",
            "low-cost-dielectric-sanity": "research_preview_low_cost_dielectric_sanity",
        }
        selected_id = aliases[args.only]
        cases = [case for case in cases if case.case_id == selected_id]
    return cases


def _case_timeout(case: StabilityCase, *, timeout_smoke: int, timeout_research: int) -> int:
    return timeout_smoke if case.timeout_kind == "smoke" else timeout_research


def _write_summary(path: Path, summary: dict) -> None:
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run local/manual Meep stability diagnostics matrix.")
    parser.add_argument("--timeout-smoke", type=int, default=300, help="Smoke case timeout in seconds.")
    parser.add_argument("--timeout-research", type=int, default=3600, help="Research-preview case timeout in seconds.")
    parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT / "runs" / "stability-matrix",
        help="Root directory for stability matrix artifacts.",
    )
    parser.add_argument(
        "--skip-research",
        action="store_true",
        help="Run only the smoke case. Useful when Meep is available but long research diagnostics are not desired.",
    )
    parser.add_argument(
        "--only",
        choices=[
            "smoke",
            "pml-library",
            "absorber-library",
            "absorber-library-courant-025",
            "dielectric-sanity",
            "low-cost-dielectric-sanity",
        ],
        help="Run one selected matrix case.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Return exit code 1 if any selected research-preview case fails.",
    )
    args = parser.parse_args(argv)

    run_id = _make_run_id()
    run_root = args.output_root / run_id
    run_root.mkdir(parents=True, exist_ok=True)
    summary_path = run_root / "stability_matrix_summary.json"

    availability = check_meep_available()
    summary: dict = {
        "schema_version": "meep_stability_matrix.v0.1",
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "core_input": CORE_MEEP_CASE,
        "output_root": str(run_root),
        "meep_available": availability.available,
        "meep_command": availability.command,
        "cases": [],
    }

    if not availability.available:
        summary["errors"] = availability.errors
        summary["warnings"] = availability.warnings
        _write_summary(summary_path, summary)
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        print("Meep is not available; stability matrix skipped.", file=sys.stderr)
        return 2

    spec = SpecService().process(CORE_MEEP_CASE, task_id=run_id)
    adapter = MeepAdapter()
    selected_cases = _select_cases(args)

    for case in selected_cases:
        case_dir = run_root / case.case_id
        case_dir.mkdir(parents=True, exist_ok=True)
        script = adapter.generate(
            spec,
            script_mode=case.script_mode,
            boundary_type=case.boundary_type,
            courant=case.courant,
            eps_averaging=case.eps_averaging,
            material_mode=case.material_mode,
            diagnostic_profile=case.diagnostic_profile,
        ).content
        script_path = case_dir / "generated_script.py"
        script_path.write_text(script, encoding="utf-8")

        result = run_meep_script(
            script_path=script_path,
            workdir=case_dir,
            timeout=_case_timeout(
                case,
                timeout_smoke=args.timeout_smoke,
                timeout_research=args.timeout_research,
            ),
            expected_mode=case.expected_mode,
            save_artifacts=True,
            run_id=f"{run_id}-{case.case_id}",
        )
        summary["cases"].append(
            {
                "case_id": case.case_id,
                "case_name": case.case_id,
                "script_mode": case.script_mode,
                "diagnostic_profile": case.diagnostic_profile,
                "expected_mode": case.expected_mode,
                "boundary_type": case.boundary_type,
                "material_mode": case.material_mode,
                "courant": case.courant,
                "eps_averaging": case.eps_averaging,
                "resolution": case.resolution,
                "freq_points": case.freq_points,
                "timeout_seconds": _case_timeout(
                    case,
                    timeout_smoke=args.timeout_smoke,
                    timeout_research=args.timeout_research,
                ),
                "workdir": str(case_dir),
                "artifact_dir": str(case_dir),
                "success": result.success,
                "available": result.available,
                "returncode": result.returncode,
                "outputs": result.outputs,
                "missing_outputs": result.missing_outputs,
                "errors": result.errors,
                "warnings": result.warnings,
                "physical_interpretation": case.physical_interpretation,
                "recommended_for_execution_pipeline_debug": (
                    case.diagnostic_profile == "low_cost" and result.success
                ),
            }
        )
        _write_summary(summary_path, summary)

    smoke_cases = [case for case in summary["cases"] if case["expected_mode"] == "smoke"]
    research_cases = [case for case in summary["cases"] if case["expected_mode"] == "research-preview"]
    smoke_failed = any(not case["success"] for case in smoke_cases)
    research_failed = any(not case["success"] for case in research_cases)

    _write_summary(summary_path, summary)
    print(json.dumps(summary, indent=2, ensure_ascii=False))

    if smoke_failed:
        return 1
    if args.strict and research_failed:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
