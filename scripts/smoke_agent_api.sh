#!/usr/bin/env bash
set -euo pipefail

python - <<'PY'
import json
import sys
from pathlib import Path

ROOT = Path.cwd()
sys.path.insert(0, str(ROOT / "src"))

from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


client = TestClient(app)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def post(path, payload):
    response = client.post(path, json=payload)
    require(response.status_code == 200, f"{path} returned {response.status_code}: {response.text}")
    return response.json()


def get(path):
    response = client.get(path)
    require(response.status_code == 200, f"{path} returned {response.status_code}: {response.text}")
    return response.json()


health = get("/api/health")
require(health["status"] == "ok", "health status must be ok")

version = get("/api/version")
require(version["package_version"] == "0.9.0rc7.dev0", "unexpected package version")
require(version["api_contract_version"] == "0.1", "unexpected API contract version")

adapters = get("/api/adapters")
adapter_names = {item["tool_name"] for item in adapters["adapters"]}
require({"meep", "gmsh", "mpb", "elmer", "optiland"}.issubset(adapter_names), "missing adapters")

schema = get("/api/schema")
require(schema["schema_name"] == "OpticalSpec", "schema endpoint should expose OpticalSpec")

parse_payload = post(
    "/api/parse",
    {"text": "Use Meep FDTD to simulate a nanoparticle spectrum.", "parser": "heuristic", "json": True},
)
require(parse_payload["external_llm_required"] is False, "parse must not require external LLM")

validate_payload = post("/api/validate", {"path": "examples/specs/minimal_nanoparticle.json"})
require(validate_payload["valid"] is True, "minimal spec should validate")

workflow_payload = post("/api/workflow-plan", {"path": "examples/workflows/local_preview_request.json"})
require(workflow_payload["external_solver_executed"] is False, "workflow plan must not run solver")

preview_payload = post(
    "/api/adapter-preview",
    {"path": "examples/specs/minimal_nanoparticle.json", "tool": "gmsh"},
)
require(preview_payload["external_solver_executed"] is False, "adapter preview must not run solver")

evidence = get("/api/validation-evidence")
require(evidence["production_grade_validation_claimed"] is False, "evidence must not claim production-grade validation")

readiness = get("/api/readiness")
require(readiness["pypi"]["published"] is False, "PyPI must remain unpublished")

materials = get("/api/materials")
material_ids = {item["material_id"] for item in materials["materials"]}
require({"sio2", "si", "au", "ag"}.issubset(material_ids), "missing preview materials")
require("production-grade optical constants" in materials["catalog_note"], "material catalog must carry preview warning")

material_detail = get("/api/materials/sio2")
require(material_detail["material"]["material_id"] == "sio2", "sio2 material detail missing")

material_suggestion = post("/api/materials/suggest", {"application": "nanoparticle plasmonics"})
suggestion_ids = {item["material_id"] for item in material_suggestion["suggested_materials"]}
require({"au", "ag", "sio2"}.issubset(suggestion_ids), "material suggestion missing plasmonics candidates")

examples = get("/api/examples")
example_ids = {item["example_id"] for item in examples["examples"]}
require(
    {
        "nanoparticle_plasmonics",
        "thin_film_coating",
        "waveguide_mode",
        "photonic_crystal_band",
        "dielectric_metasurface_preview",
        "lens_raytrace_preview",
    }.issubset(example_ids),
    "missing optical design examples",
)

example_detail = get("/api/examples/nanoparticle_plasmonics")
require(example_detail["example"]["summary"]["example_id"] == "nanoparticle_plasmonics", "example detail missing")

example_agent_trace = post("/api/examples/nanoparticle_plasmonics/agent-trace", {})
example_agent_names = {item["agent_name"] for item in example_agent_trace["agents"]}
require(
    {
        "SpecAgent",
        "MaterialAgent",
        "GeometryAgent",
        "AdapterAgent",
        "WorkflowAgent",
        "EvidenceAgent",
        "SafetyAgent",
        "RecommendationAgent",
    }.issubset(example_agent_names),
    "example agent trace missing expected agents",
)

