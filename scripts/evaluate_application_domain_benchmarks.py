#!/usr/bin/env python3
"""Evaluate local application-domain benchmark scenarios.

This script is local-only. It does not execute external solvers, call external
LLMs, upload packages, create tags, or create releases.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from optical_spec_agent.examples.domain_benchmarks import (  # noqa: E402
    evaluate_all_domain_scenarios,
)


def main() -> int:
    response = evaluate_all_domain_scenarios()
    payload = response.model_dump(mode="json")
    report_path = os.environ.get("OSA_APPLICATION_DOMAIN_BENCHMARK_REPORT")
    if report_path:
        Path(report_path).write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    summary = payload["summary"]
    print("APPLICATION DOMAIN BENCHMARKS")
    print(f"scenario_count={summary['total']}")
    print(f"pass={summary['pass']}")
    print(f"warn={summary['warn']}")
    print(f"fail={summary['fail']}")
    print(f"positive={summary['positive']}")
    print(f"ambiguous={summary['ambiguous']}")
    print(f"underconstrained={summary['underconstrained']}")
    print(f"unsupported={summary['unsupported']}")
    print("APPLICATION DOMAIN BENCHMARKS PASSED" if summary["fail"] == 0 else "APPLICATION DOMAIN BENCHMARKS FAILED")
    print("NO SOLVER EXECUTION PERFORMED")
    print("NO EXTERNAL LLM CALLED")
    print("NO UPLOAD PERFORMED")
    print("NO TAG CREATED")
    print("NO RELEASE CREATED")
    return 0 if summary["fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
