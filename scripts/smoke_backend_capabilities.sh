#!/usr/bin/env bash
set -euo pipefail

# Backend capability smoke is local-only:
# - no solver execution
# - no external LLM calls
# - no upload, tag, or release actions

python scripts/audit_sub_agents.py
python scripts/check_adapter_native_golden.py
python scripts/evaluate_application_domain_benchmarks.py
python scripts/audit_validation_claims.py
env -u OSA_RUN_OPTIONAL_GMSH_VALIDATION \
    -u OSA_RUN_OPTIONAL_MEEP_VALIDATION \
    -u OSA_RUN_OPTIONAL_MPB_VALIDATION \
    -u OSA_RUN_OPTIONAL_OPTILAND_VALIDATION \
    -u OSA_RUN_OPTIONAL_ELMER_VALIDATION \
    ./scripts/run_optional_solver_micro_benchmarks.sh

python - <<'PY'
from fastapi.testclient import TestClient

from optical_spec_agent.api.app import app
from optical_spec_agent.optics.fiber_coupling import gaussian_mode_overlap
from optical_spec_agent.optics.gaussian_beam import gaussian_beam_parameters, propagate_gaussian_beam
from optical_spec_agent.optics.paraxial import thin_lens
from optical_spec_agent.optics.polarization import (
    jones_linear_polarizer,
    jones_waveplate,
    linear_polarization,
)
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
require("adapter_native_golden_coverage" in internal_tools, "adapter-native golden coverage missing")
require("ambiguous_requirement_matching" in internal_tools, "ambiguous requirement matching missing")
require("application_domain_registry" in internal_tools, "application domain registry missing")
require("material_template_cross_checks" in internal_tools, "material-template cross-checks missing")
require("application_domain_benchmarks" in internal_tools, "application domain benchmarks missing")
require("validation_maturity_summary" in internal_tools, "validation maturity summary missing")

maturity = client.get("/api/backend-validation-maturity")
require(maturity.status_code == 200, "/api/backend-validation-maturity failed")
maturity_payload = maturity.json()
require(maturity_payload["summary"]["record_count"] >= 17, "validation maturity records missing")
require(
    maturity_payload["summary"]["calculator_maturity_level"] == "sanity_checked_preview",
    "calculator maturity level changed",
)
require(
    maturity_payload["summary"]["application_domain_maturity_level"]
    == "benchmark_checked_preview",
    "application domain maturity level changed",
)
require(
    maturity_payload["summary"]["optional_solver_micro_benchmark_default"]
    == "no_solver_execution",
    "optional solver micro-benchmark default changed",
)
require(
    maturity_payload["summary"]["optional_solver_micro_benchmarks_opt_in_required"] is True,
    "optional solver micro-benchmarks no longer require opt-in",
)
require(maturity_payload["external_solver_executed"] is False, "validation maturity executed solver")
require(
    maturity_payload["production_grade_validation_claimed"] is False,
    "validation maturity overclaimed production-grade validation",
)
require(
    maturity_payload["formal_convergence_proof_claimed"] is False,
    "validation maturity overclaimed convergence proof",
)

material_diagnose = client.post(
    "/api/materials/diagnose",
    json={"material_id": "ag", "application": "nanoparticle plasmonics"},
)
require(material_diagnose.status_code == 200, "/api/materials/diagnose failed")
material_diag_payload = material_diagnose.json()
require(
    material_diag_payload["diagnostic"]["production_grade_optical_constants"] is False,
    "material diagnostics overclaimed production-grade constants",
)
require(
    material_diag_payload["diagnostic"]["requires_user_verification"] is True,
    "material diagnostics missing user verification",
)

ambiguous_match = client.post(
    "/api/design-requirements/match",
    json={"goal": "Design a waveguide and thin-film coating preview."},
)
require(ambiguous_match.status_code == 200, "/api/design-requirements/match ambiguous failed")
ambiguous_payload = ambiguous_match.json()
require(ambiguous_payload["confidence"] == "low", "ambiguous match should be low confidence")
require(len(ambiguous_payload["candidate_templates"]) >= 2, "ambiguous candidates missing")
require(ambiguous_payload["no_external_llm_used"] is True, "ambiguous matching used external LLM")

domains = client.get("/api/application-domains")
require(domains.status_code == 200, "/api/application-domains failed")
domains_payload = domains.json()
require(domains_payload["domain_count"] == 10, "application domain count mismatch")
require(
    domains_payload["production_grade_validation_claimed"] is False,
    "domain registry overclaimed validation",
)

