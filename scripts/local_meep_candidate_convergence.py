"""Manual/local v0.6 candidate spectrum convergence analysis.

This script analyzes existing candidate-hardening artifacts. It does not run
Meep by default. Use --run-matrix explicitly if fresh artifacts are needed.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from optical_spec_agent.analysis import compare_spectra, load_scattering_csv, summarize_comparisons


DEFAULT_CASES = [
    "repeat-2",
    "repeat-3",
    "runtime-100",
    "runtime-200",
    "resolution-16-freq-10",
    "resolution-12-freq-20",
    "resolution-16-freq-20",
    "polarization-ey",
]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Analyze local v0.6 candidate spectrum consistency.")
    parser.add_argument("--matrix-dir", type=Path, help="Existing runs/candidate-hardening/<matrix_run_id> directory.")
    parser.add_argument("--latest", action="store_true", help="Use latest candidate-hardening matrix directory.")
    parser.add_argument("--run-matrix", action="store_true", help="Run candidate hardening first, then analyze it.")
    parser.add_argument("--timeout", type=int, default=900, help="Per-case timeout when --run-matrix is used.")
    parser.add_argument("--baseline-case", default="repeat-1", help="Baseline case directory name.")
    parser.add_argument("--output", type=Path, help="Output summary JSON path.")
    parser.add_argument("--peak-shift-threshold-nm", type=float, default=50.0)
    parser.add_argument("--l2-threshold", type=float, default=0.5)
    parser.add_argument("--integrated-flux-threshold", type=float, default=0.5)
    args = parser.parse_args(argv)

    matrix_dir = _resolve_matrix_dir(args)
    if matrix_dir is None:
        print(
            "No candidate-hardening matrix directory found. Run "
            "`python scripts/local_meep_candidate_hardening.py --timeout 900` "
            "or pass --matrix-dir / --latest.",
            file=sys.stderr,
        )
        return 2

    output_path = args.output or (matrix_dir / "candidate_convergence_summary.json")
    summary = analyze_matrix(
        matrix_dir=matrix_dir,
        baseline_case=args.baseline_case,
        output_path=output_path,
        peak_shift_threshold_nm=args.peak_shift_threshold_nm,
        l2_threshold=args.l2_threshold,
        integrated_flux_threshold=args.integrated_flux_threshold,
    )
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if not summary.get("errors") else 1


def analyze_matrix(
    *,
    matrix_dir: Path,
    baseline_case: str,
    output_path: Path,
    peak_shift_threshold_nm: float,
    l2_threshold: float,
    integrated_flux_threshold: float,
) -> dict:
    """Analyze spectrum consistency for an existing candidate-hardening matrix."""
    matrix_dir = Path(matrix_dir)
    baseline_path = matrix_dir / baseline_case / "scattering_spectrum.csv"
    thresholds = {
        "peak_shift_threshold_nm": peak_shift_threshold_nm,
        "l2_threshold": l2_threshold,
        "integrated_flux_threshold": integrated_flux_threshold,
    }
    summary: dict = {
        "schema_version": "candidate_convergence_summary.v0.1",
        "matrix_dir": str(matrix_dir),
        "baseline_case": baseline_case,
        "baseline_path": str(baseline_path),
        "compared_cases": [],
        "missing_cases": [],
        "comparisons": [],
        "pass_fail_thresholds": thresholds,
        "cases_passing_thresholds": [],
        "cases_failing_thresholds": [],
        "errors": [],
        "recommendation": "",
    }

    try:
        baseline = load_scattering_csv(baseline_path)
    except ValueError as exc:
        summary["errors"].append(str(exc))
        summary["recommendation"] = "Baseline spectrum could not be loaded; rerun candidate hardening."
        _write_summary(output_path, summary)
        return summary

    comparisons = []
    for case_name in DEFAULT_CASES:
        candidate_path = matrix_dir / case_name / "scattering_spectrum.csv"
        if not candidate_path.exists():
            summary["missing_cases"].append(case_name)
            continue
        try:
            candidate = load_scattering_csv(candidate_path)
            comparison = compare_spectra(baseline, candidate)
        except ValueError as exc:
            summary["cases_failing_thresholds"].append(
                {"case_name": case_name, "reason": str(exc)}
            )
            continue

        comparison_dict = comparison.to_dict()
        comparison_dict["case_name"] = case_name
        passed = _passes_thresholds(
            comparison_dict,
            peak_shift_threshold_nm=peak_shift_threshold_nm,
            l2_threshold=l2_threshold,
            integrated_flux_threshold=integrated_flux_threshold,
        )
        comparison_dict["passes_thresholds"] = passed
        summary["comparisons"].append(comparison_dict)
        summary["compared_cases"].append(case_name)
        if passed:
            summary["cases_passing_thresholds"].append(case_name)
        else:
            summary["cases_failing_thresholds"].append(case_name)
        comparisons.append(comparison)

    summary["aggregate"] = summarize_comparisons(comparisons)
    if summary["cases_failing_thresholds"]:
        summary["recommendation"] = "Candidate needs more convergence/sanity work before physical interpretation."
    elif summary["missing_cases"]:
        summary["recommendation"] = "Available cases pass thresholds, but missing cases should be generated before stronger claims."
    else:
        summary["recommendation"] = "All available hardening spectra pass initial sanity thresholds; proceed to stricter convergence checks."

    _write_summary(output_path, summary)
    return summary


def _resolve_matrix_dir(args: argparse.Namespace) -> Path | None:
    if args.run_matrix:
        cmd = [
            sys.executable,
            str(ROOT / "scripts" / "local_meep_candidate_hardening.py"),
            "--timeout",
            str(args.timeout),
        ]
        subprocess.run(cmd, cwd=str(ROOT), check=False, timeout=args.timeout * 12)
        return _latest_matrix_dir()
    if args.matrix_dir:
        return args.matrix_dir
    if args.latest:
        return _latest_matrix_dir()
    return None


def _latest_matrix_dir() -> Path | None:
    root = ROOT / "runs" / "candidate-hardening"
    if not root.exists():
        return None
    candidates = [
        path for path in root.iterdir()
        if path.is_dir() and (path / "candidate_hardening_summary.json").exists()
    ]
    if not candidates:
        return None
    return max(candidates, key=lambda path: path.stat().st_mtime)


def _passes_thresholds(
    comparison: dict,
    *,
    peak_shift_threshold_nm: float,
    l2_threshold: float,
    integrated_flux_threshold: float,
) -> bool:
    peak_shift = comparison.get("peak_shift_nm")
    l2 = comparison.get("normalized_l2_difference")
    integrated = comparison.get("integrated_flux_relative_difference")
    if peak_shift is None or l2 is None or integrated is None:
        return False
    return (
        abs(peak_shift) <= peak_shift_threshold_nm
        and l2 <= l2_threshold
        and integrated <= integrated_flux_threshold
    )


def _write_summary(path: Path, summary: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
