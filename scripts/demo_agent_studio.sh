#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"
API_URL="${OSA_DEMO_API_URL:-http://127.0.0.1:8000/api/health}"
FRONTEND_URL="${OSA_DEMO_FRONTEND_URL:-http://127.0.0.1:5173}"
OSA_DEMO_RUN_SECONDS="${OSA_DEMO_RUN_SECONDS:-0}"
OSA_DEMO_HOLD="${OSA_DEMO_HOLD:-0}"
OSA_DEMO_SKIP_SMOKE="${OSA_DEMO_SKIP_SMOKE:-0}"
OSA_DEMO_WITH_VISUAL="${OSA_DEMO_WITH_VISUAL:-0}"
OSA_DEMO_SKIP_VISUAL="${OSA_DEMO_SKIP_VISUAL:-0}"

API_PID=""
FRONTEND_PID=""
INSTALLED_FRONTEND_DEPS="0"

cleanup() {
  if [[ -n "${FRONTEND_PID}" ]]; then
    kill "${FRONTEND_PID}" >/dev/null 2>&1 || true
    wait "${FRONTEND_PID}" >/dev/null 2>&1 || true
  fi
  if [[ -n "${API_PID}" ]]; then
    kill "${API_PID}" >/dev/null 2>&1 || true
    wait "${API_PID}" >/dev/null 2>&1 || true
  fi
  rm -rf "$FRONTEND_DIR/dist" "$FRONTEND_DIR/build" \
    "$FRONTEND_DIR/test-results" "$FRONTEND_DIR/playwright-report"
  if [[ "${INSTALLED_FRONTEND_DEPS}" == "1" ]]; then
    rm -rf "$FRONTEND_DIR/node_modules"
  fi
}
trap cleanup EXIT

url_ready_once() {
  local url="$1"
  python - "$url" <<'PY'
import sys
import urllib.request

try:
    with urllib.request.urlopen(sys.argv[1], timeout=2) as response:
        raise SystemExit(0 if response.status < 500 else 1)
except Exception:
    raise SystemExit(1)
PY
}

wait_for_url() {
  local url="$1"
  local label="$2"
  python - "$url" "$label" <<'PY'
import sys
import time
import urllib.request

url = sys.argv[1]
label = sys.argv[2]
deadline = time.time() + 60
while time.time() < deadline:
    try:
        with urllib.request.urlopen(url, timeout=2) as response:
            if response.status < 500:
                print(f"{label} ready: {url}")
                raise SystemExit(0)
    except Exception:
        time.sleep(1)
print(f"{label} did not become ready: {url}", file=sys.stderr)
raise SystemExit(1)
PY
}

echo "Agent Studio local demo package"
echo "Root: $ROOT_DIR"
echo "API: $API_URL"
echo "Frontend: $FRONTEND_URL"
echo "For first-run setup, use ./scripts/bootstrap_demo_env.sh and ./scripts/run_quickstart_demo.sh."

check_python_deps() {
  python - <<'PY'
try:
    import fastapi
    import optical_spec_agent
    import uvicorn
except Exception:
    raise SystemExit(1)
raise SystemExit(0 if optical_spec_agent.__version__ == "0.9.0rc8.dev0" else 1)
PY
}

if ! check_python_deps; then
  echo "Demo dependencies are not ready."
  echo "Run:"
  echo "./scripts/bootstrap_demo_env.sh"
  echo "source /tmp/osa-agent-studio-demo/bin/activate"
  echo "./scripts/run_quickstart_demo.sh"
  echo "NO SOLVER EXECUTION PERFORMED"
  echo "NO EXTERNAL LLM CALLED"
  echo "NO PROPRIETARY SOLVER REQUIRED"
  echo "NO UPLOAD PERFORMED"
  echo "NO TAG CREATED"
  echo "NO RELEASE CREATED"
  exit 0
fi

if ! command -v npm >/dev/null 2>&1; then
  echo "npm unavailable; the API can still be checked, but the frontend demo cannot start."
  "$ROOT_DIR/scripts/smoke_agent_api.sh"
  echo "NO SOLVER EXECUTION PERFORMED"
  echo "NO EXTERNAL LLM CALLED"
  echo "NO PROPRIETARY SOLVER REQUIRED"
  echo "NO UPLOAD PERFORMED"
  echo "NO TAG CREATED"
  echo "NO RELEASE CREATED"
  exit 0
fi

if [[ "${OSA_DEMO_SKIP_SMOKE}" != "1" ]]; then
  "$ROOT_DIR/scripts/smoke_agent_api.sh"
  "$ROOT_DIR/scripts/smoke_frontend_mvp.sh"
fi

if [[ "${OSA_DEMO_WITH_VISUAL}" == "1" && "${OSA_DEMO_SKIP_VISUAL}" != "1" ]]; then
  "$ROOT_DIR/scripts/smoke_frontend_visual.sh"
fi

if url_ready_once "$API_URL"; then
  echo "Using existing local Agent API."
else
  echo "Starting local Agent API."
  cd "$ROOT_DIR"
  python -m uvicorn optical_spec_agent.api.app:app --host 127.0.0.1 --port 8000 >/tmp/osa-agent-studio-demo-api.log 2>&1 &
  API_PID="$!"
  wait_for_url "$API_URL" "Agent API"
fi

if url_ready_once "$FRONTEND_URL"; then
  echo "Using existing Agent Studio frontend."
else
  echo "Starting Agent Studio frontend."
  cd "$FRONTEND_DIR"
  npm install --no-audit --no-fund
  INSTALLED_FRONTEND_DEPS="1"
  npm run dev -- --host 127.0.0.1 --port 5173 >/tmp/osa-agent-studio-demo-frontend.log 2>&1 &
  FRONTEND_PID="$!"
  wait_for_url "$FRONTEND_URL" "Agent Studio frontend"
fi

echo "Demo URLs:"
echo "- API: $API_URL"
echo "- Frontend: $FRONTEND_URL"
echo "- API OpenAPI docs: http://127.0.0.1:8000/docs"
echo "Walkthrough: docs/agent_studio_demo_runbook.md"

echo "NO SOLVER EXECUTION PERFORMED"
echo "NO EXTERNAL LLM CALLED"
echo "NO PROPRIETARY SOLVER REQUIRED"
echo "NO UPLOAD PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"

if [[ "${OSA_DEMO_HOLD}" == "1" ]]; then
  echo "Demo is running. Press Ctrl-C to stop."
  while true; do
    sleep 3600
  done
elif [[ "${OSA_DEMO_RUN_SECONDS}" =~ ^[0-9]+$ && "${OSA_DEMO_RUN_SECONDS}" -gt 0 ]]; then
  echo "Demo will stay up for ${OSA_DEMO_RUN_SECONDS} seconds."
  sleep "${OSA_DEMO_RUN_SECONDS}"
else
  echo "Readiness check complete. Set OSA_DEMO_HOLD=1 to keep the demo running."
fi
