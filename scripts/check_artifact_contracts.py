#!/usr/bin/env python3
"""Generate and validate minimal deterministic artifact contracts."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from optical_spec_agent.analysis.physical_diagnostics import (  # noqa: E402
    generate_physical_diagnostics,
    prepare_diagnostic_spec,
)
from optical_spec_agent.workflows.runner import WorkflowRunner, WorkflowRunnerConfig  # noqa: E402


JSON_REQUIRED_FIELDS = {
    "execution_diagnostics.json": [
        "schema_version",
        "spec_path",
        "output_dir",
        "run_dir",
        "generated_at",
        "status",
        "warnings",
        "errors",
        "missing_artifacts",
        "nan_detected",
        "inf_detected",
        "timeout_detected",
        "notes",
    ],
    "semantic_benchmark_report.json": [
        "schema_version",
        "case_count",
        "passed_count",
        "failed_count",
        "all_passed",
        "cases",
    ],
    "llm_eval_report.json": [
        "schema_version",
        "total_cases",
        "passed_cases",
        "failed_cases",
        "field_accuracy",
        "cases",
    ],
    "workflow_run.json": [
        "schema_version",
        "run_id",
        "created_at",
        "input_text",
        "steps",
        "artifacts",
        "status",
    ],
    "release_readiness_report.json": [
        "schema_version",
        "generated_at",
        "status",
        "blockers",
        "warnings",
        "recommended_actions",
    ],
}

CSV_REQUIRED_COLUMNS = {
    "mesh_report.csv": ["check_name", "value", "threshold", "unit", "status", "message"],
    "flux_report.csv": ["monitor_name", "surface", "value", "unit", "status", "message"],
}


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=120,
        check=False,
    )


def _ensure_demo_artifacts(output_root: Path) -> dict[str, Path]:
    output_root.mkdir(parents=True, exist_ok=True)
    spec_path = output_root / "diagnostic_spec.json"
    spec_path, _ = prepare_diagnostic_spec(spec_path, create_demo_spec_if_missing=True)
    diagnostics_dir = output_root / "diagnostics"
    diagnostics = generate_physical_diagnostics(
        spec_path=spec_path,
        output_dir=diagnostics_dir,
        artifact_dir=output_root / "missing_run_artifacts",
    )

    semantic_report = output_root / "semantic_benchmark_report.json"
    semantic = _run(
        [sys.executable, "benchmarks/run_semantic_benchmark.py", "--report", str(semantic_report)]
    )
    if semantic.returncode != 0:
        raise RuntimeError(f"semantic benchmark failed: {semantic.stdout}\n{semantic.stderr}")

    llm_report = output_root / "llm_eval_report.json"
    llm = _run(
        [
            sys.executable,
            "benchmarks/run_llm_benchmark.py",
            "--cases",
            "benchmarks/llm_cases.json",
            "--parser",
            "hybrid",
            "--llm-provider",
            "mock",
            "--report",
            str(llm_report),
        ]
    )
    if llm.returncode != 0:
        raise RuntimeError(f"LLM benchmark failed: {llm.stdout}\n{llm.stderr}")

    workflow_dir = output_root / "workflow_demo"
    workflow = WorkflowRunner(
        WorkflowRunnerConfig(
            parser="hybrid",
            llm_provider="mock",
            tool="mpb",
            output_dir=workflow_dir,
            allow_execute=False,
            strict=False,
            run_diagnostics=True,
        )
    ).run("用 MPB 计算二维光子晶体 band diagram，输出前 8 条能带。")

    release_report = output_root / "release_readiness_report.json"
    release = _run(
        [sys.executable, "scripts/check_release_readiness.py", "--report", str(release_report)]
    )
    if release.returncode != 0:
        raise RuntimeError(f"release readiness failed: {release.stdout}\n{release.stderr}")

    return {
        "execution_diagnostics.json": diagnostics_dir / "execution_diagnostics.json",
        "mesh_report.csv": diagnostics_dir / "mesh_report.csv",
        "flux_report.csv": diagnostics_dir / "flux_report.csv",
        "diagnostic_preview.png": diagnostics_dir / "diagnostic_preview.png",
        "semantic_benchmark_report.json": semantic_report,
        "llm_eval_report.json": llm_report,
        "workflow_run.json": workflow_dir / "workflow_run.json",
        "release_readiness_report.json": release_report,
    }


def _check_json(path: Path, required: list[str]) -> list[str]:
    errors: list[str] = []
    data = json.loads(path.read_text(encoding="utf-8"))
    for field in required:
        if field not in data:
            errors.append(f"{path.name} missing required field `{field}`")
    return errors


def _check_csv(path: Path, required: list[str]) -> list[str]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames or []
        rows = list(reader)
    errors = [f"{path.name} missing column `{column}`" for column in required if column not in columns]
    if not rows:
        errors.append(f"{path.name} must contain at least one row")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "outputs" / "release_checks" / "artifact_contracts",
    )
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    artifacts: dict[str, str] = {}
    try:
        paths = _ensure_demo_artifacts(args.output_dir)
        for name, path in paths.items():
            artifacts[name] = str(path)
            if not path.exists():
                errors.append(f"{name} was not generated at {path}")
                continue
            if name in JSON_REQUIRED_FIELDS:
                errors.extend(_check_json(path, JSON_REQUIRED_FIELDS[name]))
            if name in CSV_REQUIRED_COLUMNS:
                errors.extend(_check_csv(path, CSV_REQUIRED_COLUMNS[name]))
            if name.endswith(".png") and path.stat().st_size == 0:
                errors.append(f"{name} must be non-empty")
    except Exception as exc:  # noqa: BLE001 - report release-check failures clearly.
        errors.append(str(exc))

    report = {
        "schema_version": "artifact_contract_check.v0.1",
        "status": "blocked" if errors else ("warning" if warnings else "ready"),
        "artifacts": artifacts,
        "errors": errors,
        "warnings": warnings,
    }
    report_path = args.report or (args.output_dir / "artifact_contract_report.json")
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Artifact contract check: {report['status']}")
        print(f"Report written to {report_path}")
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARNING: {warning}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
