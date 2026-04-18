#!/usr/bin/env python3
"""Golden-case benchmark runner.

Usage:
    python benchmarks/run_benchmark.py [--mode MODE] [--update]

Options:
    --mode MODE   Comparison mode: 'exact' (default), 'key_fields', or 'all'.
    --update      Overwrite golden_cases.json with current parser output.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

# Ensure src is importable
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from optical_spec_agent.services.spec_service import SpecService

GOLDEN_PATH = Path(__file__).resolve().parent / "golden_cases.json"

# Fields considered critical for key-field matching.
# For each case, only these fields are checked in key_fields mode.
# A field passes if it exists in the output with status 'confirmed' or 'inferred'
# and has a non-null value.
CORE_KEY_FIELDS = [
    "task.task_type",
    "physics.physical_system",
    "simulation.solver_method",
    "output.output_observables",
]


def _get_nested(d: dict, path: str):
    """Get a nested dict value by dot-separated path like 'task.task_type'."""
    keys = path.split(".")
    v = d
    for k in keys:
        if isinstance(v, dict):
            v = v.get(k)
        else:
            return None
    return v


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


def compare_exact(golden: list[dict], current: list[dict]) -> bool:
    """Return True if all outputs match exactly."""
    ok = True
    for g, c in zip(golden, current):
        if g["task_id"] != c["task_id"]:
            print(f"  MISMATCH task_id: {g['task_id']} vs {c['task_id']}")
            ok = False
            continue

        g_out = json.dumps(g["output"], sort_keys=True, ensure_ascii=False)
        c_out = json.dumps(c["output"], sort_keys=True, ensure_ascii=False)

        if g_out != c_out:
            print(f"  FAIL  {g['task_id']}: output differs")
            g_lines = g_out.splitlines()
            c_lines = c_out.splitlines()
            for i, (gl, cl) in enumerate(zip(g_lines, c_lines)):
                if gl != cl:
                    print(f"    line {i}:")
                    print(f"      golden : {gl[:120]}")
                    print(f"      current: {cl[:120]}")
                    if i > 5:
                        print("    ... (truncated)")
                        break
            ok = False
        else:
            print(f"  PASS  {g['task_id']}")
    return ok


def compare_key_fields(golden: list[dict], current: list[dict]) -> bool:
    """Check that core key fields are present with confirmed/inferred status."""
    ok = True
    for g, c in zip(golden, current):
        tid = g["task_id"]
        # Use case-specific fields if defined, otherwise CORE_KEY_FIELDS
        expected_fields = g.get("expected_key_fields", CORE_KEY_FIELDS)
        case_ok = True

        for field_path in expected_fields:
            field_data = _get_nested(c["output"], field_path)
            if field_data is None:
                print(f"  MISS  {tid}: {field_path} not found in output")
                case_ok = False
                continue

            status = field_data.get("status", "") if isinstance(field_data, dict) else ""
            value = field_data.get("value") if isinstance(field_data, dict) else field_data

            if status not in ("confirmed", "inferred"):
                print(f"  FAIL  {tid}: {field_path} status={status} (expected confirmed/inferred)")
                case_ok = False
            elif value is None:
                print(f"  FAIL  {tid}: {field_path} value is None")
                case_ok = False

        if case_ok:
            print(f"  PASS  {tid}: {len(expected_fields)} key fields OK")
        else:
            ok = False
    return ok


def main() -> None:
    args = set(sys.argv[1:])

    mode = "exact"
    if "--mode" in args:
        idx = sys.argv.index("--mode")
        if idx + 1 < len(sys.argv):
            mode = sys.argv[idx + 1]

    golden = load_golden()

    if "--update" in args:
        current = run_current(golden)
        with open(GOLDEN_PATH, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2, ensure_ascii=False)
        print(f"Updated {GOLDEN_PATH} with {len(current)} cases.")
        return

    current = run_current(golden)
    n = len(golden)

    if mode in ("exact", "all"):
        print(f"\n[exact mode] Full output regression ({n} cases):")
        exact_ok = compare_exact(golden, current)
        print(f"  {n} cases: {'ALL PASSED' if exact_ok else 'SOME FAILED'}")

    if mode in ("key_fields", "all"):
        print(f"\n[key_fields mode] Core field extraction ({n} cases):")
        kf_ok = compare_key_fields(golden, current)
        print(f"  {n} cases: {'ALL PASSED' if kf_ok else 'SOME FAILED'}")

    if mode == "all":
        sys.exit(0 if (exact_ok and kf_ok) else 1)
    elif mode == "exact":
        sys.exit(0 if exact_ok else 1)
    elif mode == "key_fields":
        sys.exit(0 if kf_ok else 1)
    else:
        print(f"Unknown mode: {mode}. Use 'exact', 'key_fields', or 'all'.")
        sys.exit(1)


if __name__ == "__main__":
    main()
