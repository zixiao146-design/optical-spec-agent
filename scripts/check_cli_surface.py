#!/usr/bin/env python3
"""Check that the documented CLI surface is importable and has help output.

This script is intentionally local-only: it never runs solvers, never calls an
external LLM provider, and only asks Typer for command help text.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"

CORE_COMMANDS = [
    (),
    ("parse",),
    ("validate",),
    ("schema",),
    ("example",),
    ("meep-generate",),
    ("meep-check",),
    ("meep-run",),
    ("diagnose",),
    ("adapter-list",),
    ("adapter-generate",),
    ("llm-eval",),
    ("workflow-plan",),
    ("workflow-run",),
    ("workflow-replay",),
    ("workflow-report",),
]


def _base_command() -> list[str]:
    executable = shutil.which("optical-spec")
    if executable:
        return [executable]
    return [sys.executable, "-m", "optical_spec_agent"]


def _command_label(parts: tuple[str, ...]) -> str:
    return "optical-spec" if not parts else "optical-spec " + " ".join(parts)


def _run_help(parts: tuple[str, ...]) -> dict[str, Any]:
    command = [*_base_command(), *parts, "--help"]
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=30,
        check=False,
    )
    output = f"{completed.stdout}\n{completed.stderr}"
    return {
        "command": _command_label(parts),
        "returncode": completed.returncode,
        "help_detected": "Usage" in output or "Options" in output,
        "stdout_excerpt": completed.stdout[:300],
        "stderr_excerpt": completed.stderr[:300],
    }


def _readme_mentions(command: str) -> bool:
    if not README.exists():
        return False
    return command in README.read_text(encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print the full report as JSON.")
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat README/CLI mention mismatches as errors instead of warnings.",
    )
    args = parser.parse_args()

    errors: list[str] = []
    warnings: list[str] = []
    results = [_run_help(parts) for parts in CORE_COMMANDS]

    for item in results:
        if item["returncode"] != 0 or not item["help_detected"]:
            errors.append(f"{item['command']} --help failed or did not print help text.")

    for parts in CORE_COMMANDS:
        if not parts:
            continue
        command_name = parts[0]
        mentioned = _readme_mentions(command_name)
        command_ok = next(
            result for result in results if result["command"] == _command_label(parts)
        )["returncode"] == 0
        if mentioned and not command_ok:
            errors.append(f"README mentions `{command_name}`, but the command is unavailable.")
        if command_ok and not mentioned:
            warnings.append(f"`{command_name}` exists but is not mentioned in README.md.")

    if args.strict and warnings:
        errors.extend(warnings)

    report = {
        "schema_version": "cli_surface_check.v0.1",
        "status": "blocked" if errors else ("warning" if warnings else "ready"),
        "checked_commands": results,
        "errors": errors,
        "warnings": warnings,
    }

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"CLI surface check: {report['status']}")
        for error in errors:
            print(f"ERROR: {error}")
        for warning in warnings:
            print(f"WARNING: {warning}")

    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
