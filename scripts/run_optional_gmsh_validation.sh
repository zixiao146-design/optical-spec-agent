#!/usr/bin/env bash
set -euo pipefail

OSA_RUN_OPTIONAL_GMSH_VALIDATION="${OSA_RUN_OPTIONAL_GMSH_VALIDATION:-0}"
OSA_GMSH_VALIDATION_REPORT="${OSA_GMSH_VALIDATION_REPORT:-}"
OSA_GMSH_OUTPUT_DIR="${OSA_GMSH_OUTPUT_DIR:-/tmp/osa-gmsh-validation}"
GMSH_SPEC="examples/specs/gmsh_preview.json"
GMSH_GEO="${OSA_GMSH_OUTPUT_DIR}/gmsh_preview.geo"
GMSH_MESH="${OSA_GMSH_OUTPUT_DIR}/gmsh_preview.msh"
GMSH_STDOUT="${OSA_GMSH_OUTPUT_DIR}/gmsh_stdout.log"
GMSH_STDERR="${OSA_GMSH_OUTPUT_DIR}/gmsh_stderr.log"

PROJECT_VERSION="$(python - <<'PY'
import tomllib
from pathlib import Path

with Path("pyproject.toml").open("rb") as handle:
    data = tomllib.load(handle)
print(data["project"]["version"])
PY
)"

echo "Gmsh optional validation pilot for optical-spec-agent ${PROJECT_VERSION}"
echo "Input fixture: ${GMSH_SPEC}"
echo "Output directory: ${OSA_GMSH_OUTPUT_DIR}"

if command -v gmsh >/dev/null 2>&1; then
  GMSH_AVAILABLE="true"
  GMSH_BIN="$(command -v gmsh)"
  GMSH_VERSION=""
  echo "Gmsh command detected: ${GMSH_BIN}"
  echo "Gmsh version: not checked in default detection mode"
else
  GMSH_AVAILABLE="false"
  GMSH_BIN=""
  GMSH_VERSION=""
  echo "Gmsh command detected: unavailable"
fi

if [[ ! -f "${GMSH_SPEC}" ]]; then
  echo "Missing Gmsh fixture: ${GMSH_SPEC}" >&2
  exit 1
fi

mkdir -p "${OSA_GMSH_OUTPUT_DIR}"

GMSH_EXECUTED="false"
PASSED="true"
LEVEL3_ACHIEVED="false"
COMMAND_RUN=""
RUN_STDOUT_SUMMARY=""
RUN_STDERR_SUMMARY=""
EXIT_CODE="0"

if [[ "${OSA_RUN_OPTIONAL_GMSH_VALIDATION}" == "1" ]]; then
  if [[ "${GMSH_AVAILABLE}" != "true" ]]; then
    echo "Optional validation was enabled, but Gmsh is unavailable." >&2
    PASSED="false"
    EXIT_CODE="2"
    if [[ -n "${OSA_GMSH_VALIDATION_REPORT}" ]]; then
      python - <<'PY' "${OSA_GMSH_VALIDATION_REPORT}" "${PROJECT_VERSION}" "${GMSH_AVAILABLE}" "${GMSH_BIN}" "${GMSH_VERSION}" "${OSA_RUN_OPTIONAL_GMSH_VALIDATION}" "${GMSH_EXECUTED}" "${PASSED}" "${LEVEL3_ACHIEVED}" "${GMSH_SPEC}" "${GMSH_GEO}" "${GMSH_MESH}" "${OSA_GMSH_OUTPUT_DIR}" "${COMMAND_RUN}" "${EXIT_CODE}" "${RUN_STDOUT_SUMMARY}" "${RUN_STDERR_SUMMARY}"
import json
import sys
from pathlib import Path

