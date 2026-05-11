#!/usr/bin/env python3
"""Run deterministic v0.8 LLM parser benchmark cases."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from optical_spec_agent.parsers.llm.evaluator import run_llm_evaluation


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run LLM parser benchmark cases.")
    parser.add_argument(
        "--cases",
        type=Path,
        default=Path("benchmarks/llm_cases.json"),
        help="Path to LLM benchmark cases.",
    )
    parser.add_argument("--parser", default="hybrid", choices=["llm", "hybrid"])
    parser.add_argument("--llm-provider", default="mock")
    parser.add_argument("--llm-model", default="mock-optical-parser")
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--summary-csv", type=Path, default=None)
    parser.add_argument("--json", action="store_true", help="Print report JSON to stdout.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    report = run_llm_evaluation(
        cases_path=args.cases,
        parser_mode=args.parser,
        llm_provider=args.llm_provider,
        llm_model=args.llm_model,
        report_path=args.report,
        summary_csv_path=args.summary_csv,
    )
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(
            "[llm benchmark] "
            f"{report['passed_cases']}/{report['total_cases']} passed, "
            f"field_accuracy={report['field_accuracy']:.3f}"
        )
        if args.report:
            print(f"[llm benchmark] report written to {args.report}")
        if args.summary_csv:
            print(f"[llm benchmark] CSV summary written to {args.summary_csv}")
    sys.exit(0 if report["failed_cases"] == 0 else 1)


if __name__ == "__main__":
    main()
