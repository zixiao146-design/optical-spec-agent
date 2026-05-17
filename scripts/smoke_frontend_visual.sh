#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"
API_URL="${OSA_VISUAL_API_URL:-http://127.0.0.1:8000/api/health}"

API_PID=""

cleanup() {
  if [[ -n "${API_PID}" ]]; then
    kill "${API_PID}" >/dev/null 2>&1 || true
    wait "${API_PID}" >/dev/null 2>&1 || true
  fi
  rm -rf "$FRONTEND_DIR/test-results" "$FRONTEND_DIR/playwright-report" "$FRONTEND_DIR/dist" "$FRONTEND_DIR/build" "$FRONTEND_DIR/node_modules"
}
trap cleanup EXIT

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

echo "Agent Studio Playwright visual smoke"
echo "Root: $ROOT_DIR"

if ! command -v npm >/dev/null 2>&1; then
  echo "npm unavailable; skipping optional Playwright visual smoke."
  echo "NO SOLVER EXECUTION PERFORMED"
  echo "NO EXTERNAL LLM CALLED"
  echo "NO PROPRIETARY SOLVER REQUIRED"
  echo "NO UPLOAD PERFORMED"
  echo "NO TAG CREATED"
  echo "NO RELEASE CREATED"
  exit 0
fi

if url_ready_once "$API_URL"; then
  echo "Using existing local Agent API."
else
  echo "Starting local Agent API for visual smoke."
  cd "$ROOT_DIR"
  python -m uvicorn optical_spec_agent.api.app:app --host 127.0.0.1 --port 8000 >/tmp/osa-agent-api-visual.log 2>&1 &
  API_PID="$!"
  wait_for_url "$API_URL" "Agent API"
fi

cd "$FRONTEND_DIR"
npm install --no-audit --no-fund
echo "Attempting browser install: npx playwright install chromium"
if [[ -d "/Applications/Google Chrome.app" ]]; then
  echo "System Chrome detected; using configured local Chrome channel."
else
  python - <<'PY'
import subprocess

try:
    subprocess.run(["npx", "playwright", "install", "chromium"], timeout=120, check=True)
except subprocess.TimeoutExpired:
    print("Chromium browser install timed out; continuing with configured local Chrome channel.")
except subprocess.CalledProcessError:
    print("Chromium browser install failed; continuing with configured local Chrome channel.")
PY
fi

echo "Frontend dev server is started by Playwright webServer with npm run dev -- --host 127.0.0.1 --port 5173."
npm run visual:smoke

cleanup
trap - EXIT

echo "Frontend visual smoke summary:"
echo "- Playwright chromium visual smoke: passed"
echo "- generated Playwright reports removed"
echo "NO SOLVER EXECUTION PERFORMED"
echo "NO EXTERNAL LLM CALLED"
echo "NO PROPRIETARY SOLVER REQUIRED"
echo "NO UPLOAD PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