report_path = Path(sys.argv[1])
data = {
    "package_version": sys.argv[2],
    "gmsh_available": sys.argv[3] == "true",
    "solver_path": sys.argv[4] or None,
    "solver_version": sys.argv[5] or None,
    "optional_validation_enabled": sys.argv[6] == "1",
    "gmsh_executed": sys.argv[7] == "true",
    "passed": sys.argv[8] == "true",
    "level3_achieved": sys.argv[9] == "true",
    "production_grade_validation_claimed": False,
    "formal_convergence_proof_claimed": False,
    "proprietary_required": False,
    "input_fixture": sys.argv[10],
    "generated_artifact": sys.argv[11],
    "output_artifact": sys.argv[12],
    "output_dir": sys.argv[13],
    "command_run": sys.argv[14] or None,
    "exit_code": int(sys.argv[15]),
    "stdout_summary": sys.argv[16],
    "stderr_summary": sys.argv[17],
}
report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"Wrote Gmsh validation report: {report_path}")
PY
    fi
    exit 2
  fi
  GMSH_VERSION="$("${GMSH_BIN}" --version 2>/dev/null | head -n 1 || true)"
  echo "Gmsh version: ${GMSH_VERSION:-unknown}"
  echo "Optional validation enabled. Generating local .geo preview artifact."
  optical-spec adapter-generate "${GMSH_SPEC}" --tool gmsh --output "${GMSH_GEO}"
  if grep -Eq '(^|[^A-Za-z])(Extrude|Volume|Physical Volume)' "${GMSH_GEO}"; then
    GMSH_DIMENSION_FLAG="-3"
  else
    GMSH_DIMENSION_FLAG="-2"
  fi
  COMMAND_RUN="${GMSH_BIN} ${GMSH_DIMENSION_FLAG} ${GMSH_GEO} -format msh2 -o ${GMSH_MESH}"
  echo "Running explicit Gmsh pilot command into ${GMSH_MESH}."
  set +e
  "${GMSH_BIN}" "${GMSH_DIMENSION_FLAG}" "${GMSH_GEO}" -format msh2 -o "${GMSH_MESH}" >"${GMSH_STDOUT}" 2>"${GMSH_STDERR}"
  EXIT_CODE="$?"
  set -e
  GMSH_EXECUTED="true"
  RUN_STDOUT_SUMMARY="$(tail -n 20 "${GMSH_STDOUT}" | tr '\n' ' ' | sed 's/[[:space:]]\\+/ /g' | cut -c 1-1000 || true)"
  RUN_STDERR_SUMMARY="$(tail -n 20 "${GMSH_STDERR}" | tr '\n' ' ' | sed 's/[[:space:]]\\+/ /g' | cut -c 1-1000 || true)"
  if [[ "${EXIT_CODE}" == "0" && -s "${GMSH_MESH}" ]]; then
    PASSED="true"
    LEVEL3_ACHIEVED="true"
    echo "Optional Gmsh pilot passed."
  else
    PASSED="false"
    LEVEL3_ACHIEVED="false"
    echo "Optional Gmsh pilot failed with exit code ${EXIT_CODE}." >&2
  fi
else
  echo "OPTIONAL VALIDATION NOT ENABLED"
  echo "Default mode only checks availability and fixture presence."
  echo "To run the manual pilot later, set OSA_RUN_OPTIONAL_GMSH_VALIDATION=1 after maintainer approval."
  echo "NO GMSH EXECUTION PERFORMED"
fi

if [[ -n "${OSA_GMSH_VALIDATION_REPORT}" ]]; then
  python - <<'PY' "${OSA_GMSH_VALIDATION_REPORT}" "${PROJECT_VERSION}" "${GMSH_AVAILABLE}" "${GMSH_BIN}" "${GMSH_VERSION}" "${OSA_RUN_OPTIONAL_GMSH_VALIDATION}" "${GMSH_EXECUTED}" "${PASSED}" "${LEVEL3_ACHIEVED}" "${GMSH_SPEC}" "${GMSH_GEO}" "${GMSH_MESH}" "${OSA_GMSH_OUTPUT_DIR}" "${COMMAND_RUN}" "${EXIT_CODE}" "${RUN_STDOUT_SUMMARY}" "${RUN_STDERR_SUMMARY}"
import json
import sys
from pathlib import Path

report_path = Path(sys.argv[1])
data = {
    "package_version": sys.argv[2],
    "gmsh_available": sys.argv[3] == "true",
    "solver_path": sys.argv[4] or None,
    "solver_version": sys.argv[5] or None,
    "optional_validation_enabled": sys.argv[6] == "1",
    "gmsh_executed": sys.argv[7] == "true",
    "passed": sys.argv[8] == "true",
    "level3_achieved": sys.argv[9] == "true",
    "production_grade_validation_claimed": False,
    "formal_convergence_proof_claimed": False,
    "proprietary_required": False,
    "input_fixture": sys.argv[10],
    "generated_artifact": sys.argv[11],
    "output_artifact": sys.argv[12],
    "output_dir": sys.argv[13],
    "command_run": sys.argv[14] or None,
    "exit_code": int(sys.argv[15]),
    "stdout_summary": sys.argv[16],
    "stderr_summary": sys.argv[17],
}
report_path.parent.mkdir(parents=True, exist_ok=True)
report_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"Wrote Gmsh validation report: {report_path}")
PY
fi

if [[ "${GMSH_EXECUTED}" != "true" ]]; then
  echo "NO GMSH EXECUTION PERFORMED"
fi
echo "NO PRODUCTION-GRADE VALIDATION CLAIMED"
echo "NO FORMAL CONVERGENCE PROOF CLAIMED"
echo "NO PROPRIETARY SOLVER REQUIRED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
echo "NO UPLOAD PERFORMED"

if [[ "${OSA_RUN_OPTIONAL_GMSH_VALIDATION}" == "1" && "${PASSED}" != "true" ]]; then
  exit 3
fi
