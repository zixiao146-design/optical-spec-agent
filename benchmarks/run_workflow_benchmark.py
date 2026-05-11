#!/usr/bin/env python
"""Run deterministic v0.9 workflow benchmark cases."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from optical_spec_agent.workflows import WorkflowRunner, WorkflowRunnerConfig  # noqa: E402


SCHEMA_VERSION = "workflow_benchmark.v0.9"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cases", type=Path, default=ROOT / "benchmarks" / "workflow_cases.json")
    parser.add_argument("--output-dir", type=Path, default=ROOT / "outputs" / "workflow_benchmark")
    parser.add_argument("--report", type=Path, default=ROOT / "outputs" / "workflow_benchmark_report.json")
    args = parser.parse_args()

    cases = json.loads(args.cases.read_text(encoding="utf-8"))
    case_reports = []
    passed = 0
    for case in cases:
        case_dir = args.output_dir / case["id"]
        config = WorkflowRunnerConfig(
            parser=case.get("parser", "hybrid"),
            llm_provider=case.get("llm_provider", "mock"),
            tool=case.get("tool", "auto"),
            output_dir=case_dir,
            allow_execute=False,
            strict=False,
            run_diagnostics=True,
        )
        workflow = WorkflowRunner(config).run(case["text"])
        report = _evaluate_case(case, workflow, case_dir)
        if report["passed"]:
            passed += 1
        case_reports.append(report)

    result = {
        "schema_version": SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "total_cases": len(cases),
        "passed_cases": passed,
        "failed_cases": len(cases) - passed,
        "cases": case_reports,
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Workflow benchmark: {passed}/{len(cases)} passed")
    print(f"Report written to {args.report}")
    return 0 if passed == len(cases) else 1


def _evaluate_case(case: dict[str, Any], workflow, case_dir: Path) -> dict[str, Any]:
    step_names = {step.agent_name for step in workflow.steps}
    artifact_paths = {
        artifact.path for artifact in workflow.artifacts.values()
    }
    expected_steps = case.get("expected_steps", [])
    expected_artifacts = case.get("expected_artifacts", [])
    missing_steps = [name for name in expected_steps if name not in step_names]
    missing_artifacts = [
        path for path in expected_artifacts if path not in artifact_paths and not (case_dir / path).exists()
    ]
    serialized = json.dumps(workflow.model_dump(mode="json"), ensure_ascii=False).lower()
    false_claims = []
    for claim in case.get("not_expected_claims", []):
        if claim == "solver_executed" and "solver execution succeeded" in serialized:
            false_claims.append(claim)
        if claim == "production_validation" and "production-grade physical validation achieved" in serialized:
            false_claims.append(claim)
    passed = not missing_steps and not missing_artifacts and not false_claims and workflow.status != "error"
    return {
        "id": case["id"],
        "status": workflow.status,
        "passed": passed,
        "expected_steps_passed": not missing_steps,
        "expected_artifacts_passed": not missing_artifacts,
        "missing_steps": missing_steps,
        "missing_artifacts": missing_artifacts,
        "warnings": workflow.warnings,
        "errors": workflow.errors,
        "output_dir": str(case_dir),
        "no_false_claims_passed": not false_claims,
        "false_claims": false_claims,
    }


if __name__ == "__main__":
    raise SystemExit(main())
