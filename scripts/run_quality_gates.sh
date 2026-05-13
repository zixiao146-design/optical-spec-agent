#!/usr/bin/env bash
set -euo pipefail

OSA_QUALITY_PREFIX="${OSA_QUALITY_PREFIX:-/tmp/osa-quality}"
OSA_SKIP_PREFLIGHT="${OSA_SKIP_PREFLIGHT:-0}"
OSA_SKIP_SOLVER_PREFLIGHT="${OSA_SKIP_SOLVER_PREFLIGHT:-0}"
OSA_SKIP_SMOKE="${OSA_SKIP_SMOKE:-0}"
OSA_SKIP_PYTEST="${OSA_SKIP_PYTEST:-0}"
OSA_SKIP_BUILD="${OSA_SKIP_BUILD:-0}"
OSA_SKIP_MAKE_CHECK="${OSA_SKIP_MAKE_CHECK:-0}"

PREFLIGHT_STATUS="skipped"
SOLVER_PREFLIGHT_STATUS="skipped"
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
  run_step "pytest" python -m pytest
  PYTEST_STATUS="passed"
fi

if [[ "${OSA_SKIP_BUILD}" != "1" ]]; then
  run_step "build" python -m build
  BUILD_STATUS="passed"
fi

if [[ "${OSA_SKIP_MAKE_CHECK}" != "1" ]]; then
  run_step "make check" make check
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
echo "- smoke: ${SMOKE_STATUS}"
echo "- wheel smoke: ${WHEEL_SMOKE_STATUS}"
echo "- pytest: ${PYTEST_STATUS}"
echo "- build: ${BUILD_STATUS}"
echo "- make check: ${MAKE_CHECK_STATUS}"
echo "- CLI examples: ${CLI_STATUS}"
echo "- NO UPLOAD PERFORMED"
echo "- NO SOLVER EXECUTION PERFORMED"
echo "- NO TAG CREATED"
echo "- NO RELEASE CREATED"
echo "NO UPLOAD PERFORMED"
echo "NO SOLVER EXECUTION PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
