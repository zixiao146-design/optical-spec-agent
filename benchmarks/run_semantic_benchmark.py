#!/usr/bin/env python3
"""Semantic benchmark runner for key field extraction quality."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from optical_spec_agent.models.base import StatusField
from optical_spec_agent.services.spec_service import SpecService

SEMANTIC_CASES_PATH = Path(__file__).resolve().parent / "semantic_cases.json"


def load_cases() -> list[dict[str, Any]]:
    with open(SEMANTIC_CASES_PATH, encoding="utf-8") as f:
        return json.load(f)


def _get_path_value(root: Any, path: str) -> Any:
    current = root
    for part in path.split("."):
        if isinstance(current, StatusField):
            current = current.value

        if isinstance(current, (list, tuple)) and part.isdigit():
            index = int(part)
            if index >= len(current):
                return None
            current = current[index]
        elif isinstance(current, dict):
            current = current.get(part)
        else:
            current = getattr(current, part, None)

        if current is None:
            return None

    if isinstance(current, StatusField):
        return current.value
    return current


def _parse_numeric(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)

    import re

    m = re.search(r"([\d.]+)", str(value))
    if not m:
        return None
    return float(m.group(1))


def _check(case_id: str, spec, check: dict[str, Any]) -> tuple[bool, str]:
    path = check["path"]
    value = _get_path_value(spec, path)

    if "equals" in check:
        expected = check["equals"]
        return value == expected, f"{path}: expected {expected!r}, got {value!r}"

    if "equals_any" in check:
        expected_values = check["equals_any"]
        return value in expected_values, f"{path}: expected one of {expected_values!r}, got {value!r}"

    if "numeric_equals" in check:
        actual_num = _parse_numeric(value)
        expected_num = float(check["numeric_equals"])
        ok = actual_num is not None and abs(actual_num - expected_num) < 1e-9
        return ok, f"{path}: expected numeric {expected_num}, got {value!r}"

    if "contains" in check:
        expected = check["contains"]
        ok = isinstance(value, list) and expected in value
        return ok, f"{path}: expected list containing {expected!r}, got {value!r}"

    if "contains_target_type" in check:
        expected = check["contains_target_type"]
        target_types: list[str] = []
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "target_type" in item:
                    target_types.append(item["target_type"])
                elif isinstance(item, str):
                    target_types.append(item)
        ok = expected in target_types
        return ok, f"{path}: expected target_type {expected!r}, got {target_types!r}"

    if "is_missing_or_not_equals" in check:
        unexpected = check["is_missing_or_not_equals"]
        ok = value is None or value != unexpected
        return ok, f"{path}: expected missing or not equal to {unexpected!r}, got {value!r}"

    if "contains_name" in check:
        expected = check["contains_name"]
        names: list[str] = []
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "name" in item:
                    names.append(str(item["name"]))
                else:
                    item_name = getattr(item, "name", None)
                    if item_name is not None:
                        names.append(str(item_name))
        ok = expected in names
        return ok, f"{path}: expected name {expected!r}, got {names!r}"

    if "not_contains_name" in check:
        unexpected = check["not_contains_name"]
        names: list[str] = []
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "name" in item:
                    names.append(str(item["name"]))
                else:
                    item_name = getattr(item, "name", None)
                    if item_name is not None:
                        names.append(str(item_name))
        ok = unexpected not in names
        return ok, f"{path}: expected to exclude name {unexpected!r}, got {names!r}"

    if "contains_material" in check:
        expected = check["contains_material"]
        names: list[str] = []
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "name" in item:
                    names.append(str(item["name"]))
                else:
                    item_name = getattr(item, "name", None)
                    if item_name is not None:
                        names.append(str(item_name))
        ok = expected in names
        return ok, f"{path}: expected material {expected!r}, got {names!r}"

    if "not_contains_material" in check:
        unexpected = check["not_contains_material"]
        names: list[str] = []
        if isinstance(value, list):
            for item in value:
                if isinstance(item, dict) and "name" in item:
                    names.append(str(item["name"]))
                else:
                    item_name = getattr(item, "name", None)
                    if item_name is not None:
                        names.append(str(item_name))
        ok = unexpected not in names
        return ok, f"{path}: expected to exclude material {unexpected!r}, got {names!r}"

    return False, f"{case_id}: unsupported semantic check {check!r}"


def main() -> None:
    svc = SpecService()
    cases = load_cases()
    all_ok = True

    print(f"[semantic benchmark] {len(cases)} case(s)")
    for case in cases:
        spec = svc.process(case["input"], task_id=case["task_id"])
        case_ok = True
        for check in case.get("checks", []):
            ok, message = _check(case["task_id"], spec, check)
            if not ok:
                print(f"  FAIL {case['task_id']}: {message}")
                case_ok = False
        if case_ok:
            print(f"  PASS {case['task_id']}: {len(case.get('checks', []))} semantic checks OK")
        all_ok = all_ok and case_ok

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
