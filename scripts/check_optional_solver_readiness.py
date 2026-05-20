#!/usr/bin/env python3
"""Check optional solver micro-benchmark readiness without executing solvers.

This script performs availability detection only. It checks whether known CLI
commands are on PATH and whether known Python modules can be resolved through
the import system. It does not run solver binaries, execute solver examples,
call external LLMs, upload packages, create tags, or create releases.
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "validation" / "solver_validation_micro_benchmarks.json"


def _module_available(module_name: str) -> tuple[bool, str | None]:
    try:
        spec = importlib.util.find_spec(module_name)
    except (ImportError, ModuleNotFoundError, AttributeError, ValueError):
        return False, None
    if spec is None:
        return False, None
    return True, module_name


def _mpb_module_available() -> tuple[bool, str | None]:
    meep_available, _ = _module_available("meep")
    if not meep_available:
        return False, None
    return _module_available("meep.mpb")


def _detect_solver(item: dict[str, Any]) -> dict[str, Any]:
    solver_name = item["solver_name"]
    cli_name = {
        "gmsh": "gmsh",
        "elmer": "ElmerSolver",
        "optiland": "optiland",
    }.get(solver_name)
    module_name = {
        "meep": "meep",
        "optiland": "optiland",
    }.get(solver_name)

    cli_path = shutil.which(cli_name) if cli_name else None
    if solver_name == "mpb":
        python_available, detected_module = _mpb_module_available()
    elif module_name:
        python_available, detected_module = _module_available(module_name)
    else:
        python_available, detected_module = False, None

    cli_available = bool(cli_path)
    install_deferred = solver_name == "elmer" or item.get("status") == "deferred"
    ready_for_opt_in = (
        not install_deferred
        and (
            cli_available
            or python_available
            or item.get("status") == "manual_report_recorded"
        )
    )
    detected = cli_path or detected_module
    if install_deferred:
        missing_reason = "install route deferred; maintainer approval and local solver install required"
    elif detected:
        missing_reason = ""
    elif item.get("status") == "manual_report_recorded":
        missing_reason = "not detected in this environment; previous manual evidence exists"
    else:
        missing_reason = "solver command/module not detected"

    return {
        "solver_name": solver_name,
        "availability_checked": True,
        "cli_available": cli_available,
        "python_available": python_available,
        "detected_path_or_module": detected,
        "ready_for_opt_in": ready_for_opt_in,
        "missing_reason": missing_reason,
        "install_deferred": install_deferred,
        "default_executes_solver": False,
        "production_grade_validation_claimed": False,
        "formal_convergence_proof_claimed": False,
    }


def build_readiness_report() -> dict[str, Any]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    solvers = [_detect_solver(item) for item in manifest["solvers"]]
    return {
        "schema_version": "optional_solver_readiness.v0.1",
        "manifest": str(MANIFEST.relative_to(ROOT)),
        "availability_detection_only": True,
        "default_executes_solver": False,
        "external_solver_executed": False,
        "external_llm_called": False,
        "upload_performed": False,
        "tag_created": False,
        "release_created": False,
        "production_grade_validation_claimed": False,
        "formal_convergence_proof_claimed": False,
        "solvers": solvers,
    }


def main() -> int:
    report = build_readiness_report()
    report_path = os.environ.get("OSA_SOLVER_READINESS_REPORT")
    if report_path:
        path = Path(report_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
        print(f"Wrote optional solver readiness report: {path}")

    for item in report["solvers"]:
        detected = item["detected_path_or_module"] or "not detected"
        print(
            "{solver_name}: cli_available={cli_available}; "
            "python_available={python_available}; ready_for_opt_in={ready_for_opt_in}; "
            "detected={detected}".format(detected=detected, **item)
        )

    print("SOLVER READINESS CHECK PASSED")
    print("NO SOLVER EXECUTION PERFORMED")
    print("NO EXTERNAL LLM CALLED")
    print("NO UPLOAD PERFORMED")
    print("NO TAG CREATED")
    print("NO RELEASE CREATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
