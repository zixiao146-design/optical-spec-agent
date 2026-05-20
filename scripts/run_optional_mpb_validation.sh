#!/usr/bin/env bash
set -euo pipefail

OSA_RUN_OPTIONAL_MPB_VALIDATION="${OSA_RUN_OPTIONAL_MPB_VALIDATION:-0}"
OSA_MPB_VALIDATION_REPORT="${OSA_MPB_VALIDATION_REPORT:-}"
OSA_MPB_OUTPUT_DIR="${OSA_MPB_OUTPUT_DIR:-/tmp/osa-mpb-validation}"
OSA_SOLVER_PYTHON="${OSA_SOLVER_PYTHON:-}"
MPB_SPEC="examples/specs/mpb_preview.json"
MPB_GENERATED_ARTIFACT="${OSA_MPB_OUTPUT_DIR}/mpb_preview.py"
MPB_VALIDATION_SCRIPT="${OSA_MPB_OUTPUT_DIR}/mpb_minimal_validation.py"
MPB_OUTPUT_ARTIFACT="${OSA_MPB_OUTPUT_DIR}/mpb_validation_result.json"
MPB_STDOUT="${OSA_MPB_OUTPUT_DIR}/mpb_stdout.log"
MPB_STDERR="${OSA_MPB_OUTPUT_DIR}/mpb_stderr.log"

PROJECT_VERSION="$(python - <<'PY'
import tomllib
from pathlib import Path

with Path("pyproject.toml").open("rb") as handle:
    data = tomllib.load(handle)
print(data["project"]["version"])
PY
)"

if [[ -n "${OSA_SOLVER_PYTHON}" ]]; then
  PYTHON_BIN="${OSA_SOLVER_PYTHON}"
else
  PYTHON_BIN="$(command -v python || true)"
fi
MPB_CLI_AVAILABLE="false"
MPB_CLI_PATH=""
MPB_AVAILABLE="false"
MPB_VERSION=""
MPB_EXECUTED="false"
PASSED="true"
LEVEL3_ACHIEVED="false"
COMMAND_RUN=""
RUN_STDOUT_SUMMARY=""
RUN_STDERR_SUMMARY=""
EXIT_CODE="0"

echo "MPB optional validation pilot for optical-spec-agent ${PROJECT_VERSION}"
echo "Input fixture: ${MPB_SPEC}"
echo "Output directory: ${OSA_MPB_OUTPUT_DIR}"
echo "Python executable: ${PYTHON_BIN:-unavailable}"
if [[ -n "${OSA_SOLVER_PYTHON}" ]]; then
  echo "Python source: OSA_SOLVER_PYTHON"
else
  echo "Python source: current PATH"
fi

if [[ -n "${OSA_SOLVER_PYTHON}" && ! -x "${OSA_SOLVER_PYTHON}" ]]; then
  echo "OSA_SOLVER_PYTHON is set but is not executable: ${OSA_SOLVER_PYTHON}" >&2
  exit 2
fi

if MPB_CLI_PATH="$(command -v mpb 2>/dev/null || true)" && [[ -n "${MPB_CLI_PATH}" ]]; then
  MPB_CLI_AVAILABLE="true"
  echo "MPB CLI detected: ${MPB_CLI_PATH}"
else
  echo "MPB CLI detected: unavailable; Python meep.mpb path is sufficient for this pilot"
fi

if [[ -n "${PYTHON_BIN}" ]]; then
  MPB_IMPORT_OUTPUT="$("${PYTHON_BIN}" - <<'PY' 2>/dev/null || true
import meep as mp
from meep import mpb
print(getattr(mp, "__version__", "unknown"))
PY
)"
  MPB_VERSION="$(printf '%s\n' "${MPB_IMPORT_OUTPUT}" | sed '/^[[:space:]]*$/d' | head -n 1)"
  if [[ -n "${MPB_VERSION}" ]]; then
    MPB_AVAILABLE="true"
    echo "MPB Python path detected through meep.mpb; PyMeep version: ${MPB_VERSION}"
  else
    echo "MPB Python path detected: unavailable"
  fi