agent_trace = post("/api/agent-trace", {"example_id": "nanoparticle_plasmonics", "text": "nanoparticle plasmonics"})
agent_names = {item["agent_name"] for item in agent_trace["agents"]}
require({"SpecAgent", "MaterialAgent", "AdapterAgent", "SafetyAgent"}.issubset(agent_names), "agent trace missing expected agents")

agent_session = post(
    "/api/agent-session",
    {
        "goal": "Create a local preview workflow for a silver nanoparticle scattering case.",
        "example_id": "nanoparticle_plasmonics",
        "language": "en",
    },
)
require(agent_session["optical_intent_summary"], "agent session missing optical intent")
require(agent_session["plan_steps"], "agent session missing plan steps")
require(agent_session["artifacts"], "agent session missing artifacts")
require(agent_session["permission_gates"], "agent session missing permission gates")
require(agent_session["tool_call_ledger"], "agent session missing tool call ledger")

tool_capabilities = get("/api/tool-capabilities")
internal_tools = {item["tool_name"] for item in tool_capabilities["internal_tools"]}
require("optical_calculators" in internal_tools, "tool capabilities missing optical calculators")

backend_report = get("/api/backend-capability-report")
require(backend_report["package"]["package_version"] == "0.9.0rc7.dev0", "backend report package mismatch")
require(backend_report["design_case_cross_checks"], "backend report missing design case checks")
require(all(item["executed"] is False for item in backend_report["blocked_external_actions"]), "blocked action executed")

design_case_cross_checks = get("/api/design-case-cross-checks")
require(design_case_cross_checks["summary"]["total"] == 6, "design case cross-check count mismatch")
require(design_case_cross_checks["summary"]["fail"] == 0, "design case cross-check failed")
require(
    design_case_cross_checks["summary"]["requirement_templates_fail"] == 0,
    "requirement template cross-check failed",
)

design_requirements = get("/api/design-requirements")
require(design_requirements["template_count"] == 7, "design requirement template count mismatch")

design_requirement_detail = get("/api/design-requirements/thin_film_ar_coating")
require(
    design_requirement_detail["template"]["template_id"] == "thin_film_ar_coating",
    "design requirement detail mismatch",
)

design_requirement_match = post(
    "/api/design-requirements/match",
    {"goal": "Design an anti-reflection coating for glass at 550 nm.", "language": "en"},
)
require(
    design_requirement_match["matched_template_id"] == "thin_film_ar_coating",
    "design requirement match failed",
)

optical_language_infer = post(
    "/api/optical-language/infer",
    {
        "goal": "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。",
        "template_id": "nanoparticle_plasmonics",
        "language": "zh-CN",
    },
)
require(optical_language_infer["source_model"]["source_type"] == "plane_wave", "source inference failed")
require(
    optical_language_infer["monitor_model"]["monitor_type"] == "scattering_spectrum",
    "monitor inference failed",
)

optical_language_diagnose = post(
    "/api/optical-language/diagnose",
    {
        "goal": "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。",
        "template_id": "nanoparticle_plasmonics",
        "language": "zh-CN",
    },
)
require(optical_language_diagnose["safe_to_preview"] is True, "diagnostics should be safe to preview")
require(optical_language_diagnose["safe_to_run_solver"] is False, "solver safety should remain false")

