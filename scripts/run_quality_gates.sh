#!/usr/bin/env bash
set -euo pipefail

OSA_QUALITY_PREFIX="${OSA_QUALITY_PREFIX:-/tmp/osa-quality}"
OSA_SKIP_PREFLIGHT="${OSA_SKIP_PREFLIGHT:-0}"
OSA_SKIP_SOLVER_PREFLIGHT="${OSA_SKIP_SOLVER_PREFLIGHT:-0}"
OSA_SKIP_GMSH_PREFLIGHT="${OSA_SKIP_GMSH_PREFLIGHT:-0}"
OSA_SKIP_MEEP_PREFLIGHT="${OSA_SKIP_MEEP_PREFLIGHT:-0}"
OSA_SKIP_MPB_PREFLIGHT="${OSA_SKIP_MPB_PREFLIGHT:-0}"
OSA_SKIP_OPTILAND_PREFLIGHT="${OSA_SKIP_OPTILAND_PREFLIGHT:-0}"
OSA_SKIP_ELMER_PREFLIGHT="${OSA_SKIP_ELMER_PREFLIGHT:-0}"
OSA_SKIP_SMOKE="${OSA_SKIP_SMOKE:-0}"
OSA_SKIP_PYTEST="${OSA_SKIP_PYTEST:-0}"
OSA_SKIP_BUILD="${OSA_SKIP_BUILD:-0}"
OSA_SKIP_MAKE_CHECK="${OSA_SKIP_MAKE_CHECK:-0}"
OSA_QUALITY_TEST_VENV="${OSA_QUALITY_TEST_VENV:-${OSA_QUALITY_PREFIX}-test}"
QUALITY_PYTHON="${OSA_QUALITY_PYTHON:-}"

PREFLIGHT_STATUS="skipped"
SOLVER_PREFLIGHT_STATUS="skipped"
GMSH_PREFLIGHT_STATUS="skipped"
MEEP_PREFLIGHT_STATUS="skipped"
MPB_PREFLIGHT_STATUS="skipped"
OPTILAND_PREFLIGHT_STATUS="skipped"
ELMER_PREFLIGHT_STATUS="skipped"
SMOKE_STATUS="skipped"
WHEEL_SMOKE_STATUS="skipped"
PYTEST_STATUS="skipped"
BUILD_STATUS="skipped"
MAKE_CHECK_STATUS="skipped"
CLI_STATUS="pending"

run_step() {
  local title="$1"
  shift
  echo
  echo "==> ${title}"
  "$@"
}

prepare_quality_python() {
  if [[ -n "${QUALITY_PYTHON}" ]]; then
    echo "Quality Python: ${QUALITY_PYTHON}"
    return
  fi

  if python - <<'PY' >/dev/null 2>&1
import build  # noqa: F401
import pytest  # noqa: F401
PY
  then
    QUALITY_PYTHON="$(command -v python)"
  else
    echo "Current Python is missing build/pytest; creating quality venv: ${OSA_QUALITY_TEST_VENV}"
    rm -rf "${OSA_QUALITY_TEST_VENV}"
    python -m venv "${OSA_QUALITY_TEST_VENV}"
    "${OSA_QUALITY_TEST_VENV}/bin/python" -m pip install --upgrade pip
    "${OSA_QUALITY_TEST_VENV}/bin/python" -m pip install -e ".[test]" build
    QUALITY_PYTHON="${OSA_QUALITY_TEST_VENV}/bin/python"
  fi

  echo "Quality Python: ${QUALITY_PYTHON}"
}

PROJECT_VERSION="$(python - <<'PY'
import tomllib
from pathlib import Path

with Path("pyproject.toml").open("rb") as handle:
    data = tomllib.load(handle)
print(data["project"]["version"])
PY
)"

echo "Quality gates for optical-spec-agent ${PROJECT_VERSION}"
echo "Quality prefix: ${OSA_QUALITY_PREFIX}"
echo "Default path: no upload, no tag creation, no release creation."

if [[ "${OSA_SKIP_PREFLIGHT}" != "1" ]]; then
  run_step "TestPyPI no-upload preflight" env \
    OSA_TESTPYPI_PREFLIGHT_VENV="${OSA_QUALITY_PREFIX}-testpypi-preflight" \
    OSA_TESTPYPI_WHEEL_VENV="${OSA_QUALITY_PREFIX}-testpypi-wheel" \
    ./scripts/testpypi_preflight.sh
  PREFLIGHT_STATUS="passed"
fi

if [[ "${OSA_SKIP_SOLVER_PREFLIGHT}" != "1" ]]; then
  run_step "Open-source solver validation preflight" env \
    OSA_SOLVER_PREFLIGHT_JSON="${OSA_QUALITY_PREFIX}-open-solver-preflight.json" \
    ./scripts/open_solver_validation_preflight.sh
  SOLVER_PREFLIGHT_STATUS="passed"
fi

if [[ "${OSA_SKIP_GMSH_PREFLIGHT}" != "1" ]]; then
  run_step "Gmsh optional validation pilot default preflight" env \
    OSA_GMSH_VALIDATION_REPORT="${OSA_QUALITY_PREFIX}-gmsh-validation-default.json" \
    ./scripts/run_optional_gmsh_validation.sh
  GMSH_PREFLIGHT_STATUS="passed"
fi

if [[ "${OSA_SKIP_MEEP_PREFLIGHT}" != "1" ]]; then
  run_step "Meep optional validation pilot default preflight" env \
    OSA_MEEP_VALIDATION_REPORT="${OSA_QUALITY_PREFIX}-meep-validation-default.json" \
    ./scripts/run_optional_meep_validation.sh
  MEEP_PREFLIGHT_STATUS="passed"
