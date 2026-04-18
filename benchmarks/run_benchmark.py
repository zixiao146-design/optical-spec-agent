#!/usr/bin/env python3
"""Golden-case benchmark runner.

Usage:
    python benchmarks/run_benchmark.py [--update]

Options:
    --update   Overwrite golden_cases.json with current parser output.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from optical_spec_agent.services.spec_service import SpecService

GOLDEN_PATH = Path(__file__).resolve().parent / "golden_cases.json"


def load_golden() -> list[dict]:
    with open(GOLDEN_PATH, encoding="utf-8") as f:
        return json.load(f)


def run_current(cases: list[dict]) -> list[dict]:
    svc = SpecService()
    results: list[dict] = []
    for case in cases:
        spec = svc.process(case["input"], task_id=case["task_id"])
        results.append(
            {
                "task_id": case["task_id"],
                "input": case["input"],
                "output": json.loads(json.dumps(spec.to_flat_dict(), default=str)),
            }
        )
    return results


def compare(golden: list[dict], current: list[dict]) -> bool:
    """Return True if all outputs match exactly."""
    ok = True
    for g, c in zip(golden, current):
        if g["task_id"] != c["task_id"]:
            print(f"MISMATCH task_id: {g['task_id']} vs {c['task_id']}")
            ok = False
            continue

        g_out = json.dumps(g["output"], sort_keys=True, ensure_ascii=False)
        c_out = json.dumps(c["output"], sort_keys=True, ensure_ascii=False)

        if g_out != c_out:
            print(f"FAIL  {g['task_id']}: output differs")
            # Show a brief diff
            g_lines = g_out.splitlines()
            c_lines = c_out.splitlines()
            for i, (gl, cl) in enumerate(zip(g_lines, c_lines)):
                if gl != cl:
                    print(f"  line {i}:")
                    print(f"    golden : {gl[:120]}")
                    print(f"    current: {cl[:120]}")
                    if i > 5:
                        print("  ... (truncated)")
                        break
            ok = False
        else:
            print(f"PASS  {g['task_id']}")

    return ok


def main() -> None:
    args = set(sys.argv[1:])
    golden = load_golden()
    current = run_current(golden)

    if "--update" in args:
        with open(GOLDEN_PATH, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2, ensure_ascii=False)
        print(f"Updated {GOLDEN_PATH} with {len(current)} cases.")
        return

    n = len(golden)
    ok = compare(golden, current)
    print(f"\n{n} cases: {'ALL PASSED' if ok else 'SOME FAILED'}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
