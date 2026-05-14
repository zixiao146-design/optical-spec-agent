#!/usr/bin/env bash
set -euo pipefail

OSA_RUN_OPTIONAL_OPTILAND_VALIDATION="${OSA_RUN_OPTIONAL_OPTILAND_VALIDATION:-0}"
OSA_OPTILAND_VALIDATION_REPORT="${OSA_OPTILAND_VALIDATION_REPORT:-}"
OSA_OPTILAND_OUTPUT_DIR="${OSA_OPTILAND_OUTPUT_DIR:-/tmp/osa-optiland-validation}"
OPTILAND_SPEC="examples/specs/optiland_preview.json"
OPTILAND_GENERATED_ARTIFACT="${OSA_OPTILAND_OUTPUT_DIR}/optiland_preview.py"
OPTILAND_VALIDATION_SCRIPT="${OSA_OPTILAND_OUTPUT_DIR}/optiland_minimal_validation.py"
OPTILAND_OUTPUT_ARTIFACT="${OSA_OPTILAND_OUTPUT_DIR}/optiland_validation_result.json"
OPTILAND_STDOUT="${OSA_OPTILAND_OUTPUT_DIR}/optiland_stdout.log"
OPTILAND_STDERR="${OSA_OPTILAND_OUTPUT_DIR}/optiland_stderr.log"

PROJECT_VERSION="$(python - <<'PY'
import tomllib
from pathlib import Path

with Path("pyproject.toml").open("rb") as handle:
    data = tomllib.load(handle)
print(data["project"]["version"])
PY
)"

PYTHON_BIN="$(command -v python || true)"
OPTILAND_AVAILABLE="false"
OPTILAND_VERSION=""
OPTILAND_EXECUTED="false"
PASSED="true"
LEVEL3_ACHIEVED="false"
COMMAND_RUN=""
RUN_STDOUT_SUMMARY=""
RUN_STDERR_SUMMARY=""
EXIT_CODE="0"

echo "Optiland optional validation pilot for optical-spec-agent ${PROJECT_VERSION}"
echo "Input fixture: ${OPTILAND_SPEC}"
echo "Output directory: ${OSA_OPTILAND_OUTPUT_DIR}"
echo "Python executable: ${PYTHON_BIN:-unavailable}"

if [[ -n "${PYTHON_BIN}" ]]; then
  OPTILAND_IMPORT_OUTPUT="$("${PYTHON_BIN}" - <<'PY' 2>/dev/null || true
import optiland
print(getattr(optiland, "__version__", "unknown"))
PY
)"
  OPTILAND_VERSION="$(printf '%s\n' "${OPTILAND_IMPORT_OUTPUT}" | sed '/^[[:space:]]*$/d' | head -n 1)"
  if [[ -n "${OPTILAND_VERSION}" ]]; then
    OPTILAND_AVAILABLE="true"
    echo "Optiland Python import detected; version: ${OPTILAND_VERSION}"
  else
    echo "Optiland Python import detected: unavailable"
  fi
else
  echo "Optiland Python import detected: unavailable"
fi

if [[ ! -f "${OPTILAND_SPEC}" ]]; then
  echo "Missing Optiland fixture: ${OPTILAND_SPEC}" >&2
  exit 1
fi

mkdir -p "${OSA_OPTILAND_OUTPUT_DIR}"

if [[ "${OSA_RUN_OPTIONAL_OPTILAND_VALIDATION}" == "1" ]]; then
  if [[ "${OPTILAND_AVAILABLE}" != "true" ]]; then
    echo "Optional validation was enabled, but Optiland is unavailable." >&2
    PASSED="false"
    EXIT_CODE="2"
  else
    echo "Optional validation enabled. Generating local Optiland preview artifact."
    optical-spec adapter-generate "${OPTILAND_SPEC}" \
      --tool optiland \
      --output "${OPTILAND_GENERATED_ARTIFACT}"

    cat >"${OPTILAND_VALIDATION_SCRIPT}" <<'PY'