else
  echo "MPB Python path detected: unavailable"
fi

if [[ ! -f "${MPB_SPEC}" ]]; then
  echo "Missing MPB fixture: ${MPB_SPEC}" >&2
  exit 1
fi

mkdir -p "${OSA_MPB_OUTPUT_DIR}"

if [[ "${OSA_RUN_OPTIONAL_MPB_VALIDATION}" == "1" ]]; then
  if [[ "${MPB_AVAILABLE}" != "true" ]]; then
    echo "Optional validation was enabled, but meep.mpb is unavailable." >&2
    PASSED="false"
    EXIT_CODE="2"
  else
    echo "Optional validation enabled. Generating local MPB preview artifact."
    optical-spec adapter-generate "${MPB_SPEC}" \
      --tool mpb \
      --output "${MPB_GENERATED_ARTIFACT}"

    cat >"${MPB_VALIDATION_SCRIPT}" <<'PY'
"""Tiny project-owned MPB validation path.

This script is generated into /tmp by run_optional_mpb_validation.sh. It
verifies that the adapter-generated artifact exists and contains an MPB
ModeSolver scaffold, then runs a tiny MPB solve with one k-point, one band, and
low resolution. It does not validate photonic-band correctness or convergence.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import meep as mp
from meep import mpb


generated_artifact = Path(sys.argv[1])
output_artifact = Path(sys.argv[2])
artifact_text = generated_artifact.read_text(encoding="utf-8")

contains_python_path = "from meep import mpb" in artifact_text
contains_mode_solver = "mpb.ModeSolver" in artifact_text
if not (contains_python_path and contains_mode_solver):
    raise SystemExit("adapter-generated artifact does not contain the expected MPB scaffold")

mode_solver = mpb.ModeSolver(
    num_bands=1,
    k_points=[mp.Vector3()],
    geometry=[],
    geometry_lattice=mp.Lattice(size=mp.Vector3(1, 1)),
    resolution=4,
)
mode_solver.run_te()

result = {
    "solver": "MPB via PyMeep",
    "solver_version": getattr(mp, "__version__", "unknown"),
    "adapter_generated_artifact": str(generated_artifact),
    "adapter_artifact_contains_python_path": contains_python_path,
    "adapter_artifact_contains_mode_solver": contains_mode_solver,
    "validation_type": "tiny_project_owned_mpb_pilot",
    "k_points": 1,
    "num_bands": 1,
    "resolution": 4,
    "frequencies_recorded": len(getattr(mode_solver, "all_freqs", []) or []),
    "production_grade_validation_claimed": False,
    "production_grade_mpb_validation_claimed": False,
    "production_band_structure_validation_claimed": False,
    "formal_convergence_proof_claimed": False,
    "optical_correctness_claimed": False,
    "meep_fdtd_benchmark_executed": False,
}
output_artifact.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print("MPB tiny validation passed")
print(json.dumps(result, sort_keys=True))
PY

    COMMAND_RUN="${PYTHON_BIN} ${MPB_VALIDATION_SCRIPT} ${MPB_GENERATED_ARTIFACT} ${MPB_OUTPUT_ARTIFACT}"
    echo "Running explicit MPB pilot command into ${MPB_OUTPUT_ARTIFACT}."
    set +e
    "${PYTHON_BIN}" "${MPB_VALIDATION_SCRIPT}" "${MPB_GENERATED_ARTIFACT}" "${MPB_OUTPUT_ARTIFACT}" >"${MPB_STDOUT}" 2>"${MPB_STDERR}"
    EXIT_CODE="$?"
    set -e
    MPB_EXECUTED="true"
    RUN_STDOUT_SUMMARY="$(tail -n 30 "${MPB_STDOUT}" | tr '\n' ' ' | sed 's/[[:space:]]\\+/ /g' | cut -c 1-1200 || true)"
    RUN_STDERR_SUMMARY="$(tail -n 20 "${MPB_STDERR}" | tr '\n' ' ' | sed 's/[[:space:]]\\+/ /g' | cut -c 1-1000 || true)"
    if [[ "${EXIT_CODE}" == "0" && -s "${MPB_OUTPUT_ARTIFACT}" ]]; then
      PASSED="true"
      LEVEL3_ACHIEVED="true"
      echo "Optional MPB pilot passed."
    else
      PASSED="false"
      LEVEL3_ACHIEVED="false"
      echo "Optional MPB pilot failed with exit code ${EXIT_CODE}." >&2
    fi
  fi
else
  echo "OPTIONAL VALIDATION NOT ENABLED"
  echo "Default mode only checks meep.mpb availability and fixture presence."
  echo "To run the manual pilot later, set OSA_RUN_OPTIONAL_MPB_VALIDATION=1 after maintainer approval."
  echo "NO MPB EXECUTION PERFORMED"
fi

if [[ -n "${OSA_MPB_VALIDATION_REPORT}" ]]; then
  python - <<'PY' "${OSA_MPB_VALIDATION_REPORT}" "${PROJECT_VERSION}" "${MPB_AVAILABLE}" "${MPB_CLI_AVAILABLE}" "${MPB_CLI_PATH}" "${PYTHON_BIN}" "${MPB_VERSION}" "${OSA_RUN_OPTIONAL_MPB_VALIDATION}" "${MPB_EXECUTED}" "${PASSED}" "${LEVEL3_ACHIEVED}" "${MPB_SPEC}" "${MPB_GENERATED_ARTIFACT}" "${MPB_VALIDATION_SCRIPT}" "${MPB_OUTPUT_ARTIFACT}" "${OSA_MPB_OUTPUT_DIR}" "${COMMAND_RUN}" "${EXIT_CODE}" "${RUN_STDOUT_SUMMARY}" "${RUN_STDERR_SUMMARY}"
import json
import sys
from pathlib import Path

report_path = Path(sys.argv[1])
data = {
    "package_version": sys.argv[2],
    "mpb_available": sys.argv[3] == "true",
    "mpb_cli_available": sys.argv[4] == "true",
    "mpb_cli_path": sys.argv[5] or None,
    "python_executable": sys.argv[6] or None,
    "solver_python_env_var": "OSA_SOLVER_PYTHON",
    "solver_version": sys.argv[7] or None,
    "optional_validation_enabled": sys.argv[8] == "1",
    "mpb_executed": sys.argv[9] == "true",
    "passed": sys.argv[10] == "true",
    "level3_achieved": sys.argv[11] == "true",
    "production_grade_validation_claimed": False,
    "production_grade_mpb_validation_claimed": False,
    "production_band_structure_validation_claimed": False,
    "formal_convergence_proof_claimed": False,
    "optical_correctness_claimed": False,
    "proprietary_required": False,
    "meep_fdtd_benchmark_executed": False,
    "gmsh_executed": False,
    "optiland_executed": False,
    "elmer_executed": False,
    "external_solver_executed": sys.argv[9] == "true",
    "input_fixture": sys.argv[12],
    "generated_artifact": sys.argv[13],
    "validation_script": sys.argv[14],
    "output_artifact": sys.argv[15],
    "output_dir": sys.argv[16],
    "command_run": sys.argv[17] or None,
    "exit_code": int(sys.argv[18]),
    "stdout_summary": sys.argv[19],
    "stderr_summary": sys.argv[20],
}
report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"Wrote MPB validation report: {report_path}")
PY
fi

if [[ "${MPB_EXECUTED}" != "true" ]]; then
  echo "NO MPB EXECUTION PERFORMED"
fi
echo "NO PRODUCTION-GRADE VALIDATION CLAIMED"
echo "NO FORMAL CONVERGENCE PROOF CLAIMED"
echo "NO PROPRIETARY SOLVER REQUIRED"
echo "NO MPB CLI REQUIRED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
echo "NO UPLOAD PERFORMED"

if [[ "${OSA_RUN_OPTIONAL_MPB_VALIDATION}" == "1" && "${PASSED}" != "true" ]]; then
  exit 3
fi
