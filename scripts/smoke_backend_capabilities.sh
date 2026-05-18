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
from optical_spec_agent.optics.gaussian_beam import gaussian_beam_parameters, propagate_gaussian_beam
from optical_spec_agent.optics.paraxial import thin_lens
from optical_spec_agent.optics.thin_film import calculate_thin_film_stack
from optical_spec_agent.optics.waveguide import slab_waveguide_v_number


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
require("source_monitor_inference" in internal_tools, "source/monitor inference missing")
require("missing_input_diagnostics" in internal_tools, "missing-input diagnostics missing")
require("observable_diagnostics" in internal_tools, "observable diagnostics missing")
require("adapter_native_mapping" in internal_tools, "adapter-native mapping missing")

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
require(ledger["optical_language.infer_source_monitor"]["executed"] is True, "source/monitor inference not executed")
require(ledger["optical_language.diagnose_missing_inputs"]["executed"] is True, "missing-input diagnostics not executed")
require(ledger["optical_language.diagnose_observable"]["executed"] is True, "observable diagnostics not executed")
require(
    ledger["optical_language.map_source_monitor_to_adapter"]["executed"] is True,
    "adapter source/monitor mapping not executed",
)
require(ledger["external_llm"]["executed"] is False, "external LLM unexpectedly executed")
require(ledger["pypi_publish"]["executed"] is False, "PyPI publish unexpectedly executed")
require(session_payload["observable_diagnostics"], "agent session missing observable diagnostics")
require(
    session_payload["adapter_source_monitor_mapping"],
    "agent session missing adapter source/monitor mapping",
)

source_monitor = client.post(
    "/api/optical-language/infer",
    json={
        "goal": "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。",
        "template_id": "nanoparticle_plasmonics",
        "language": "zh-CN",
    },
)
require(source_monitor.status_code == 200, "/api/optical-language/infer failed")
source_payload = source_monitor.json()
require(source_payload["source_model"]["source_type"] == "plane_wave", "source inference mismatch")
require(source_payload["monitor_model"]["monitor_type"] == "scattering_spectrum", "monitor inference mismatch")

diagnostics = client.post(
    "/api/optical-language/diagnose",
    json={
        "goal": "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。",
        "template_id": "nanoparticle_plasmonics",
        "language": "zh-CN",
    },
)
require(diagnostics.status_code == 200, "/api/optical-language/diagnose failed")
diag_payload = diagnostics.json()
require(diag_payload["safe_to_preview"] is True, "diagnostics should be preview-safe")
require(diag_payload["safe_to_run_solver"] is False, "diagnostics should block solver by default")

observable = client.post(
    "/api/optical-language/observables/diagnose",
    json={
        "goal": "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。",
        "template_id": "nanoparticle_plasmonics",
        "language": "zh-CN",
    },
)
require(observable.status_code == 200, "/api/optical-language/observables/diagnose failed")
observable_payload = observable.json()
observable_kinds = {item["observable_kind"] for item in observable_payload["observable_diagnostics"]}
require("scattering_spectrum" in observable_kinds, "scattering observable diagnostic missing")
require(
    observable_payload["production_grade_validation_claimed"] is False,
    "observable diagnostics overclaimed validation",
)

adapter_mapping = client.post(
    "/api/optical-language/adapter-mapping",
    json={
        "adapter_name": "meep",
        "goal": "请为一个银纳米颗粒位于薄膜上的散射问题生成本地预览工作流。",
        "template_id": "nanoparticle_plasmonics",
        "language": "zh-CN",
    },
)
require(adapter_mapping.status_code == 200, "/api/optical-language/adapter-mapping failed")
mapping_payload = adapter_mapping.json()
require(
    mapping_payload["adapter_source_monitor_mapping"]["adapter_name"] == "meep",
    "adapter mapping did not preserve adapter name",
)
require(
    "scattering_spectrum"
    in mapping_payload["adapter_source_monitor_mapping"]["supported_observables"],
    "Meep mapping missing scattering support metadata",
)
require(
    mapping_payload["adapter_source_monitor_mapping"]["external_solver_executed"] is False,
    "adapter mapping executed solver",
)

