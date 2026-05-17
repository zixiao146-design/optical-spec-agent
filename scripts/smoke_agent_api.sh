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
}.items():
    require(payload["external_solver_executed"] is False, f"{name} solver flag changed")
    require(payload["external_llm_required"] is False, f"{name} LLM flag changed")
    require(payload["proprietary_solver_required"] is False, f"{name} proprietary flag changed")
    require(payload["production_grade_validation_claimed"] is False, f"{name} production claim changed")
    require(payload["formal_convergence_proof_claimed"] is False, f"{name} convergence claim changed")

print(json.dumps({"status": "ok", "checked_endpoints": 17}, indent=2))
PY

echo "NO SOLVER EXECUTION PERFORMED"
echo "NO EXTERNAL LLM CALLED"
echo "NO PROPRIETARY SOLVER REQUIRED"
echo "NO UPLOAD PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
