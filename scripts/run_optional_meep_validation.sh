#!/usr/bin/env bash
set -euo pipefail

OSA_RUN_OPTIONAL_MEEP_VALIDATION="${OSA_RUN_OPTIONAL_MEEP_VALIDATION:-0}"
OSA_MEEP_VALIDATION_REPORT="${OSA_MEEP_VALIDATION_REPORT:-}"
OSA_MEEP_OUTPUT_DIR="${OSA_MEEP_OUTPUT_DIR:-/tmp/osa-meep-validation}"
MEEP_SPEC="examples/specs/missing_wavelength_meep_preview.json"
MEEP_GENERATED_ARTIFACT="${OSA_MEEP_OUTPUT_DIR}/meep_preview.py"
MEEP_VALIDATION_SCRIPT="${OSA_MEEP_OUTPUT_DIR}/meep_minimal_validation.py"
MEEP_OUTPUT_ARTIFACT="${OSA_MEEP_OUTPUT_DIR}/meep_validation_result.json"
MEEP_STDOUT="${OSA_MEEP_OUTPUT_DIR}/meep_stdout.log"
MEEP_STDERR="${OSA_MEEP_OUTPUT_DIR}/meep_stderr.log"

PROJECT_VERSION="$(python - <<'PY'
import tomllib
from pathlib import Path

with Path("pyproject.toml").open("rb") as handle:
    data = tomllib.load(handle)
print(data["project"]["version"])
PY
)"

MEEP_SOLVER_PYTHON="${OSA_SOLVER_PYTHON:-}"
PYTHON_BIN=""
PYTHON_SOURCE="current PATH"
if [[ -n "${MEEP_SOLVER_PYTHON}" ]]; then
  PYTHON_SOURCE="OSA_SOLVER_PYTHON"
  if [[ -x "${MEEP_SOLVER_PYTHON}" ]]; then
    PYTHON_BIN="${MEEP_SOLVER_PYTHON}"
  else
    echo "OSA_SOLVER_PYTHON is set but is not executable: ${MEEP_SOLVER_PYTHON}" >&2
  fi
else
  PYTHON_BIN="$(command -v python || true)"
fi
MEEP_AVAILABLE="false"
MEEP_VERSION=""
MEEP_EXECUTED="false"
PASSED="true"
LEVEL3_ACHIEVED="false"
COMMAND_RUN=""
RUN_STDOUT_SUMMARY=""
RUN_STDERR_SUMMARY=""
EXIT_CODE="0"

echo "Meep optional validation pilot for optical-spec-agent ${PROJECT_VERSION}"
echo "Input fixture: ${MEEP_SPEC}"
echo "Output directory: ${OSA_MEEP_OUTPUT_DIR}"
echo "Python source: ${PYTHON_SOURCE}"
echo "Python executable: ${PYTHON_BIN:-unavailable}"

if [[ -n "${PYTHON_BIN}" ]]; then
  MEEP_IMPORT_OUTPUT="$("${PYTHON_BIN}" - <<'PY' 2>/dev/null || true
import meep as mp
print(getattr(mp, "__version__", "unknown"))
PY
)"
  MEEP_VERSION="$(printf '%s\n' "${MEEP_IMPORT_OUTPUT}" | sed '/^[[:space:]]*$/d' | head -n 1)"
  if [[ -n "${MEEP_VERSION}" ]]; then
    MEEP_AVAILABLE="true"
    echo "PyMeep import detected: ${MEEP_VERSION}"
  else
    echo "PyMeep import detected: unavailable"
  fi
else
  echo "PyMeep import detected: unavailable"
fi

if [[ ! -f "${MEEP_SPEC}" ]]; then
  echo "Missing Meep fixture: ${MEEP_SPEC}" >&2
  exit 1
fi

mkdir -p "${OSA_MEEP_OUTPUT_DIR}"

if [[ "${OSA_RUN_OPTIONAL_MEEP_VALIDATION}" == "1" ]]; then
  if [[ "${MEEP_AVAILABLE}" != "true" ]]; then
    echo "Optional validation was enabled, but PyMeep is unavailable." >&2
    PASSED="false"
    EXIT_CODE="2"
  else
    echo "Optional validation enabled. Generating local Meep preview artifact."
    optical-spec adapter-generate "${MEEP_SPEC}" \
      --tool meep \
      --output "${MEEP_GENERATED_ARTIFACT}" \
      --allow-preview-defaults

    cat >"${MEEP_VALIDATION_SCRIPT}" <<'PY'
