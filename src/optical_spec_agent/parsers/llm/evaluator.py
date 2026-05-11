"""Deterministic LLM parser evaluation harness."""

from __future__ import annotations

import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from optical_spec_agent.models.base import StatusField
from optical_spec_agent.parsers.llm.config import LLMParserConfig
from optical_spec_agent.services.spec_service import SpecService


LLM_EVAL_SCHEMA_VERSION = "llm_eval_report.v0.8"


def run_llm_evaluation(
    *,
    cases_path: Path,
    parser_mode: str = "hybrid",
    llm_provider: str = "mock",
    llm_model: str = "mock-optical-parser",
    report_path: Path | None = None,
    summary_csv_path: Path | None = None,
) -> dict[str, Any]:
    """Run deterministic LLM parser evaluation cases."""

    cases = json.loads(cases_path.read_text(encoding="utf-8"))
    if not isinstance(cases, list):
        raise ValueError("LLM benchmark file must contain a list of cases")

    config = LLMParserConfig(provider=llm_provider, model=llm_model, parser_mode="hybrid" if parser_mode == "hybrid" else "llm")
    svc = SpecService(parser=parser_mode, llm_config=config)
    report_cases: list[dict[str, Any]] = []
    total_fields = 0
    passed_fields = 0

    for case in cases:
        spec = svc.process(case["text"], task_id=case.get("id", ""))
        expected = case.get("expected", {})
        checks: list[dict[str, Any]] = []
        case_ok = True
        for path, expected_value in expected.items():
            actual = _get_path_value(spec, path)
            ok = actual == expected_value
            checks.append(
                {
                    "path": path,
                    "expected": expected_value,
                    "actual": actual,
                    "passed": ok,
                }
            )
            total_fields += 1
            passed_fields += 1 if ok else 0
            case_ok = case_ok and ok

        allowed_missing = case.get("allowed_missing", [])
        missing_handled = all(path in spec.missing_fields for path in allowed_missing)
        parser_report = svc.last_parser_report.model_dump() if svc.last_parser_report else {}
        report_cases.append(
            {
                "id": case.get("id", ""),
                "text": case.get("text", ""),
                "passed": case_ok and missing_handled,
                "expected": expected,
                "actual": {check["path"]: check["actual"] for check in checks},
                "checks": checks,
                "missing_expected": [
                    path for path in expected if _get_path_value(spec, path) is None
                ],
                "unexpected_values": [
                    check for check in checks if not check["passed"]
                ],
                "allowed_missing": allowed_missing,
                "missing_field_handling": missing_handled,
                "warnings": parser_report.get("warnings", []) + spec.validation_status.warnings,
                "errors": parser_report.get("errors", []) + spec.validation_status.errors,
                "fallback_used": parser_report.get("fallback_used", False),
                "repair_used": parser_report.get("repair_used", False),
                "conflict_count": len(parser_report.get("conflicts", [])),
                "notes": case.get("notes", ""),
            }
        )

    passed_cases = sum(1 for case in report_cases if case["passed"])
    report = {
        "schema_version": LLM_EVAL_SCHEMA_VERSION,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "parser_mode": parser_mode,
        "provider": llm_provider,
        "model": llm_model,
        "total_cases": len(report_cases),
        "passed_cases": passed_cases,
        "failed_cases": len(report_cases) - passed_cases,
        "field_accuracy": (passed_fields / total_fields) if total_fields else 0.0,
        "cases": report_cases,
    }

    if report_path:
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    if summary_csv_path:
        _write_summary_csv(summary_csv_path, report_cases)
    return report


def _get_path_value(root: Any, path: str) -> Any:
    current = root
    for part in path.split("."):
        if isinstance(current, StatusField):
            current = current.value
        if isinstance(current, dict):
            current = current.get(part)
        else:
            current = getattr(current, part, None)
        if current is None:
            return None
    if isinstance(current, StatusField):
        return current.value
    return current


def _write_summary_csv(path: Path, cases: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "passed", "fallback_used", "repair_used", "conflict_count"],
        )
        writer.writeheader()
        for case in cases:
            writer.writerow(
                {
                    "id": case["id"],
                    "passed": case["passed"],
                    "fallback_used": case["fallback_used"],
                    "repair_used": case["repair_used"],
                    "conflict_count": case["conflict_count"],
                }
            )