waveguide_domain = client.post(
    "/api/application-domains/match",
    json={"goal": "请设计一个 1550 nm 单模硅氮波导预览。", "language": "zh-CN"},
)
require(waveguide_domain.status_code == 200, "/api/application-domains/match failed")
waveguide_payload = waveguide_domain.json()
require("slab_waveguide" in waveguide_payload["matched_domains"], "waveguide domain match failed")
require(waveguide_payload["no_external_llm_used"] is True, "domain matching used external LLM")

domain_checks = client.get("/api/application-domain-cross-checks")
require(domain_checks.status_code == 200, "/api/application-domain-cross-checks failed")
domain_check_payload = domain_checks.json()
require(domain_check_payload["summary"]["total"] == 10, "application cross-check count mismatch")
require(domain_check_payload["summary"]["fail"] == 0, "application domain cross-check failed")
require(domain_check_payload["external_solver_executed"] is False, "domain cross-check executed solver")

benchmarks = client.get("/api/application-domain-benchmarks")
require(benchmarks.status_code == 200, "/api/application-domain-benchmarks failed")
benchmark_payload = benchmarks.json()
require(benchmark_payload["scenario_count"] >= 19, "application benchmark count mismatch")
require(benchmark_payload["scenario_type_counts"]["positive"] >= 10, "positive benchmark count mismatch")

benchmark_eval = client.post("/api/application-domain-benchmarks/nanoparticle_plasmonics_positive/evaluate")
require(benchmark_eval.status_code == 200, "application benchmark evaluation failed")
require(benchmark_eval.json()["status"] in {"pass", "warn"}, "nanoparticle benchmark did not pass")

benchmark_results = client.get("/api/application-domain-benchmark-results")
require(benchmark_results.status_code == 200, "/api/application-domain-benchmark-results failed")
benchmark_results_payload = benchmark_results.json()
require(benchmark_results_payload["summary"]["fail"] == 0, "application benchmark failed")
require(benchmark_results_payload["summary"]["warn"] == 0, "application benchmark warning remained")
require(benchmark_results_payload["external_solver_executed"] is False, "benchmark executed solver")