thin_film = post(
    "/api/optics/thin-film",
    {"incident_n": 1.0, "substrate_n": 1.5, "wavelength_nm": 550.0, "layers": [{"n": 1.22, "thickness_nm": 112.7}]},
)
thin_film_spectrum = post(
    "/api/optics/thin-film-spectrum",
    {
        "incident_n": 1.0,
        "substrate_n": 1.5,
        "wavelength_start_nm": 450.0,
        "wavelength_stop_nm": 700.0,
        "points": 6,
        "layers": [{"n": 1.38, "thickness_nm": 100.0}],
    },
)
quarter_wave_ar = post(
    "/api/optics/quarter-wave-ar",
    {"incident_n": 1.0, "substrate_n": 1.5, "target_wavelength_nm": 550.0},
)
paraxial = post("/api/optics/paraxial-lens", {"focal_length_mm": 50.0, "object_distance_mm": 200.0})
paraxial_system = post(
    "/api/optics/paraxial-system",
    {"elements": [{"type": "free_space", "distance_mm": 25.0}, {"type": "thin_lens", "focal_length_mm": 50.0}]},
)
two_lens_relay = post(
    "/api/optics/two-lens-relay",
    {"f1_mm": 50.0, "f2_mm": 100.0, "separation_mm": 150.0, "object_distance_mm": 100.0},
)
gaussian = post("/api/optics/gaussian-beam", {"wavelength_nm": 1064.0, "waist_um": 10.0, "z_mm": 5.0})
gaussian_series = post(
    "/api/optics/gaussian-beam-series",
    {"wavelength_nm": 1064.0, "waist_um": 10.0, "z_start_mm": 0.0, "z_stop_mm": 10.0, "points": 5},
)
gaussian_focus = post(
    "/api/optics/gaussian-beam-focus",
    {"wavelength_nm": 1064.0, "input_waist_um": 1000.0, "focal_length_mm": 50.0},
)
waveguide = post(
    "/api/optics/waveguide-estimate",
    {"core_n": 3.48, "cladding_n": 1.44, "core_thickness_um": 0.22, "wavelength_nm": 1550.0},
)
waveguide_sweep = post(
    "/api/optics/waveguide-sweep",
    {
        "core_n": 2.0,
        "cladding_n": 1.44,
        "wavelength_nm": 1550.0,
        "thickness_start_um": 0.1,
        "thickness_stop_um": 0.6,
        "points": 6,
    },
)
waveguide_range = post(
    "/api/optics/waveguide-single-mode-range",
    {"core_n": 2.0, "cladding_n": 1.44, "wavelength_nm": 1550.0},
)

for name, payload in {
    "health": health,
    "version": version,
    "adapters": adapters,
    "schema": schema,
    "parse": parse_payload,
    "validate": validate_payload,
    "workflow": workflow_payload,
    "preview": preview_payload,
    "evidence": evidence,
    "readiness": readiness,
    "materials": materials,
    "material_detail": material_detail,
    "material_suggestion": material_suggestion,
    "examples": examples,
    "example_detail": example_detail,
    "example_agent_trace": example_agent_trace,
    "agent_trace": agent_trace,
    "agent_session": agent_session,
    "tool_capabilities": tool_capabilities,
    "backend_report": backend_report,
    "design_case_cross_checks": design_case_cross_checks,
    "design_requirements": design_requirements,
    "design_requirement_detail": design_requirement_detail,
    "design_requirement_match": design_requirement_match,
    "optical_language_infer": optical_language_infer,
    "optical_language_diagnose": optical_language_diagnose,
    "thin_film": thin_film,
    "thin_film_spectrum": thin_film_spectrum,
    "quarter_wave_ar": quarter_wave_ar,
    "paraxial": paraxial,
    "paraxial_system": paraxial_system,
    "two_lens_relay": two_lens_relay,
    "gaussian": gaussian,
    "gaussian_series": gaussian_series,
    "gaussian_focus": gaussian_focus,
    "waveguide": waveguide,
    "waveguide_sweep": waveguide_sweep,
    "waveguide_range": waveguide_range,
}.items():
    require(payload["external_solver_executed"] is False, f"{name} solver flag changed")
    require(payload["external_llm_required"] is False, f"{name} LLM flag changed")
    require(payload["proprietary_solver_required"] is False, f"{name} proprietary flag changed")
    require(payload["production_grade_validation_claimed"] is False, f"{name} production claim changed")
    require(payload["formal_convergence_proof_claimed"] is False, f"{name} convergence claim changed")

print(json.dumps({"status": "ok", "checked_endpoints": 38}, indent=2))
PY

echo "NO SOLVER EXECUTION PERFORMED"
echo "NO EXTERNAL LLM CALLED"
echo "NO PROPRIETARY SOLVER REQUIRED"
echo "NO UPLOAD PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
