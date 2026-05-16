#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FRONTEND_DIR="$ROOT_DIR/frontend"

echo "Agent Studio frontend MVP smoke"
echo "Root: $ROOT_DIR"

if ! command -v npm >/dev/null 2>&1; then
  echo "npm unavailable; skipping frontend build smoke."
  echo "NO SOLVER EXECUTION PERFORMED"
  echo "NO EXTERNAL LLM CALLED"
  echo "NO PROPRIETARY SOLVER REQUIRED"
  echo "NO UPLOAD PERFORMED"
  echo "NO TAG CREATED"
  echo "NO RELEASE CREATED"
  exit 0
fi

cd "$FRONTEND_DIR"
cleanup() {
  rm -rf node_modules dist build
}
trap cleanup EXIT

npm install --ignore-scripts --no-audit --no-fund
npm run typecheck
npm run build

cleanup

echo "Frontend MVP smoke summary:"
echo "- npm install: passed"
echo "- npm run typecheck: passed"
echo "- npm run build: passed"
echo "- generated frontend artifacts removed"
echo "NO SOLVER EXECUTION PERFORMED"
echo "NO EXTERNAL LLM CALLED"
echo "NO PROPRIETARY SOLVER REQUIRED"
echo "NO UPLOAD PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