golden_coverage = client.get("/api/adapter-native-golden-coverage")
require(golden_coverage.status_code == 200, "/api/adapter-native-golden-coverage failed")
golden_payload = golden_coverage.json()
require(golden_payload["status"] == "ok", "adapter golden coverage status changed")
require(
    set(golden_payload["adapters_covered"]) == {"meep", "mpb", "gmsh", "elmer", "optiland"},
    "adapter golden coverage adapter list mismatch",
)
require(golden_payload["missing_adapters"] == [], "adapter golden coverage missing adapters")
require(golden_payload["external_solver_executed"] is False, "golden coverage executed solver")
require(
    all(item["coverage_status"] == "pass" for item in golden_payload["coverage_items"]),
    "adapter golden coverage case failed",
)

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
require(
    ledger["requirements.match_ambiguity_check"]["executed"] is True,
    "ambiguity check not executed",
)
require(
    ledger["optical_language.generate_disambiguation_questions"]["executed"] is True,
    "disambiguation questions not generated",
)
require(
    ledger["application_domains.match_goal"]["executed"] is True,
    "application domain matching not executed",
)
require(
    ledger["application_domains.cross_check_domain"]["executed"] is True,
    "application domain cross-check not executed",
)
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
require("match_confidence" in session_payload, "agent session missing match confidence")
require("missing_critical_inputs" in session_payload, "agent session missing critical inputs")
require("application_domain_id" in session_payload, "agent session missing application domain")
require("domain_cross_check_status" in session_payload, "agent session missing domain status")

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
    (
        "/api/optics/fiber-coupling",
        {
            "waist_input_um": 5.2,
            "waist_fiber_um": 5.2,
            "lateral_offset_um": 0.0,
            "angular_tilt_mrad": 0.0,
            "wavelength_nm": 1550.0,
        },
    ),
    (
        "/api/optics/polarization-jones",
        {
            "element_type": "waveplate",
            "input_angle_deg": 0.0,
            "retardance_rad": 3.141592653589793,
            "fast_axis_deg": 45.0,
        },
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

fiber_reference = gaussian_mode_overlap(5.2, 5.2, wavelength_nm=1550.0)
require(abs(fiber_reference.result["coupling_efficiency_estimate"] - 1.0) < 1e-12, "fiber coupling sanity check failed")
fiber_offset = gaussian_mode_overlap(5.2, 5.2, lateral_offset_um=2.0, wavelength_nm=1550.0)
require(
    fiber_offset.result["coupling_efficiency_estimate"]
    < fiber_reference.result["coupling_efficiency_estimate"],
    "fiber coupling offset-loss reference failed",
)
require(
    fiber_offset.quality.reference_case == "fiber_gaussian_offset_loss",
    "fiber coupling offset reference case missing",
)

horizontal = linear_polarization(0.0)
crossed = jones_linear_polarizer(horizontal.result["output_jones"], 90.0)
require(crossed.result["intensity"] < 1e-24, "polarization crossed-polarizer sanity check failed")
diagonal = linear_polarization(45.0)
malus = jones_linear_polarizer(diagonal.result["output_jones"], 0.0)
require(abs(malus.result["intensity"] - 0.5) < 1e-12, "polarization Malus sanity check failed")
quarter_wave = jones_waveplate(diagonal.result["output_jones"], 3.141592653589793 / 2.0, 0.0)
require(
    abs(quarter_wave.result["relative_phase_rad"] - 3.141592653589793 / 2.0) < 1e-12,
    "polarization quarter-wave sanity check failed",
)

print("CALCULATOR SANITY CHECKS PASSED")
print("FIBER COUPLING REFERENCE SANITY PASSED")
print("POLARIZATION REFERENCE SANITY PASSED")
print("MATERIAL PROVENANCE DIAGNOSTICS PASSED")
print("AMBIGUOUS REQUIREMENT MATCHING PASSED")
print("APPLICATION DOMAIN COVERAGE PASSED")
print("MATERIAL TEMPLATE CROSS-CHECKS PASSED")
print("APPLICATION DOMAIN BENCHMARKS PASSED")
print("FIBER COUPLING PREVIEW PASSED")
print("POLARIZATION PREVIEW PASSED")
print("SOURCE/MONITOR INFERENCE PASSED")
print("MISSING INPUT DIAGNOSTICS PASSED")
print("OBSERVABLE DIAGNOSTICS PASSED")
print("ADAPTER SOURCE/MONITOR MAPPING PASSED")
print("ADAPTER NATIVE GOLDEN CHECKS PASSED")
print("ADAPTER NATIVE METADATA DIFF PASSED")
print("ADAPTER GOLDEN COVERAGE REPORT PASSED")
print("VALIDATION MATURITY CHECKS PASSED")
print("VALIDATION CLAIM AUDIT PASSED")
print("OPTIONAL SOLVER MICRO-BENCHMARK PLAN PASSED")
print("Backend capabilities smoke passed")
PY

echo "CALCULATOR SANITY CHECKS PASSED"
echo "FIBER COUPLING REFERENCE SANITY PASSED"
echo "POLARIZATION REFERENCE SANITY PASSED"
echo "MATERIAL PROVENANCE DIAGNOSTICS PASSED"
echo "AMBIGUOUS REQUIREMENT MATCHING PASSED"
echo "APPLICATION DOMAIN COVERAGE PASSED"
echo "MATERIAL TEMPLATE CROSS-CHECKS PASSED"
echo "APPLICATION DOMAIN BENCHMARKS PASSED"
echo "FIBER COUPLING PREVIEW PASSED"
echo "POLARIZATION PREVIEW PASSED"
echo "SOURCE/MONITOR INFERENCE PASSED"
echo "MISSING INPUT DIAGNOSTICS PASSED"
echo "OBSERVABLE DIAGNOSTICS PASSED"
echo "ADAPTER SOURCE/MONITOR MAPPING PASSED"
echo "ADAPTER NATIVE GOLDEN CHECKS PASSED"
echo "ADAPTER NATIVE METADATA DIFF PASSED"
echo "ADAPTER GOLDEN COVERAGE REPORT PASSED"
echo "VALIDATION MATURITY CHECKS PASSED"
echo "VALIDATION CLAIM AUDIT PASSED"
echo "OPTIONAL SOLVER MICRO-BENCHMARK PLAN PASSED"
echo "NO SOLVER EXECUTION PERFORMED"
echo "NO EXTERNAL LLM CALLED"
echo "NO UPLOAD PERFORMED"
echo "NO TAG CREATED"
echo "NO RELEASE CREATED"
