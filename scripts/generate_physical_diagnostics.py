#!/usr/bin/env python3
"""Generate local physical diagnostics reports for one OpticalSpec/artifact set."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from optical_spec_agent.analysis import generate_physical_diagnostics, prepare_diagnostic_spec


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Read an OpticalSpec JSON and optional Meep execution artifacts, then write "
            "mesh_report.csv, flux_report.csv, execution_diagnostics.json, and "
            "diagnostic_preview.png under outputs/."
        )
    )
    parser.add_argument("--spec", type=Path, default=Path("outputs/my_spec.json"))
    parser.add_argument("--output-dir", type=Path, default=Path("outputs"))
    parser.add_argument("--artifact-dir", "--run-dir", dest="artifact_dir", type=Path, default=None)
    parser.add_argument("--execution-result", type=Path, default=None)
    parser.add_argument("--spectrum", type=Path, default=None)
    parser.add_argument("--flux-surfaces", type=Path, default=None)
    parser.add_argument("--resolution", type=float, default=12.0)
    parser.add_argument(
        "--create-demo-spec-if-missing",
        action="store_true",
        help="Create outputs/my_spec.json from the core Meep hero task if it is missing.",
    )
    parser.add_argument(
        "--no-preview",
        action="store_true",
        help="Skip diagnostic_preview.png generation.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print the final diagnostics JSON to stdout.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        spec_path, created_demo = prepare_diagnostic_spec(
            args.spec,
            create_demo_spec_if_missing=args.create_demo_spec_if_missing,
        )
    except FileNotFoundError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    if created_demo:
        print(f"Created demo spec from core hero task: {spec_path}", file=sys.stderr)

    result = generate_physical_diagnostics(
        spec_path=spec_path,
        output_dir=args.output_dir,
        artifact_dir=args.artifact_dir,
        execution_result_path=args.execution_result,
        spectrum_path=args.spectrum,
        flux_surfaces_path=args.flux_surfaces,
        resolution_px_per_um=args.resolution,
        create_preview=not args.no_preview,
    )

    if args.json:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False))
    else:
        print("Physical diagnostics written:")
        for name, path in result.generated_outputs.items():
            print(f"  - {name}: {path}")
        if result.warnings:
            print("Warnings:")
            for warning in result.warnings:
                print(f"  - {warning}")
        if result.errors:
            print("Errors:")
            for error in result.errors:
                print(f"  - {error}")

    return 1 if result.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
