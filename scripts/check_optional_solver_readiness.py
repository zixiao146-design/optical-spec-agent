#!/usr/bin/env python3
"""Check optional solver micro-benchmark readiness without executing solvers.

This script performs availability detection only. It checks whether known CLI
commands are on PATH and whether known Python modules can be imported by the
selected Python interpreter. It does not run solver binaries, execute solver
examples, call external LLMs, upload packages, create tags, or create releases.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "validation" / "solver_validation_micro_benchmarks.json"


def _selected_python() -> str:
    return os.environ.get("OSA_SOLVER_PYTHON") or sys.executable


def _profile_name() -> str:
    return os.environ.get("OSA_SOLVER_READINESS_PROFILE") or (
        "solver-python" if os.environ.get("OSA_SOLVER_PYTHON") else "current"
    )


def _python_probe_available(python_executable: str) -> tuple[bool, str]:
    resolved = shutil.which(python_executable) or (
        python_executable if Path(python_executable).exists() else None
    )
    if not resolved:
        return False, "python executable not found"
    try:
        result = subprocess.run(
            [python_executable, "-c", "import sys; raise SystemExit(0)"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False, "python executable probe failed"
    if result.returncode != 0:
        return False, "python executable probe failed"
    return True, ""


def _probe_module(python_executable: str, module_name: str) -> dict[str, Any]:
    """Probe module importability without importing it in this process."""

    try:
        result = subprocess.run(
            [python_executable, "-c", f"import {module_name}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=20,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        result = None
    return {
        "module_name": module_name,
        "available": bool(result and result.returncode == 0),
        "detected_module": module_name if result and result.returncode == 0 else None,
        "probe": "python_import_only",
        "external_solver_executed": False,
    }


def _command_probe(command_name: str) -> dict[str, Any]:
    path = shutil.which(command_name)
    return {
        "command_name": command_name,
        "available": bool(path),
        "path": path,
        "probe": "command_path_only",
        "external_solver_executed": False,
    }


def _detect_solver(
    item: dict[str, Any],
    *,
    python_executable: str,
    python_probe_available: bool,
    detection_profile: str,
) -> dict[str, Any]:
    solver_name = item["solver_name"]
    command_names = list(item.get("command_names") or [])
    module_names = list(item.get("module_names") or [])

    command_results = [_command_probe(name) for name in command_names]
    module_results = (
        [_probe_module(python_executable, name) for name in module_names]
        if python_probe_available
        else [
            {
                "module_name": name,
                "available": False,
                "detected_module": None,
                "probe": "python_import_only",
                "external_solver_executed": False,
                "missing_reason": "python probe unavailable",
            }
            for name in module_names
        ]
    )

    cli_available = any(item["available"] for item in command_results)
    python_available = any(item["available"] for item in module_results)
    detected_cli = next((item["path"] for item in command_results if item["path"]), None)
    detected_module = next(
        (item["detected_module"] for item in module_results if item["detected_module"]),
        None,
    )
    install_deferred = solver_name == "elmer" or item.get("status") == "deferred"
    detected_in_profile = cli_available or python_available
    ready_for_opt_in = (
        not install_deferred
        and (
            detected_in_profile
            or item.get("status") == "manual_report_recorded"
        )
    )
    detected = detected_cli or detected_module
    if install_deferred:
        missing_reason = "install route deferred; maintainer approval and local solver install required"
    elif detected:
        missing_reason = ""
    elif item.get("status") == "manual_report_recorded":
        missing_reason = "not detected in this readiness profile; previous manual evidence exists"
    else:
        missing_reason = "solver command/module not detected"

    return {
        "solver_name": solver_name,
        "detection_profile": detection_profile,
        "python_executable_used": python_executable,
        "python_probe_available": python_probe_available,
        "availability_checked": True,
        "cli_available": cli_available,
        "python_available": python_available,
        "detected_in_profile": detected_in_profile,
        "detected_path_or_module": detected,
        "cli_probe_path": {
            item["command_name"]: item["path"] for item in command_results
        },
        "module_probe_results": module_results,
        "command_probe_results": command_results,
        "ready_for_opt_in": ready_for_opt_in,
        "missing_reason": missing_reason,
        "install_deferred": install_deferred,
        "default_executes_solver": False,
        "production_grade_validation_claimed": False,
        "formal_convergence_proof_claimed": False,
    }


def build_readiness_report() -> dict[str, Any]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    python_executable = _selected_python()
    detection_profile = _profile_name()
    python_available, python_missing_reason = _python_probe_available(python_executable)
    solvers = [
        _detect_solver(
            item,
            python_executable=python_executable,
            python_probe_available=python_available,
            detection_profile=detection_profile,
        )
        for item in manifest["solvers"]
    ]
    return {
        "schema_version": "optional_solver_readiness.v0.2",
        "manifest": str(MANIFEST.relative_to(ROOT)),
        "detection_profile": detection_profile,
        "python_executable_used": python_executable,
        "python_probe_available": python_available,
        "python_probe_missing_reason": python_missing_reason,
        "cli_probe_path": {
            command: shutil.which(command)
            for item in manifest["solvers"]
            for command in item.get("command_names", [])
        },
        "module_probe_results": {
            solver["solver_name"]: solver["module_probe_results"]
            for solver in solvers
        },
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
            "{solver_name}: profile={detection_profile}; "
            "cli_available={cli_available}; python_available={python_available}; "
            "detected_in_profile={detected_in_profile}; ready_for_opt_in={ready_for_opt_in}; "
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
