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
    "requirements_templates",
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
internal_tools = {item["tool_name"]: item for item in report["internal_tools"]}
require(internal_tools["source_monitor_inference"]["executed_in_sample"] is True, "source/monitor inference not executed in sample")
require(internal_tools["missing_input_diagnostics"]["executed_in_sample"] is True, "missing-input diagnostics not executed in sample")
require(all(action["executed"] is False for action in report["blocked_external_actions"]), "external action executed")
require(report["production_grade_validation_claimed"] is False, "production claim changed")
require(report["formal_convergence_proof_claimed"] is False, "convergence claim changed")
require(len(report["requirements_templates"]) == 7, "requirement template count mismatch")
require(
    all(item["matched_by_heuristic"] for item in report["requirements_templates"]),
    "requirement template matching failed",
)

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
require(cross_payload["summary"]["requirement_templates_fail"] == 0, "requirement template cross-check failed")
require(cross_payload["external_llm_required"] is False, "cross-check LLM flag changed")

requirements = client.get("/api/design-requirements")
require(requirements.status_code == 200, "/api/design-requirements failed")
require(requirements.json()["template_count"] == 7, "design requirements count mismatch")

thin_detail = client.get("/api/design-requirements/thin_film_ar_coating")
require(thin_detail.status_code == 200, "thin-film requirement detail failed")
require(thin_detail.json()["template"]["template_id"] == "thin_film_ar_coating", "wrong requirement detail")

match = client.post(
    "/api/design-requirements/match",
    json={
        "goal": "Design a local preview for a single-layer anti-reflection coating on glass at 550 nm.",
        "language": "en",
    },
)
require(match.status_code == 200, "design requirement match failed")
require(match.json()["matched_template_id"] == "thin_film_ar_coating", "thin-film match failed")

zh_session = client.post(
    "/api/agent-session",
    json={
        "goal": "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流，默认不运行外部求解器。",
        "language": "zh-CN",
    },
)
require(zh_session.status_code == 200, "Chinese nanoparticle agent session failed")
zh_payload = zh_session.json()
require(zh_payload["requirement_template_id"] == "nanoparticle_plasmonics", "Chinese nanoparticle template mismatch")

thin_session = client.post(
    "/api/agent-session",
    json={
        "goal": "Design an anti-reflection coating for glass at 550 nm and run only local preview calculators.",
        "language": "en",
    },
)
require(thin_session.status_code == 200, "thin-film agent session failed")
thin_payload = thin_session.json()
ledger = {entry["tool_name"]: entry for entry in thin_payload["tool_call_ledger"]}
require(thin_payload["requirement_template_id"] == "thin_film_ar_coating", "thin-film session template mismatch")
require(ledger["requirements.match_template"]["executed"] is True, "requirements match not executed")
require(ledger["requirements.extract_optical_intent"]["executed"] is True, "intent extraction not executed")
require(ledger["optical_language.infer_source_monitor"]["executed"] is True, "source/monitor inference not executed")
require(ledger["optical_language.diagnose_missing_inputs"]["executed"] is True, "missing-input diagnostics not executed")
require(ledger["optics.thin_film.spectrum"]["executed"] is True, "thin-film calculator not executed")

infer = client.post(
    "/api/optical-language/infer",
    json={
        "goal": "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。",
        "template_id": "nanoparticle_plasmonics",
        "language": "zh-CN",
    },
)
require(infer.status_code == 200, "optical-language inference failed")
require(infer.json()["source_model"]["source_type"] == "plane_wave", "source inference mismatch")
require(infer.json()["monitor_model"]["monitor_type"] == "scattering_spectrum", "monitor inference mismatch")

diagnose = client.post(
    "/api/optical-language/diagnose",
    json={
        "goal": "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。",
        "template_id": "nanoparticle_plasmonics",
        "language": "zh-CN",
    },
)
require(diagnose.status_code == 200, "optical-language diagnostics failed")
require(diagnose.json()["safe_to_run_solver"] is False, "diagnostics changed solver safety")

print("BACKEND CAPABILITY REPORT PASSED")
print("DESIGN CASE CROSS-CHECKS PASSED")
print("DESIGN REQUIREMENT MATCHING PASSED")
print("SOURCE/MONITOR INFERENCE PASSED")
print("MISSING INPUT DIAGNOSTICS PASSED")
PY

echo "NO SOLVER EXECUTION PERFORMED"
echo "NO EXTERNAL LLM CALLED"
echo "NO UPLOAD PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
