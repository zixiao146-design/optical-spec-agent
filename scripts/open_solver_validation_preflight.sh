#!/usr/bin/env bash
set -euo pipefail

PROJECT_VERSION="$(python - <<'PY'
import tomllib
from pathlib import Path

with Path("pyproject.toml").open("rb") as handle:
    data = tomllib.load(handle)
print(data["project"]["version"])
PY
)"

echo "Open-source solver validation preflight"
echo "Project version: ${PROJECT_VERSION}"
echo "Default behavior: detect availability only; do not run solvers."

if [[ ! -f "docs/adapter_support_matrix.md" ]]; then
  echo "STOP: docs/adapter_support_matrix.md is missing."
  exit 1
fi

if [[ ! -f "docs/open_source_solver_validation_plan.md" ]]; then
  echo "STOP: docs/open_source_solver_validation_plan.md is missing."
  exit 1
fi

CHECKED_COMMANDS=(meep mpb gmsh ElmerSolver optiland)
AVAILABLE=()
UNAVAILABLE=()

echo
echo "Candidate open-source solver command availability:"
for candidate in "${CHECKED_COMMANDS[@]}"; do
  if command -v "${candidate}" >/dev/null 2>&1; then
    path="$(command -v "${candidate}")"
    AVAILABLE+=("${candidate}=${path}")
    echo "- ${candidate}: available at ${path} (not executed)"
  else
    UNAVAILABLE+=("${candidate}")
    echo "- ${candidate}: unavailable"
  fi
done

if [[ -n "${OSA_SOLVER_PREFLIGHT_JSON:-}" ]]; then
  AVAILABLE_JOIN=""
  UNAVAILABLE_JOIN=""
  if ((${#AVAILABLE[@]})); then
    AVAILABLE_JOIN="$(printf '%s\n' "${AVAILABLE[@]}")"
  fi
  if ((${#UNAVAILABLE[@]})); then
    UNAVAILABLE_JOIN="$(printf '%s\n' "${UNAVAILABLE[@]}")"
  fi
  CHECKED_JOIN="$(printf '%s\n' "${CHECKED_COMMANDS[@]}")"
  export PROJECT_VERSION AVAILABLE_JOIN UNAVAILABLE_JOIN CHECKED_JOIN OSA_SOLVER_PREFLIGHT_JSON
  python - <<'PY'
import json
import os
from pathlib import Path

checked = [item for item in os.environ["CHECKED_JOIN"].splitlines() if item]
available = []
for item in os.environ["AVAILABLE_JOIN"].splitlines():
    if not item:
        continue
    name, _, path = item.partition("=")
    available.append({"name": name, "path": path})
unavailable = [item for item in os.environ["UNAVAILABLE_JOIN"].splitlines() if item]

report = {
    "package_version": os.environ["PROJECT_VERSION"],
    "checked_commands": checked,
    "available": available,
    "unavailable": unavailable,
    "executed_solvers": False,
    "proprietary_required": False,
}

target = Path(os.environ["OSA_SOLVER_PREFLIGHT_JSON"])
target.parent.mkdir(parents=True, exist_ok=True)
target.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"JSON report written: {target}")
PY
fi

echo
echo "Next manual validation steps:"
echo "- Review docs/open_solver_validation_harness.md."
echo "- Install any desired open-source solver manually."
echo "- Run solver-specific checks only after explicit opt-in."
echo "- Record results in docs/manual_solver_validation_report_template.md."
echo
echo "Open solver preflight summary:"
echo "- availability checked"
echo "- no solver process started"
echo "- unavailable solvers do not fail this preflight"
echo "- NO SOLVER EXECUTION PERFORMED"
echo "- NO PROPRIETARY SOLVER REQUIRED"
echo "- NO TAG CREATED"
echo "- NO RELEASE CREATED"
echo "- NO UPLOAD PERFORMED"
echo "NO SOLVER EXECUTION PERFORMED"
echo "NO PROPRIETARY SOLVER REQUIRED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
echo "NO UPLOAD PERFORMED"
