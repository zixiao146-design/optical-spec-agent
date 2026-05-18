#!/usr/bin/env bash
set -euo pipefail

# Backend report smoke is local-only:
# - no solver execution
# - no external LLM calls
# - no upload, tag, or release actions

JSON_OUT="/tmp/osa-backend-capability-report.json"
MARKDOWN_OUT="/tmp/osa-backend-capability-report.md"

python scripts/generate_backend_capability_report.py \
  --json-out "$JSON_OUT" \
  --markdown-out "$MARKDOWN_OUT"

python - <<'PY'
import json
from pathlib import Path

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


report = json.loads(Path("/tmp/osa-backend-capability-report.json").read_text(encoding="utf-8"))
for section in [
    "package",
    "sub_agents",
    "internal_tools",
    "optical_calculators",
    "design_case_cross_checks",
    "blocked_external_actions",
]:
    require(section in report, f"missing report section: {section}")

require(all(agent["executed_in_sample_session"] for agent in report["sub_agents"]), "not all sub-agents executed")
require({item["calculator_name"] for item in report["optical_calculators"]} == {
    "thin_film",
    "paraxial",
    "gaussian_beam",
    "waveguide",
}, "calculator list mismatch")
require(all(action["executed"] is False for action in report["blocked_external_actions"]), "external action executed")
require(report["production_grade_validation_claimed"] is False, "production claim changed")
require(report["formal_convergence_proof_claimed"] is False, "convergence claim changed")

client = TestClient(app)
capability = client.get("/api/backend-capability-report")
require(capability.status_code == 200, "/api/backend-capability-report failed")
capability_payload = capability.json()
require(capability_payload["sub_agents"], "API report missing sub-agents")
require(capability_payload["external_solver_executed"] is False, "API report solver flag changed")

cross_checks = client.get("/api/design-case-cross-checks")
require(cross_checks.status_code == 200, "/api/design-case-cross-checks failed")
cross_payload = cross_checks.json()
require(cross_payload["cross_checks"], "API cross-checks missing")
require(cross_payload["summary"]["fail"] == 0, "design case cross-check failed")
require(cross_payload["external_llm_required"] is False, "cross-check LLM flag changed")

print("BACKEND CAPABILITY REPORT PASSED")
print("DESIGN CASE CROSS-CHECKS PASSED")
PY

echo "NO SOLVER EXECUTION PERFORMED"
echo "NO EXTERNAL LLM CALLED"
echo "NO UPLOAD PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
