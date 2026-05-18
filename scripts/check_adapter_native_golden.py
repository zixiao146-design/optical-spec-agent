#!/usr/bin/env python3
"""Check adapter-native source/monitor golden preview cases.

This script is local-only. It calls the in-process FastAPI TestClient and
checks preview metadata; it does not run Meep, MPB, Gmsh, ElmerSolver,
Optiland, external LLMs, uploads, tags, or releases.
"""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fastapi.testclient import TestClient  # noqa: E402

from optical_spec_agent.api.app import app  # noqa: E402


CASE_ROOT = ROOT / "examples" / "adapter_native_golden"
REQUIRED_CASE_FILES = (
    "request.json",
    "source_model.json",
    "monitor_model.json",
    "observable_diagnostics.json",
    "adapter_mapping.json",
    "expected_preview_fragments.txt",
    "README.md",
)
SAFETY_FLAGS = (
    "external_solver_executed",
    "external_llm_required",
    "proprietary_solver_required",
    "production_grade_validation_claimed",
    "formal_convergence_proof_claimed",
)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _expected_fragments(path: Path) -> list[str]:
    fragments = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            fragments.append(stripped)
    return fragments


def _assert_safe(payload: dict[str, Any], *, case_id: str) -> None:
    for flag in SAFETY_FLAGS:
        if flag in payload and payload[flag] is not False:
            raise AssertionError(f"{case_id}: safety flag {flag} is not false")
    mapping = payload.get("adapter_source_monitor_mapping", {})
    if mapping.get("external_solver_executed") is not False:
        raise AssertionError(f"{case_id}: adapter mapping executed a solver")
    if mapping.get("preview_only") is not True:
        raise AssertionError(f"{case_id}: adapter mapping is not preview_only")
    if mapping.get("production_grade_validation_claimed") is not False:
        raise AssertionError(f"{case_id}: adapter mapping overclaimed validation")
    if mapping.get("formal_convergence_proof_claimed") is not False:
        raise AssertionError(f"{case_id}: adapter mapping overclaimed convergence")


def _check_case(client: TestClient, case_dir: Path) -> dict[str, Any]:
    case_id = case_dir.name
    for filename in REQUIRED_CASE_FILES:
        path = case_dir / filename
        if not path.exists():
            raise AssertionError(f"{case_id}: missing {filename}")

    request = _load_json(case_dir / "request.json")
    response = client.post("/api/optical-language/adapter-mapping", json=request)
    if response.status_code != 200:
        raise AssertionError(f"{case_id}: adapter mapping returned {response.status_code}")
    payload = response.json()
    _assert_safe(payload, case_id=case_id)

    expected_source = _load_json(case_dir / "source_model.json")
    expected_monitor = _load_json(case_dir / "monitor_model.json")
    expected_observables = _load_json(case_dir / "observable_diagnostics.json")
    expected_mapping = _load_json(case_dir / "adapter_mapping.json")

    if payload["source_model"] != expected_source:
        raise AssertionError(f"{case_id}: source_model drifted")
    if payload["monitor_model"] != expected_monitor:
        raise AssertionError(f"{case_id}: monitor_model drifted")
    if payload["observable_diagnostics"] != expected_observables:
        raise AssertionError(f"{case_id}: observable_diagnostics drifted")
    if payload["adapter_source_monitor_mapping"] != expected_mapping:
        raise AssertionError(f"{case_id}: adapter_mapping drifted")

    serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False).lower()
    missing_fragments = [
        fragment
        for fragment in _expected_fragments(case_dir / "expected_preview_fragments.txt")
        if fragment.lower() not in serialized
    ]
    if missing_fragments:
        raise AssertionError(f"{case_id}: missing expected fragments {missing_fragments}")

    return {
        "case_id": case_id,
        "adapter_name": payload["adapter_source_monitor_mapping"]["adapter_name"],
        "supported_observables": payload["adapter_source_monitor_mapping"][
            "supported_observables"
        ],
        "requires_solver_for_real_result": payload["adapter_source_monitor_mapping"][
            "requires_solver_for_real_result"
        ],
        "external_solver_executed": False,
        "preview_only": True,
    }


def main() -> int:
    client = TestClient(app)
    case_dirs = sorted(path for path in CASE_ROOT.iterdir() if path.is_dir())
    if not case_dirs:
        raise AssertionError("No adapter-native golden case directories found.")

    report = {
        "schema_version": "adapter_native_golden.v0.1",
        "case_count": len(case_dirs),
        "cases": [_check_case(client, case_dir) for case_dir in case_dirs],
        "external_solver_executed": False,
        "external_llm_required": False,
        "proprietary_solver_required": False,
        "production_grade_validation_claimed": False,
        "formal_convergence_proof_claimed": False,
    }

    report_path = os.environ.get("OSA_ADAPTER_NATIVE_GOLDEN_REPORT")
    if report_path:
        Path(report_path).write_text(
            json.dumps(report, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    print(json.dumps(report, indent=2, ensure_ascii=False))
    print("ADAPTER NATIVE GOLDEN CHECKS PASSED")
    print("NO SOLVER EXECUTION PERFORMED")
    print("NO EXTERNAL LLM CALLED")
    print("NO UPLOAD PERFORMED")
    print("NO TAG CREATED")
    print("NO RELEASE CREATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
