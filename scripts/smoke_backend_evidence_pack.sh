#!/usr/bin/env bash
set -euo pipefail

# Backend evidence pack smoke is local-only:
# - no solver execution
# - no external LLM calls
# - no upload, tag, or release actions

JSON_OUT="/tmp/osa-backend-evidence-pack.json"
MARKDOWN_OUT="/tmp/osa-backend-evidence-pack.md"

python scripts/generate_backend_evidence_pack.py \
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


json_path = Path("/tmp/osa-backend-evidence-pack.json")
markdown_path = Path("/tmp/osa-backend-evidence-pack.md")
require(json_path.exists(), "evidence pack JSON was not generated")
require(markdown_path.exists(), "evidence pack Markdown was not generated")

payload = json.loads(json_path.read_text(encoding="utf-8"))
for section in [
    "package_and_release_status",
    "sub_agent_reality",
    "tool_call_reality",
    "optical_calculators",
    "design_case_cross_checks",
    "source_monitor_observable_diagnostics",
    "adapter_native_golden_coverage",
    "blocked_or_deferred_capabilities",
    "maintainer_review_questions",
]:
    require(section in payload, f"missing evidence pack section: {section}")

require(len(payload["sub_agent_reality"]) == 8, "sub-agent reality count mismatch")
require(
    all(item["executed_in_sample_session"] for item in payload["sub_agent_reality"]),
    "not all sub-agents executed in sample session",
)
require(
    {item["calculator_name"] for item in payload["optical_calculators"]}
    == {"thin_film", "paraxial", "gaussian_beam", "waveguide"},
    "calculator evidence mismatch",
)
golden = payload["adapter_native_golden_coverage"]
require(golden["status"] == "ok", "adapter golden evidence not ok")
require(len(golden["cases"]) == 5, "adapter golden case count mismatch")
require(all(case["metadata_match"] for case in golden["cases"]), "metadata diff failed")
require(all(case["fragment_match"] for case in golden["cases"]), "fragment diff failed")
require(all(case["safety_match"] for case in golden["cases"]), "safety diff failed")
require(all(case["solver_executed"] is False for case in golden["cases"]), "solver executed")
require(
    all(item["executed"] is False for item in payload["blocked_or_deferred_capabilities"]),
    "blocked/deferred capability executed",
)
require(payload["external_solver_executed"] is False, "solver flag changed")
require(payload["external_llm_required"] is False, "LLM flag changed")
require(payload["production_grade_validation_claimed"] is False, "production claim changed")
require(payload["formal_convergence_proof_claimed"] is False, "convergence claim changed")

markdown = markdown_path.read_text(encoding="utf-8")
for heading in [
    "Sub-agent reality",
    "Tool-call reality",
    "Optical calculators",
    "Design-case cross-checks",
    "Adapter-native golden coverage",
    "Blocked or deferred capabilities",
]:
    require(heading in markdown, f"missing Markdown heading: {heading}")
require("production-grade physical validation" in markdown, "missing limitation copy")
require("NO SOLVER EXECUTION PERFORMED" in markdown, "missing solver safety marker")

client = TestClient(app)
response = client.get("/api/backend-evidence-summary")
require(response.status_code == 200, "/api/backend-evidence-summary failed")
api_payload = response.json()
require(api_payload["evidence_pack_available"] is True, "API evidence flag missing")
require(api_payload["external_solver_executed"] is False, "API solver flag changed")
require(api_payload["adapter_native_golden_coverage"]["status"] == "ok", "API golden status changed")

print("BACKEND EVIDENCE PACK PASSED")
PY

echo "NO SOLVER EXECUTION PERFORMED"
echo "NO EXTERNAL LLM CALLED"
echo "NO UPLOAD PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