"""Tiny project-owned Optiland validation path.

This script is generated into /tmp by run_optional_optiland_validation.sh. It
verifies that the adapter-generated scaffold exists and contains the expected
Optiland guarded import, then constructs a minimal Optiland object graph with
one wavelength, one field, and one entrance-pupil aperture. It does not run a
long optimization, prove optical correctness, or claim production readiness.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import optiland
from optiland.optic import Optic


generated_artifact = Path(sys.argv[1])
output_artifact = Path(sys.argv[2])
artifact_text = generated_artifact.read_text(encoding="utf-8")

contains_import = "import optiland" in artifact_text
contains_scaffold = "Optiland scaffold" in artifact_text
contains_builder = "def build_optical_system" in artifact_text
if not (contains_import and contains_scaffold and contains_builder):
    raise SystemExit("adapter-generated artifact does not contain the expected Optiland scaffold")

optic = Optic(name="osa-optiland-tiny-pilot")
optic.wavelengths.add(0.55, is_primary=True, unit="um")
optic.fields.add(y=0.0, x=0.0)
optic.set_aperture("EPD", 1.0)
optic_dict = optic.to_dict()

result = {
    "backend": "Optiland",
    "backend_version": getattr(optiland, "__version__", "unknown"),
    "adapter_generated_artifact": str(generated_artifact),
    "adapter_artifact_contains_import": contains_import,
    "adapter_artifact_contains_scaffold": contains_scaffold,
    "adapter_artifact_contains_builder": contains_builder,
    "validation_type": "tiny_project_owned_optiland_pilot",
    "optic_type": type(optic).__name__,
    "num_wavelengths": optic.wavelengths.num_wavelengths,
    "num_fields": optic.fields.num_fields,
    "serialized_keys": sorted(optic_dict.keys()),
    "production_grade_validation_claimed": False,
    "formal_convergence_proof_claimed": False,
}
output_artifact.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
print("Optiland tiny validation passed")
print(json.dumps(result, sort_keys=True))
PY

    COMMAND_RUN="${PYTHON_BIN} ${OPTILAND_VALIDATION_SCRIPT} ${OPTILAND_GENERATED_ARTIFACT} ${OPTILAND_OUTPUT_ARTIFACT}"
    echo "Running explicit Optiland pilot command into ${OPTILAND_OUTPUT_ARTIFACT}."
    set +e
    "${PYTHON_BIN}" "${OPTILAND_VALIDATION_SCRIPT}" "${OPTILAND_GENERATED_ARTIFACT}" "${OPTILAND_OUTPUT_ARTIFACT}" >"${OPTILAND_STDOUT}" 2>"${OPTILAND_STDERR}"
    EXIT_CODE="$?"
    set -e
    OPTILAND_EXECUTED="true"
    RUN_STDOUT_SUMMARY="$(tail -n 30 "${OPTILAND_STDOUT}" | tr '\n' ' ' | sed 's/[[:space:]]\\+/ /g' | cut -c 1-1200 || true)"
    RUN_STDERR_SUMMARY="$(tail -n 20 "${OPTILAND_STDERR}" | tr '\n' ' ' | sed 's/[[:space:]]\\+/ /g' | cut -c 1-1000 || true)"
    if [[ "${EXIT_CODE}" == "0" && -s "${OPTILAND_OUTPUT_ARTIFACT}" ]]; then
      PASSED="true"
      LEVEL3_ACHIEVED="true"
      echo "Optional Optiland pilot passed."
    else
      PASSED="false"
      LEVEL3_ACHIEVED="false"
      echo "Optional Optiland pilot failed with exit code ${EXIT_CODE}." >&2
    fi
  fi
else
  echo "OPTIONAL VALIDATION NOT ENABLED"
  echo "Default mode only checks Optiland availability and fixture presence."
  echo "To run the manual pilot later, set OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1 after maintainer approval."
  echo "NO OPTILAND EXECUTION PERFORMED"
fi

if [[ -n "${OSA_OPTILAND_VALIDATION_REPORT}" ]]; then
  python - <<'PY' "${OSA_OPTILAND_VALIDATION_REPORT}" "${PROJECT_VERSION}" "${OPTILAND_AVAILABLE}" "${PYTHON_BIN}" "${OPTILAND_VERSION}" "${OSA_RUN_OPTIONAL_OPTILAND_VALIDATION}" "${OPTILAND_EXECUTED}" "${PASSED}" "${LEVEL3_ACHIEVED}" "${OPTILAND_SPEC}" "${OPTILAND_GENERATED_ARTIFACT}" "${OPTILAND_VALIDATION_SCRIPT}" "${OPTILAND_OUTPUT_ARTIFACT}" "${OSA_OPTILAND_OUTPUT_DIR}" "${COMMAND_RUN}" "${EXIT_CODE}" "${RUN_STDOUT_SUMMARY}" "${RUN_STDERR_SUMMARY}"
import json
import sys
from pathlib import Path

report_path = Path(sys.argv[1])
data = {
    "package_version": sys.argv[2],
    "optiland_available": sys.argv[3] == "true",
    "python_executable": sys.argv[4] or None,
    "backend_version": sys.argv[5] or None,
    "optional_validation_enabled": sys.argv[6] == "1",
    "optiland_executed": sys.argv[7] == "true",
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
print(f"Wrote Optiland validation report: {report_path}")
PY
fi

if [[ "${OPTILAND_EXECUTED}" != "true" ]]; then
  echo "NO OPTILAND EXECUTION PERFORMED"
fi
echo "NO PRODUCTION-GRADE VALIDATION CLAIMED"
echo "NO FORMAL CONVERGENCE PROOF CLAIMED"
echo "NO PROPRIETARY SOLVER REQUIRED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
echo "NO UPLOAD PERFORMED"

if [[ "${OSA_RUN_OPTIONAL_OPTILAND_VALIDATION}" == "1" && "${PASSED}" != "true" ]]; then
  exit 3
fi
