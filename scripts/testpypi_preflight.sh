#!/usr/bin/env bash
set -euo pipefail

OSA_TESTPYPI_PREFLIGHT_VENV="${OSA_TESTPYPI_PREFLIGHT_VENV:-/tmp/osa-testpypi-preflight}"
OSA_TESTPYPI_WHEEL_VENV="${OSA_TESTPYPI_WHEEL_VENV:-/tmp/osa-testpypi-preflight-wheel}"
OSA_TESTPYPI_PREFLIGHT_PYTHON="${OSA_TESTPYPI_PREFLIGHT_PYTHON:-python3}"

if ! "${OSA_TESTPYPI_PREFLIGHT_PYTHON}" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info >= (3, 11) else 1)
PY
then
  if command -v python3.11 >/dev/null 2>&1; then
    echo "python3 is older than 3.11; using python3.11 for this project."
    OSA_TESTPYPI_PREFLIGHT_PYTHON="python3.11"
  else
    echo "ERROR: ${OSA_TESTPYPI_PREFLIGHT_PYTHON} is older than Python 3.11 and python3.11 was not found." >&2
    exit 1
  fi
fi

echo "TestPyPI preflight venv: ${OSA_TESTPYPI_PREFLIGHT_VENV}"
echo "Wheel install venv: ${OSA_TESTPYPI_WHEEL_VENV}"
echo "Python executable: ${OSA_TESTPYPI_PREFLIGHT_PYTHON}"
"${OSA_TESTPYPI_PREFLIGHT_PYTHON}" --version

PROJECT_VERSION="$("${OSA_TESTPYPI_PREFLIGHT_PYTHON}" - <<'PY'
import tomllib
from pathlib import Path

with Path("pyproject.toml").open("rb") as handle:
    data = tomllib.load(handle)
print(data["project"]["version"])
PY
)"
echo "Project version: ${PROJECT_VERSION}"

rm -rf "${OSA_TESTPYPI_PREFLIGHT_VENV}"
"${OSA_TESTPYPI_PREFLIGHT_PYTHON}" -m venv "${OSA_TESTPYPI_PREFLIGHT_VENV}"

# shellcheck source=/dev/null
source "${OSA_TESTPYPI_PREFLIGHT_VENV}/bin/activate"

echo "Preflight Python: $(python --version)"
python -m pip install --upgrade pip build twine

rm -rf dist build *.egg-info src/*.egg-info
python -m build
echo "build passed"

python -m twine check dist/*
echo "twine check passed"

python - "${PROJECT_VERSION}" <<'PY'
import sys
from pathlib import Path

version = sys.argv[1]
expected = [
    Path("dist") / f"optical_spec_agent-{version}-py3-none-any.whl",
    Path("dist") / f"optical_spec_agent-{version}.tar.gz",
]
missing = [str(path) for path in expected if not path.exists()]
if missing:
    raise SystemExit(f"ERROR: missing expected dist artifacts for {version}: {missing}")
print(f"dist filename check passed for {version}")
PY

echo "Wheel install smoke venv: ${OSA_TESTPYPI_WHEEL_VENV}"
rm -rf "${OSA_TESTPYPI_WHEEL_VENV}"
"${OSA_TESTPYPI_PREFLIGHT_PYTHON}" -m venv "${OSA_TESTPYPI_WHEEL_VENV}"
"${OSA_TESTPYPI_WHEEL_VENV}/bin/python" -m pip install --upgrade pip
"${OSA_TESTPYPI_WHEEL_VENV}/bin/python" -m pip install "dist/optical_spec_agent-${PROJECT_VERSION}-py3-none-any.whl"

"${OSA_TESTPYPI_WHEEL_VENV}/bin/python" - "${PROJECT_VERSION}" <<'PY'
import importlib.metadata
import sys

import optical_spec_agent

expected = sys.argv[1]
metadata_version = importlib.metadata.version("optical-spec-agent")
package_version = optical_spec_agent.__version__
print(f"Wheel-installed package version: {metadata_version}")
print(f"Wheel-installed __version__: {package_version}")
if metadata_version != expected:
    raise SystemExit(f"metadata version mismatch: {metadata_version} != {expected}")
if package_version != expected:
    raise SystemExit(f"package __version__ mismatch: {package_version} != {expected}")
PY

"${OSA_TESTPYPI_WHEEL_VENV}/bin/optical-spec" --help >/dev/null
echo "optical-spec --help passed"

echo
echo "TestPyPI preflight summary:"
echo "- build passed"
echo "- twine check passed"
echo "- wheel install passed"
echo "- optical-spec --help passed"
echo "- NO UPLOAD PERFORMED"
echo "NO UPLOAD PERFORMED"
