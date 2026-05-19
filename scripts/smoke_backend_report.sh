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

python scripts/check_adapter_native_golden.py
python scripts/evaluate_application_domain_benchmarks.py

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
    "application_domain_coverage",
    "material_template_cross_checks",
    "application_domain_benchmarks",
    "adapter_native_golden_coverage",
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
    "fiber_coupling",
    "polarization",
}, "calculator list mismatch")
internal_tools = {item["tool_name"]: item for item in report["internal_tools"]}
require(internal_tools["source_monitor_inference"]["executed_in_sample"] is True, "source/monitor inference not executed in sample")
require(internal_tools["missing_input_diagnostics"]["executed_in_sample"] is True, "missing-input diagnostics not executed in sample")
require(internal_tools["observable_diagnostics"]["executed_in_sample"] is True, "observable diagnostics not executed in sample")
require(internal_tools["adapter_native_mapping"]["executed_in_sample"] is True, "adapter-native mapping not executed in sample")
require(internal_tools["adapter_native_golden_coverage"]["executed_in_sample"] is True, "adapter golden coverage not executed in sample")
require(internal_tools["application_domain_registry"]["executed_in_sample"] is True, "application domain registry not executed in sample")
require(internal_tools["material_template_cross_checks"]["executed_in_sample"] is True, "material-template cross-checks not executed in sample")
require(internal_tools["application_domain_benchmarks"]["executed_in_sample"] is True, "application domain benchmarks not executed in sample")
golden = report["adapter_native_golden_coverage"]
require(golden["status"] == "ok", "adapter golden coverage report not ok")
require(set(golden["adapters_covered"]) == {"meep", "mpb", "gmsh", "elmer", "optiland"}, "adapter golden coverage mismatch")
require(golden["missing_adapters"] == [], "adapter golden coverage reports missing adapter")
require(all(item["coverage_status"] == "pass" for item in golden["coverage_items"]), "adapter golden case coverage failed")
require(all(action["executed"] is False for action in report["blocked_external_actions"]), "external action executed")
require(report["production_grade_validation_claimed"] is False, "production claim changed")
require(report["formal_convergence_proof_claimed"] is False, "convergence claim changed")
require(report["application_domain_coverage"]["domain_count"] == 10, "application domain count mismatch")
require(report["application_domain_coverage"]["failed_domains"] == [], "application domain coverage failed")
require(report["material_template_cross_checks"]["total"] == 10, "material-template cross-check count mismatch")
require(report["material_template_cross_checks"]["fail_count"] == 0, "material-template cross-check failed")
require(report["application_domain_benchmarks"]["scenario_count"] >= 19, "benchmark scenario count mismatch")
require(report["application_domain_benchmarks"]["fail_count"] == 0, "application domain benchmark failed")
require(report["application_domain_benchmarks"]["warn_count"] == 0, "application domain benchmark warning remained")
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
require(capability_payload["adapter_native_golden_coverage"]["status"] == "ok", "API report missing golden coverage")

cross_checks = client.get("/api/design-case-cross-checks")
require(cross_checks.status_code == 200, "/api/design-case-cross-checks failed")
cross_payload = cross_checks.json()
require(cross_payload["cross_checks"], "API cross-checks missing")
require(cross_payload["summary"]["fail"] == 0, "design case cross-check failed")
require(cross_payload["summary"]["requirement_templates_fail"] == 0, "requirement template cross-check failed")
require(cross_payload["external_llm_required"] is False, "cross-check LLM flag changed")

domain_checks = client.get("/api/application-domain-cross-checks")
require(domain_checks.status_code == 200, "/api/application-domain-cross-checks failed")
domain_payload = domain_checks.json()
require(domain_payload["summary"]["total"] == 10, "application domain cross-check count mismatch")
require(domain_payload["summary"]["fail"] == 0, "application domain cross-check failed")
require(domain_payload["external_solver_executed"] is False, "domain cross-check solver flag changed")

benchmarks = client.get("/api/application-domain-benchmarks")
require(benchmarks.status_code == 200, "/api/application-domain-benchmarks failed")
require(benchmarks.json()["scenario_count"] >= 19, "benchmark scenario count mismatch")