adapter_preview = client.post(
    "/api/adapter-preview",
    json={"path": "examples/specs/minimal_nanoparticle.json", "tool": "meep"},
)
require(adapter_preview.status_code == 200, "/api/adapter-preview source/monitor metadata failed")
preview_payload = adapter_preview.json()
require(preview_payload["source_model"], "adapter preview missing source model")
require(preview_payload["monitor_model"], "adapter preview missing monitor model")
require(preview_payload["observable_diagnostics"], "adapter preview missing observable diagnostics")
require(
    preview_payload["adapter_source_monitor_mapping"],
    "adapter preview missing adapter source/monitor mapping",
)
require(preview_payload["external_solver_executed"] is False, "adapter preview executed solver")

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
        "/api/optics/thin-film-spectrum",
        {
            "incident_n": 1.0,
            "substrate_n": 1.5,
            "wavelength_start_nm": 450.0,
            "wavelength_stop_nm": 700.0,
            "points": 6,
            "layers": [{"n": 1.38, "thickness_nm": 100.0}],
        },
    ),
    (
        "/api/optics/quarter-wave-ar",
        {"incident_n": 1.0, "substrate_n": 1.5, "target_wavelength_nm": 550.0},
    ),
    (
        "/api/optics/paraxial-lens",
        {"focal_length_mm": 50.0, "object_distance_mm": 200.0},
    ),
    (
        "/api/optics/paraxial-system",
        {
            "elements": [
                {"type": "free_space", "distance_mm": 25.0},
                {"type": "thin_lens", "focal_length_mm": 50.0},
            ]
        },
    ),
    (
        "/api/optics/two-lens-relay",
        {"f1_mm": 50.0, "f2_mm": 100.0, "separation_mm": 150.0, "object_distance_mm": 100.0},
    ),
    (
        "/api/optics/gaussian-beam",
        {"wavelength_nm": 1064.0, "waist_um": 10.0, "z_mm": 5.0},
    ),
    (
        "/api/optics/gaussian-beam-series",
        {"wavelength_nm": 1064.0, "waist_um": 10.0, "z_start_mm": 0.0, "z_stop_mm": 10.0, "points": 5},
    ),
    (
        "/api/optics/gaussian-beam-focus",
        {"wavelength_nm": 1064.0, "input_waist_um": 1000.0, "focal_length_mm": 50.0},
    ),
    (
        "/api/optics/waveguide-estimate",
        {"core_n": 3.48, "cladding_n": 1.44, "core_thickness_um": 0.22, "wavelength_nm": 1550.0},
    ),
    (
        "/api/optics/waveguide-sweep",
        {
            "core_n": 2.0,
            "cladding_n": 1.44,
            "wavelength_nm": 1550.0,
            "thickness_start_um": 0.1,
            "thickness_stop_um": 0.6,
            "points": 6,
        },
    ),
    (
        "/api/optics/waveguide-single-mode-range",
        {"core_n": 2.0, "cladding_n": 1.44, "wavelength_nm": 1550.0},
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

thin_film_reference = calculate_thin_film_stack([], 550.0, incident_n=1.0, substrate_n=1.5)
require(
    abs(thin_film_reference.result["reflectance"] - 0.04) < 1e-12,
    "thin-film single-interface sanity check failed",
)

gaussian_reference = gaussian_beam_parameters(1000.0, 10.0)
z_rayleigh_mm = gaussian_reference.result["rayleigh_range_mm"]
beam_at_zr = propagate_gaussian_beam(1000.0, 10.0, z_rayleigh_mm)
require(
    abs(beam_at_zr.result["beam_radius_um"] - (10.0 * 2**0.5)) < 1e-12,
    "Gaussian Rayleigh-range sanity check failed",
)

paraxial_reference = thin_lens(50.0, 100.0)
require(paraxial_reference.result["image_distance_mm"] == 100.0, "paraxial thin-lens sanity check failed")
require(paraxial_reference.result["magnification"] == -1.0, "paraxial magnification sanity check failed")

waveguide_reference = slab_waveguide_v_number(2.0, 1.5, 0.3, 1550.0)
require(waveguide_reference.result["v_number"] > 0, "waveguide V-number sanity check failed")

print("CALCULATOR SANITY CHECKS PASSED")
print("SOURCE/MONITOR INFERENCE PASSED")
print("MISSING INPUT DIAGNOSTICS PASSED")
print("OBSERVABLE DIAGNOSTICS PASSED")
print("ADAPTER SOURCE/MONITOR MAPPING PASSED")
print("Backend capabilities smoke passed")
PY

echo "CALCULATOR SANITY CHECKS PASSED"
echo "SOURCE/MONITOR INFERENCE PASSED"
echo "MISSING INPUT DIAGNOSTICS PASSED"
echo "OBSERVABLE DIAGNOSTICS PASSED"
echo "ADAPTER SOURCE/MONITOR MAPPING PASSED"
echo "NO SOLVER EXECUTION PERFORMED"
echo "NO EXTERNAL LLM CALLED"
echo "NO UPLOAD PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
