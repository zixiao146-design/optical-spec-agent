#!/usr/bin/env bash
set -euo pipefail

OSA_SMOKE_VENV="${OSA_SMOKE_VENV:-/tmp/osa-smoke-release}"
OSA_SMOKE_PYTHON="${OSA_SMOKE_PYTHON:-python3}"

if ! "${OSA_SMOKE_PYTHON}" - <<'PY' >/dev/null 2>&1
import sys
raise SystemExit(0 if sys.version_info >= (3, 11) else 1)
PY
then
  if command -v python3.11 >/dev/null 2>&1; then
    echo "python3 is older than 3.11; using python3.11 for this project."
    OSA_SMOKE_PYTHON="python3.11"
  else
    echo "ERROR: ${OSA_SMOKE_PYTHON} is older than Python 3.11 and python3.11 was not found." >&2
    exit 1
  fi
fi

echo "Release smoke venv: ${OSA_SMOKE_VENV}"
echo "Python executable: ${OSA_SMOKE_PYTHON}"

rm -rf "${OSA_SMOKE_VENV}"
"${OSA_SMOKE_PYTHON}" -m venv "${OSA_SMOKE_VENV}"

# shellcheck source=/dev/null
source "${OSA_SMOKE_VENV}/bin/activate"

python -m pip install --upgrade pip build
python -m pip install -e ".[test]"

python -m pytest
echo "pytest passed"

python -m build
echo "build passed"

CLI_STATUS="CLI not applicable"
if python - <<'PY'
import tomllib
from pathlib import Path

with Path("pyproject.toml").open("rb") as handle:
    data = tomllib.load(handle)
scripts = data.get("project", {}).get("scripts", {})
raise SystemExit(0 if "optical-spec" in scripts else 1)
PY
then
  optical-spec --help >/dev/null
  CLI_STATUS="CLI help passed"
  echo "${CLI_STATUS}"
else
  echo "${CLI_STATUS}; no optical-spec console script declared."
fi

echo "dist artifacts:"
ls -lh dist/

cat <<EOF

Release smoke summary:
- install passed
- pytest passed
- build passed
- ${CLI_STATUS}
- dist artifacts listed
EOF
