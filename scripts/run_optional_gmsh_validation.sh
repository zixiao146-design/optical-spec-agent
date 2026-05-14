#!/usr/bin/env bash
set -euo pipefail

OSA_RUN_OPTIONAL_GMSH_VALIDATION="${OSA_RUN_OPTIONAL_GMSH_VALIDATION:-0}"
OSA_GMSH_VALIDATION_REPORT="${OSA_GMSH_VALIDATION_REPORT:-}"
OSA_GMSH_OUTPUT_DIR="${OSA_GMSH_OUTPUT_DIR:-/tmp/osa-gmsh-validation}"
GMSH_SPEC="examples/specs/gmsh_preview.json"
GMSH_GEO="${OSA_GMSH_OUTPUT_DIR}/gmsh_preview.geo"
GMSH_MESH="${OSA_GMSH_OUTPUT_DIR}/gmsh_preview.msh"

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
  echo "Gmsh command detected: ${GMSH_BIN}"
else
  GMSH_AVAILABLE="false"
  GMSH_BIN=""
  echo "Gmsh command detected: unavailable"
fi

if [[ ! -f "${GMSH_SPEC}" ]]; then
  echo "Missing Gmsh fixture: ${GMSH_SPEC}" >&2
  exit 1
fi

mkdir -p "${OSA_GMSH_OUTPUT_DIR}"

GMSH_EXECUTED="false"

if [[ "${OSA_RUN_OPTIONAL_GMSH_VALIDATION}" == "1" ]]; then
  if [[ "${GMSH_AVAILABLE}" != "true" ]]; then
    echo "Optional validation was enabled, but Gmsh is unavailable." >&2
    exit 2
  fi
  echo "Optional validation enabled. Generating local .geo preview artifact."
  optical-spec adapter-generate "${GMSH_SPEC}" --tool gmsh --output "${GMSH_GEO}"
  echo "Running explicit Gmsh pilot command into ${GMSH_MESH}."
  "${GMSH_BIN}" -2 "${GMSH_GEO}" -o "${GMSH_MESH}" -format msh2
  GMSH_EXECUTED="true"
else
  echo "OPTIONAL VALIDATION NOT ENABLED"
  echo "Default mode only checks availability and fixture presence."
  echo "To run the manual pilot later, set OSA_RUN_OPTIONAL_GMSH_VALIDATION=1 after maintainer approval."
  echo "NO GMSH EXECUTION PERFORMED"
fi

if [[ -n "${OSA_GMSH_VALIDATION_REPORT}" ]]; then
  python - <<'PY' "${OSA_GMSH_VALIDATION_REPORT}" "${PROJECT_VERSION}" "${GMSH_AVAILABLE}" "${OSA_RUN_OPTIONAL_GMSH_VALIDATION}" "${GMSH_EXECUTED}" "${GMSH_SPEC}" "${OSA_GMSH_OUTPUT_DIR}"
import json
import sys
from pathlib import Path

report_path = Path(sys.argv[1])
data = {
    "package_version": sys.argv[2],
    "gmsh_available": sys.argv[3] == "true",
    "optional_validation_enabled": sys.argv[4] == "1",
    "gmsh_executed": sys.argv[5] == "true",
    "production_grade_validation_claimed": False,
    "proprietary_required": False,
    "input_fixture": sys.argv[6],
    "output_dir": sys.argv[7],
}
report_path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print(f"Wrote Gmsh validation report: {report_path}")
PY
fi

if [[ "${GMSH_EXECUTED}" != "true" ]]; then
  echo "NO GMSH EXECUTION PERFORMED"
fi
echo "NO PRODUCTION-GRADE VALIDATION CLAIMED"
echo "NO PROPRIETARY SOLVER REQUIRED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
echo "NO UPLOAD PERFORMED"