fi

if [[ "${OSA_SKIP_MPB_PREFLIGHT}" != "1" ]]; then
  run_step "MPB optional validation pilot default preflight" env \
    OSA_MPB_VALIDATION_REPORT="${OSA_QUALITY_PREFIX}-mpb-validation-default.json" \
    ./scripts/run_optional_mpb_validation.sh
  MPB_PREFLIGHT_STATUS="passed"
fi

if [[ "${OSA_SKIP_OPTILAND_PREFLIGHT}" != "1" ]]; then
  run_step "Optiland optional validation pilot default preflight" env \
    OSA_OPTILAND_VALIDATION_REPORT="${OSA_QUALITY_PREFIX}-optiland-validation-default.json" \
    ./scripts/run_optional_optiland_validation.sh
  OPTILAND_PREFLIGHT_STATUS="passed"
fi

if [[ "${OSA_SKIP_ELMER_PREFLIGHT}" != "1" ]]; then
  run_step "Elmer optional validation pilot default preflight" env \
    OSA_ELMER_VALIDATION_REPORT="${OSA_QUALITY_PREFIX}-elmer-validation-default.json" \
    ./scripts/run_optional_elmer_validation.sh
  ELMER_PREFLIGHT_STATUS="passed"
fi

if [[ "${OSA_SKIP_SMOKE}" != "1" ]]; then
  run_step "Release smoke" env \
    OSA_SMOKE_VENV="${OSA_QUALITY_PREFIX}-smoke" \
    ./scripts/smoke_release.sh
  SMOKE_STATUS="passed"

  run_step "Wheel release smoke" env \
    OSA_SMOKE_VENV="${OSA_QUALITY_PREFIX}-smoke-main" \
    OSA_SMOKE_VERIFY_WHEEL=1 \
    OSA_SMOKE_WHEEL_VENV="${OSA_QUALITY_PREFIX}-smoke-wheel" \
    ./scripts/smoke_release.sh
  WHEEL_SMOKE_STATUS="passed"
fi

if [[ "${OSA_SKIP_PYTEST}" != "1" ]]; then
  prepare_quality_python
  run_step "pytest" "${QUALITY_PYTHON}" -m pytest
  PYTEST_STATUS="passed"
fi

if [[ "${OSA_SKIP_BUILD}" != "1" ]]; then
  prepare_quality_python
  run_step "build" "${QUALITY_PYTHON}" -m build
  BUILD_STATUS="passed"
fi

if [[ "${OSA_SKIP_MAKE_CHECK}" != "1" ]]; then
  prepare_quality_python
  run_step "make check" env \
    PATH="$(dirname "${QUALITY_PYTHON}"):${PATH}" \
    PYTHON="${QUALITY_PYTHON}" \
    make check
  MAKE_CHECK_STATUS="passed"
fi

run_step "CLI examples" optical-spec --help
run_step "Adapter list JSON" optical-spec adapter-list --json
run_step "Validate offline spec" optical-spec validate examples/specs/minimal_nanoparticle.json
run_step "Parse offline spec" optical-spec parse examples/specs/minimal_nanoparticle.json --json
run_step "Workflow preview" optical-spec workflow-plan examples/workflows/local_preview_request.json --json
run_step "E2E workflow preview" optical-spec workflow-plan examples/e2e/local_optical_workflow.json --json
CLI_STATUS="passed"

echo
echo "Quality gate summary:"
echo "- TestPyPI no-upload preflight: ${PREFLIGHT_STATUS}"
echo "- open-source solver preflight: ${SOLVER_PREFLIGHT_STATUS}"
echo "- Gmsh optional validation default preflight: ${GMSH_PREFLIGHT_STATUS}"
echo "- Meep optional validation default preflight: ${MEEP_PREFLIGHT_STATUS}"
echo "- MPB optional validation default preflight: ${MPB_PREFLIGHT_STATUS}"
echo "- Optiland optional validation default preflight: ${OPTILAND_PREFLIGHT_STATUS}"
echo "- Elmer optional validation default preflight: ${ELMER_PREFLIGHT_STATUS}"
echo "- smoke: ${SMOKE_STATUS}"
echo "- wheel smoke: ${WHEEL_SMOKE_STATUS}"
echo "- pytest: ${PYTEST_STATUS}"
echo "- build: ${BUILD_STATUS}"
echo "- make check: ${MAKE_CHECK_STATUS}"
echo "- CLI examples: ${CLI_STATUS}"
echo "- NO UPLOAD PERFORMED"
echo "- NO GMSH EXECUTION PERFORMED"
echo "- NO MEEP EXECUTION PERFORMED"
echo "- NO MPB EXECUTION PERFORMED"
echo "- NO OPTILAND EXECUTION PERFORMED"
echo "- NO ELMER EXECUTION PERFORMED"
echo "- NO SOLVER EXECUTION PERFORMED"
echo "- NO TAG CREATED"
echo "- NO RELEASE CREATED"
echo "NO UPLOAD PERFORMED"
echo "NO GMSH EXECUTION PERFORMED"
echo "NO MEEP EXECUTION PERFORMED"
echo "NO MPB EXECUTION PERFORMED"
echo "NO OPTILAND EXECUTION PERFORMED"
echo "NO ELMER EXECUTION PERFORMED"
echo "NO SOLVER EXECUTION PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
