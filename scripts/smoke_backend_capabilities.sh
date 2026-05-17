#!/usr/bin/env bash
set -euo pipefail

# Backend capability smoke is local-only:
# - no solver execution
# - no external LLM calls
# - no upload, tag, or release actions

python scripts/audit_sub_agents.py

python - <<'PY'
from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app


client = TestClient(app)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


capabilities = client.get("/api/tool-capabilities")
require(capabilities.status_code == 200, "/api/tool-capabilities failed")
cap_payload = capabilities.json()
require(cap_payload["external_solver_executed"] is False, "tool capabilities changed solver flag")
require(cap_payload["external_llm_required"] is False, "tool capabilities changed LLM flag")
internal_tools = {item["tool_name"] for item in cap_payload["internal_tools"]}
require("optical_calculators" in internal_tools, "optical calculators missing")

session = client.post(
    "/api/agent-session",
    json={
        "goal": "Plan a local thin film coating preview with no external solver.",
        "example_id": "thin_film_coating",
    },
)
require(session.status_code == 200, "/api/agent-session failed")
session_payload = session.json()
require(session_payload["tool_call_ledger"], "tool_call_ledger missing")
ledger = {entry["tool_name"]: entry for entry in session_payload["tool_call_ledger"]}
require(ledger["material_catalog.suggest"]["executed"] is True, "material catalog not executed")
require(ledger["external_llm"]["executed"] is False, "external LLM unexpectedly executed")
require(ledger["pypi_publish"]["executed"] is False, "PyPI publish unexpectedly executed")

requests = [
    (
        "/api/optics/thin-film",
        {
            "incident_n": 1.0,
            "substrate_n": 1.5,
            "wavelength_nm": 550.0,
            "layers": [{"n": 1.22, "thickness_nm": 112.7}],
        },
    ),
    (
        "/api/optics/paraxial-lens",
        {"focal_length_mm": 50.0, "object_distance_mm": 200.0},
    ),
    (
        "/api/optics/gaussian-beam",
        {"wavelength_nm": 1064.0, "waist_um": 10.0, "z_mm": 5.0},
    ),
    (
        "/api/optics/waveguide-estimate",
        {"core_n": 3.48, "cladding_n": 1.44, "core_thickness_um": 0.22, "wavelength_nm": 1550.0},
    ),
]
for endpoint, payload in requests:
    response = client.post(endpoint, json=payload)
    require(response.status_code == 200, f"{endpoint} failed")
    body = response.json()
    require(body["status"] == "ok", f"{endpoint} did not return ok")
    require(body["external_solver_executed"] is False, f"{endpoint} changed solver flag")
    require(body["external_llm_required"] is False, f"{endpoint} changed LLM flag")
    require(body["production_grade_validation_claimed"] is False, f"{endpoint} overclaimed validation")
    require(body["formal_convergence_proof_claimed"] is False, f"{endpoint} overclaimed convergence")

print("Backend capabilities smoke passed")
PY

echo "NO SOLVER EXECUTION PERFORMED"
echo "NO EXTERNAL LLM CALLED"
echo "NO UPLOAD PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