"""Tiny project-owned PyMeep validation path.

This script is generated into /tmp by run_optional_meep_validation.sh. It is
intentionally minimal: it verifies that the adapter-generated artifact exists
and contains a Meep Simulation scaffold, then runs a one-step 2D PyMeep sanity
simulation. It does not validate optical correctness or convergence.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import meep as mp


generated_artifact = Path(sys.argv[1])
output_artifact = Path(sys.argv[2])
artifact_text = generated_artifact.read_text(encoding="utf-8")

contains_simulation = "mp.Simulation" in artifact_text
if not contains_simulation:
    raise SystemExit("adapter-generated artifact does not contain mp.Simulation")

cell = mp.Vector3(1, 1, 0)
sources = [
    mp.Source(
        mp.GaussianSource(frequency=1.0, fwidth=0.2),
        component=mp.Ez,
        center=mp.Vector3(),
    )
]
sim = mp.Simulation(
    cell_size=cell,
    boundary_layers=[mp.PML(0.1)],
    sources=sources,
    resolution=10,
)
sim.run(until=0.01)

result = {
    "solver": "Meep / PyMeep",
    "solver_version": getattr(mp, "__version__", "unknown"),
    "adapter_generated_artifact": str(generated_artifact),
    "adapter_artifact_contains_simulation": contains_simulation,
    "validation_type": "tiny_project_owned_pilot",
    "ran_until": 0.01,
    "timesteps_expected": "one or more internal timesteps",
    "production_grade_validation_claimed": False,
    "formal_convergence_proof_claimed": False,
}
output_artifact.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print("PyMeep tiny validation passed")
print(json.dumps(result, sort_keys=True))
PY

    COMMAND_RUN="${PYTHON_BIN} ${MEEP_VALIDATION_SCRIPT} ${MEEP_GENERATED_ARTIFACT} ${MEEP_OUTPUT_ARTIFACT}"
    echo "Running explicit PyMeep pilot command into ${MEEP_OUTPUT_ARTIFACT}."
    set +e
    "${PYTHON_BIN}" "${MEEP_VALIDATION_SCRIPT}" "${MEEP_GENERATED_ARTIFACT}" "${MEEP_OUTPUT_ARTIFACT}" >"${MEEP_STDOUT}" 2>"${MEEP_STDERR}"
    EXIT_CODE="$?"
    set -e
    MEEP_EXECUTED="true"
    RUN_STDOUT_SUMMARY="$(tail -n 20 "${MEEP_STDOUT}" | tr '\n' ' ' | sed 's/[[:space:]]\\+/ /g' | cut -c 1-1000 || true)"
    RUN_STDERR_SUMMARY="$(tail -n 20 "${MEEP_STDERR}" | tr '\n' ' ' | sed 's/[[:space:]]\\+/ /g' | cut -c 1-1000 || true)"
    if [[ "${EXIT_CODE}" == "0" && -s "${MEEP_OUTPUT_ARTIFACT}" ]]; then
      PASSED="true"
      LEVEL3_ACHIEVED="true"
      echo "Optional Meep pilot passed."
    else
      PASSED="false"
      LEVEL3_ACHIEVED="false"
      echo "Optional Meep pilot failed with exit code ${EXIT_CODE}." >&2
    fi
  fi
else
  echo "OPTIONAL VALIDATION NOT ENABLED"
  echo "Default mode only checks PyMeep availability and fixture presence."
  echo "To run the manual pilot later, set OSA_RUN_OPTIONAL_MEEP_VALIDATION=1 after maintainer approval."
  echo "NO MEEP EXECUTION PERFORMED"
fi

if [[ -n "${OSA_MEEP_VALIDATION_REPORT}" ]]; then
  python - <<'PY' "${OSA_MEEP_VALIDATION_REPORT}" "${PROJECT_VERSION}" "${MEEP_AVAILABLE}" "${PYTHON_BIN}" "${MEEP_VERSION}" "${OSA_RUN_OPTIONAL_MEEP_VALIDATION}" "${MEEP_EXECUTED}" "${PASSED}" "${LEVEL3_ACHIEVED}" "${MEEP_SPEC}" "${MEEP_GENERATED_ARTIFACT}" "${MEEP_VALIDATION_SCRIPT}" "${MEEP_OUTPUT_ARTIFACT}" "${OSA_MEEP_OUTPUT_DIR}" "${COMMAND_RUN}" "${EXIT_CODE}" "${RUN_STDOUT_SUMMARY}" "${RUN_STDERR_SUMMARY}"
import json
import sys
from pathlib import Path

report_path = Path(sys.argv[1])
data = {
    "package_version": sys.argv[2],
    "meep_available": sys.argv[3] == "true",
    "python_executable": sys.argv[4] or None,
    "solver_version": sys.argv[5] or None,
    "optional_validation_enabled": sys.argv[6] == "1",
    "meep_executed": sys.argv[7] == "true",
    "passed": sys.argv[8] == "true",
    "level3_achieved": sys.argv[9] == "true",
    "production_grade_validation_claimed": False,
    "formal_convergence_proof_claimed": False,
    "proprietary_required": False,
    "input_fixture": sys.argv[10],
    "generated_artifact": sys.argv[11],
    "validation_script": sys.argv[12],
    "output_artifact": sys.argv[13],
    "output_dir": sys.argv[14],
    "command_run": sys.argv[15] or None,
    "exit_code": int(sys.argv[16]),
    "stdout_summary": sys.argv[17],
    "stderr_summary": sys.argv[18],
}
report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"Wrote Meep validation report: {report_path}")
PY
fi

if [[ "${MEEP_EXECUTED}" != "true" ]]; then
  echo "NO MEEP EXECUTION PERFORMED"
fi
echo "NO PRODUCTION-GRADE VALIDATION CLAIMED"
echo "NO FORMAL CONVERGENCE PROOF CLAIMED"
echo "NO PROPRIETARY SOLVER REQUIRED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
echo "NO UPLOAD PERFORMED"

if [[ "${OSA_RUN_OPTIONAL_MEEP_VALIDATION}" == "1" && "${PASSED}" != "true" ]]; then
  exit 3
fi