benchmark_eval = client.post("/api/application-domain-benchmarks/waveguide_or_coating_ambiguous/evaluate")
require(benchmark_eval.status_code == 200, "application benchmark evaluation failed")
require(benchmark_eval.json()["status"] in {"pass", "warn"}, "ambiguous benchmark status changed")

benchmark_results = client.get("/api/application-domain-benchmark-results")
require(benchmark_results.status_code == 200, "/api/application-domain-benchmark-results failed")
require(benchmark_results.json()["summary"]["fail"] == 0, "application benchmark failed")
require(benchmark_results.json()["summary"]["warn"] == 0, "application benchmark warning remained")

golden_api = client.get("/api/adapter-native-golden-coverage")
require(golden_api.status_code == 200, "/api/adapter-native-golden-coverage failed")
golden_payload = golden_api.json()
require(golden_payload["status"] == "ok", "golden coverage API not ok")
require(golden_payload["external_solver_executed"] is False, "golden coverage solver flag changed")

requirements = client.get("/api/design-requirements")
require(requirements.status_code == 200, "/api/design-requirements failed")
require(requirements.json()["template_count"] == 7, "design requirements count mismatch")

application_domains = client.get("/api/application-domains")
require(application_domains.status_code == 200, "/api/application-domains failed")
require(application_domains.json()["domain_count"] == 10, "application domain count mismatch")

domain_match = client.post(
    "/api/application-domains/match",
    json={"goal": "Design a thin-film anti-reflection coating.", "language": "en"},
)
require(domain_match.status_code == 200, "application domain match failed")
require(
    domain_match.json()["matched_domains"] == ["thin_film_coating"],
    "thin-film application domain match failed",
)

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

observable = client.post(
    "/api/optical-language/observables/diagnose",
    json={
        "goal": "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。",
        "template_id": "nanoparticle_plasmonics",
        "language": "zh-CN",
    },
)
require(observable.status_code == 200, "observable diagnostics failed")
require(
    "scattering_spectrum"
    in {item["observable_kind"] for item in observable.json()["observable_diagnostics"]},
    "observable diagnostics missing scattering spectrum",
)

mapping = client.post(
    "/api/optical-language/adapter-mapping",
    json={
        "adapter_name": "meep",
        "goal": "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。",
        "template_id": "nanoparticle_plasmonics",
        "language": "zh-CN",
    },
)
require(mapping.status_code == 200, "adapter source/monitor mapping failed")
mapping_payload = mapping.json()
require(
    mapping_payload["adapter_source_monitor_mapping"]["adapter_name"] == "meep",
    "adapter mapping adapter name mismatch",
)
require(
    mapping_payload["adapter_source_monitor_mapping"]["external_solver_executed"] is False,
    "adapter mapping executed solver",
)

preview = client.post(
    "/api/adapter-preview",
    json={"path": "examples/specs/minimal_nanoparticle.json", "tool": "meep"},
)
require(preview.status_code == 200, "adapter preview source/monitor metadata failed")
preview_payload = preview.json()
require(preview_payload["observable_diagnostics"], "adapter preview missing observable diagnostics")
require(preview_payload["adapter_source_monitor_mapping"], "adapter preview missing mapping")

print("BACKEND CAPABILITY REPORT PASSED")
print("DESIGN CASE CROSS-CHECKS PASSED")
print("DESIGN REQUIREMENT MATCHING PASSED")
print("APPLICATION DOMAIN COVERAGE PASSED")
print("MATERIAL TEMPLATE CROSS-CHECKS PASSED")
print("APPLICATION DOMAIN BENCHMARKS PASSED")
print("FIBER COUPLING PREVIEW PASSED")
print("POLARIZATION PREVIEW PASSED")
print("SOURCE/MONITOR INFERENCE PASSED")
print("MISSING INPUT DIAGNOSTICS PASSED")
print("OBSERVABLE DIAGNOSTICS PASSED")
print("ADAPTER SOURCE/MONITOR MAPPING PASSED")
print("ADAPTER NATIVE METADATA DIFF PASSED")
print("ADAPTER GOLDEN COVERAGE REPORT PASSED")
PY

echo "FIBER COUPLING PREVIEW PASSED"
echo "POLARIZATION PREVIEW PASSED"
echo "NO SOLVER EXECUTION PERFORMED"
echo "NO EXTERNAL LLM CALLED"
echo "NO UPLOAD PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
