#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"
OSA_DEMO_VENV="${OSA_DEMO_VENV:-/tmp/osa-agent-studio-demo}"

echo "Agent Studio quickstart bootstrap"
echo "Root: $ROOT_DIR"
echo "Demo venv: $OSA_DEMO_VENV"

if command -v python3.11 >/dev/null 2>&1; then
  PYTHON_BIN="python3.11"
elif command -v python >/dev/null 2>&1 && python - <<'PY'
import sys
raise SystemExit(0 if sys.version_info[:2] == (3, 11) else 1)
PY
then
  PYTHON_BIN="python"
else
  echo "Python 3.11 is required for the quickstart demo."
  exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm is required for the Agent Studio frontend quickstart."
  exit 1
fi

"$PYTHON_BIN" -m venv "$OSA_DEMO_VENV"
"$OSA_DEMO_VENV/bin/python" -m pip install --upgrade pip
"$OSA_DEMO_VENV/bin/python" -m pip install -e "$ROOT_DIR[test]"

"$OSA_DEMO_VENV/bin/python" - <<'PY'
import fastapi
import optical_spec_agent
import uvicorn

assert optical_spec_agent.__version__ == "0.9.0rc8.dev0"
print(f"optical-spec-agent {optical_spec_agent.__version__} ready")
print(f"fastapi {fastapi.__version__} ready")
print(f"uvicorn {uvicorn.__version__} ready")
PY

cd "$FRONTEND_DIR"
npm install --no-audit --no-fund

echo "Next steps:"
echo "source $OSA_DEMO_VENV/bin/activate"
echo "./scripts/run_quickstart_demo.sh"
echo "NO SOLVER EXECUTION PERFORMED"
echo "NO EXTERNAL LLM CALLED"
echo "NO UPLOAD PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
