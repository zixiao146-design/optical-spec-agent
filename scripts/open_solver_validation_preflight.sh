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

SOLVER_NAMES=(gmsh meep mpb optiland elmer)
CHECKED_COMMANDS=(gmsh meep mpb optiland ElmerSolver)
AVAILABLE=()
UNAVAILABLE=()

gmsh_cli_available=false
gmsh_cli_path=""
gmsh_python_available=false
gmsh_python_detail=""

meep_cli_available=false
meep_cli_path=""
meep_python_available=false
meep_python_detail=""

mpb_cli_available=false
mpb_cli_path=""
mpb_python_available=false
mpb_python_detail=""

optiland_cli_available=false
optiland_cli_path=""
optiland_python_available=false
optiland_python_detail=""

elmer_cli_available=false
elmer_cli_path=""
elmer_python_available=false
elmer_python_detail=""

detect_cli() {
  local command_name="$1"
  if command -v "${command_name}" >/dev/null 2>&1; then
    command -v "${command_name}"
  fi
}

detect_python() {
  local snippet="$1"
  python -c "${snippet}" 2>/dev/null \
    | sed '/^[[:space:]]*$/d;/^Elapsed run time/d' \
    | head -n 1 || true
}

if gmsh_cli_path="$(detect_cli gmsh)" && [[ -n "${gmsh_cli_path}" ]]; then
  gmsh_cli_available=true
fi

if meep_cli_path="$(detect_cli meep)" && [[ -n "${meep_cli_path}" ]]; then
  meep_cli_available=true
fi
meep_python_detail="$(detect_python "import meep as mp; print(getattr(mp, '__version__', 'unknown'))")"
if [[ -n "${meep_python_detail}" ]]; then
  meep_python_available=true
fi

if mpb_cli_path="$(detect_cli mpb)" && [[ -n "${mpb_cli_path}" ]]; then
  mpb_cli_available=true
fi
mpb_python_detail="$(detect_python "from meep import mpb; print('meep.mpb available')")"
if [[ -n "${mpb_python_detail}" ]]; then
  mpb_python_available=true
fi

if optiland_cli_path="$(detect_cli optiland)" && [[ -n "${optiland_cli_path}" ]]; then
  optiland_cli_available=true
fi
optiland_python_detail="$(detect_python "import optiland; print(getattr(optiland, '__version__', 'unknown'))")"
if [[ -n "${optiland_python_detail}" ]]; then
  optiland_python_available=true
fi

if elmer_cli_path="$(detect_cli ElmerSolver)" && [[ -n "${elmer_cli_path}" ]]; then
  elmer_cli_available=true
fi

echo
echo "Candidate open-source solver availability:"
for solver in "${SOLVER_NAMES[@]}"; do
  cli_var="${solver}_cli_available"
  cli_path_var="${solver}_cli_path"
  python_var="${solver}_python_available"
  python_detail_var="${solver}_python_detail"
  cli_value="${!cli_var}"
  cli_path="${!cli_path_var}"
  python_value="${!python_var}"
  python_detail="${!python_detail_var}"

  if [[ "${cli_value}" == "true" || "${python_value}" == "true" ]]; then
    detail=""
    if [[ "${cli_value}" == "true" ]]; then
      detail+="cli=${cli_path}"
    fi
    if [[ "${python_value}" == "true" ]]; then
      if [[ -n "${detail}" ]]; then
        detail+=", "
      fi
      detail+="python=${python_detail}"
    fi
    AVAILABLE+=("${solver}=${detail}")
    echo "- ${solver}: available (${detail}) (not executed)"
  else
    UNAVAILABLE+=("${solver}")
    echo "- ${solver}: unavailable"
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
  SOLVER_JOIN="$(printf '%s\n' "${SOLVER_NAMES[@]}")"
  export PROJECT_VERSION AVAILABLE_JOIN UNAVAILABLE_JOIN CHECKED_JOIN SOLVER_JOIN OSA_SOLVER_PREFLIGHT_JSON
  export gmsh_cli_available gmsh_cli_path gmsh_python_available gmsh_python_detail
  export meep_cli_available meep_cli_path meep_python_available meep_python_detail
  export mpb_cli_available mpb_cli_path mpb_python_available mpb_python_detail
  export optiland_cli_available optiland_cli_path optiland_python_available optiland_python_detail
  export elmer_cli_available elmer_cli_path elmer_python_available elmer_python_detail
  python - <<'PY'
import json
import os
from pathlib import Path

checked = [item for item in os.environ["CHECKED_JOIN"].splitlines() if item]
solver_names = [item for item in os.environ["SOLVER_JOIN"].splitlines() if item]
available = []
for item in os.environ["AVAILABLE_JOIN"].splitlines():
    if not item:
        continue
    name, _, detail = item.partition("=")
    available.append({"name": name, "detail": detail})
unavailable = [item for item in os.environ["UNAVAILABLE_JOIN"].splitlines() if item]

solvers = {}
for name in solver_names:
    cli_available = os.environ.get(f"{name}_cli_available") == "true"
    python_available = os.environ.get(f"{name}_python_available") == "true"
    solvers[name] = {
        "cli_available": cli_available,
        "cli_path": os.environ.get(f"{name}_cli_path") or None,
        "python_available": python_available,
        "python_detail": os.environ.get(f"{name}_python_detail") or None,
        "available": cli_available or python_available,
        "execution_performed": False,
    }

report = {
    "package_version": os.environ["PROJECT_VERSION"],
    "checked_commands": checked,
    "available": available,
    "unavailable": unavailable,
    "solvers": solvers,
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
