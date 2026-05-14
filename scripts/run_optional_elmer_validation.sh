#!/usr/bin/env bash
set -euo pipefail

OSA_RUN_OPTIONAL_ELMER_VALIDATION="${OSA_RUN_OPTIONAL_ELMER_VALIDATION:-0}"
OSA_ELMER_VALIDATION_REPORT="${OSA_ELMER_VALIDATION_REPORT:-}"
OSA_ELMER_OUTPUT_DIR="${OSA_ELMER_OUTPUT_DIR:-/tmp/osa-elmer-validation}"
ELMER_SPEC="examples/specs/elmer_preview.json"
ELMER_MESH="examples/meshes/waveguide.msh"
ELMER_GENERATED_ARTIFACT="${OSA_ELMER_OUTPUT_DIR}/case.sif"
ELMER_STDOUT="${OSA_ELMER_OUTPUT_DIR}/elmer_stdout.log"
ELMER_STDERR="${OSA_ELMER_OUTPUT_DIR}/elmer_stderr.log"

PROJECT_VERSION="$(python - <<'PY'
import tomllib
from pathlib import Path

with Path("pyproject.toml").open("rb") as handle:
    data = tomllib.load(handle)
print(data["project"]["version"])
PY
)"

ELMER_PATH="$(command -v ElmerSolver || true)"
ELMER_AVAILABLE="false"
ELMER_VERSION=""
ELMER_EXECUTED="false"
PASSED="true"
LEVEL3_ACHIEVED="false"
COMMAND_RUN=""
RUN_STDOUT_SUMMARY=""
RUN_STDERR_SUMMARY=""
EXIT_CODE="0"

echo "Elmer optional validation pilot for optical-spec-agent ${PROJECT_VERSION}"
echo "Input fixture: ${ELMER_SPEC}"
echo "Output directory: ${OSA_ELMER_OUTPUT_DIR}"

if [[ -n "${ELMER_PATH}" ]]; then
  ELMER_AVAILABLE="true"
  echo "ElmerSolver command detected: ${ELMER_PATH}"
  ELMER_VERSION="$("${ELMER_PATH}" --version 2>/dev/null | head -n 1 || true)"
  if [[ -n "${ELMER_VERSION}" ]]; then
    echo "ElmerSolver version: ${ELMER_VERSION}"
  else
    echo "ElmerSolver version: unavailable from --version"
  fi
else
  echo "ElmerSolver command detected: unavailable"
fi

if [[ ! -f "${ELMER_SPEC}" ]]; then
  echo "Missing Elmer fixture: ${ELMER_SPEC}" >&2
  exit 1
fi

mkdir -p "${OSA_ELMER_OUTPUT_DIR}"

if [[ "${OSA_RUN_OPTIONAL_ELMER_VALIDATION}" == "1" ]]; then
  if [[ "${ELMER_AVAILABLE}" != "true" ]]; then
    echo "Optional validation was enabled, but ElmerSolver is unavailable." >&2
    PASSED="false"
    EXIT_CODE="2"
  else
    echo "Optional validation enabled. Generating local Elmer SIF artifact."
    optical-spec adapter-generate "${ELMER_SPEC}" \
      --tool elmer \
      --mesh "${ELMER_MESH}" \
      --output "${ELMER_GENERATED_ARTIFACT}"

    COMMAND_RUN="${ELMER_PATH} ${ELMER_GENERATED_ARTIFACT}"
    echo "Running explicit Elmer pilot command with ${ELMER_GENERATED_ARTIFACT}."
    set +e
    "${ELMER_PATH}" "${ELMER_GENERATED_ARTIFACT}" >"${ELMER_STDOUT}" 2>"${ELMER_STDERR}"
    EXIT_CODE="$?"
    set -e
    ELMER_EXECUTED="true"
    RUN_STDOUT_SUMMARY="$(tail -n 30 "${ELMER_STDOUT}" | tr '\n' ' ' | sed 's/[[:space:]]\\+/ /g' | cut -c 1-1200 || true)"
    RUN_STDERR_SUMMARY="$(tail -n 20 "${ELMER_STDERR}" | tr '\n' ' ' | sed 's/[[:space:]]\\+/ /g' | cut -c 1-1000 || true)"
    if [[ "${EXIT_CODE}" == "0" ]]; then
      PASSED="true"
      LEVEL3_ACHIEVED="true"
      echo "Optional Elmer pilot passed."
    else
      PASSED="false"
      LEVEL3_ACHIEVED="false"
      echo "Optional Elmer pilot failed with exit code ${EXIT_CODE}." >&2
    fi
  fi
else
  echo "OPTIONAL VALIDATION NOT ENABLED"
  echo "Default mode only checks ElmerSolver availability and fixture presence."
  echo "To run the manual pilot later, set OSA_RUN_OPTIONAL_ELMER_VALIDATION=1 after maintainer approval."
  echo "NO ELMER EXECUTION PERFORMED"
fi

if [[ -n "${OSA_ELMER_VALIDATION_REPORT}" ]]; then
  python - <<'PY' "${OSA_ELMER_VALIDATION_REPORT}" "${PROJECT_VERSION}" "${ELMER_AVAILABLE}" "${ELMER_PATH}" "${ELMER_VERSION}" "${OSA_RUN_OPTIONAL_ELMER_VALIDATION}" "${ELMER_EXECUTED}" "${PASSED}" "${LEVEL3_ACHIEVED}" "${ELMER_SPEC}" "${ELMER_GENERATED_ARTIFACT}" "${OSA_ELMER_OUTPUT_DIR}" "${COMMAND_RUN}" "${EXIT_CODE}" "${RUN_STDOUT_SUMMARY}" "${RUN_STDERR_SUMMARY}"
import json
import sys
from pathlib import Path

report_path = Path(sys.argv[1])
data = {
    "package_version": sys.argv[2],
    "elmer_available": sys.argv[3] == "true",
    "solver_path": sys.argv[4] or None,
    "solver_version": sys.argv[5] or None,
    "optional_validation_enabled": sys.argv[6] == "1",
    "elmer_executed": sys.argv[7] == "true",
    "passed": sys.argv[8] == "true",
    "level3_achieved": sys.argv[9] == "true",
    "production_grade_validation_claimed": False,
    "formal_convergence_proof_claimed": False,
    "proprietary_required": False,
    "input_fixture": sys.argv[10],
    "generated_artifact": sys.argv[11],
    "output_dir": sys.argv[12],
    "command_run": sys.argv[13] or None,
    "exit_code": int(sys.argv[14]),
    "stdout_summary": sys.argv[15],
    "stderr_summary": sys.argv[16],
}
report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"Wrote Elmer validation report: {report_path}")
PY
fi

if [[ "${ELMER_EXECUTED}" != "true" ]]; then
  echo "NO ELMER EXECUTION PERFORMED"
fi
echo "NO PRODUCTION-GRADE VALIDATION CLAIMED"
echo "NO FORMAL CONVERGENCE PROOF CLAIMED"
echo "NO PROPRIETARY SOLVER REQUIRED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
echo "NO UPLOAD PERFORMED"

if [[ "${OSA_RUN_OPTIONAL_ELMER_VALIDATION}" == "1" && "${PASSED}" != "true" ]]; then
  exit 3
fi
