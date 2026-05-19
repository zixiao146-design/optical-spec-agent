"""Adapter-native golden API fixture tests."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API_EXAMPLES = ROOT / "examples" / "api"


EXPECTED = {
    "adapter_native_golden_meep_response.json": ["meep", "scattering_spectrum", "GaussianSource"],
    "adapter_native_golden_mpb_response.json": ["mpb", "band_structure", "k-points"],
    "adapter_native_golden_gmsh_response.json": ["gmsh", "mesh_region", "Physical Surface/Volume groups"],
    "adapter_native_golden_elmer_response.json": ["elmer", "Boundary Condition placeholders", "ElmerSolver"],
    "adapter_native_golden_optiland_response.json": ["optiland", "ray bundle", "image plane"],
    "adapter_native_golden_coverage_response.json": ["optiland_lens_image_plane", "adapters_covered", "coverage_items"],
    "backend_capability_report_with_golden_coverage_response.json": ["adapter_native_golden_coverage", "coverage_items", "missing_adapters"],
}


def _load(name: str) -> dict:
    return json.loads((API_EXAMPLES / name).read_text(encoding="utf-8"))


def test_adapter_native_golden_fixtures_exist_and_keep_safety_flags():
    for filename, fragments in EXPECTED.items():
        payload = _load(filename)
        assert payload["api_contract_version"] == "0.1"
        assert payload["external_solver_executed"] is False
        assert payload["external_llm_required"] is False
        assert payload["proprietary_solver_required"] is False
        assert payload["production_grade_validation_claimed"] is False
        assert payload["formal_convergence_proof_claimed"] is False
        if "adapter_source_monitor_mapping" not in payload:
            serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
            for fragment in fragments:
                assert fragment in serialized
            continue
        mapping = payload["adapter_source_monitor_mapping"]
        assert mapping["external_solver_executed"] is False
        assert mapping["preview_only"] is True
        serialized = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        for fragment in fragments:
            assert fragment in serialized


def test_adapter_native_golden_coverage_fixture_has_all_adapters():
    payload = _load("adapter_native_golden_coverage_response.json")
    assert payload["status"] == "ok"
    assert set(payload["adapters_covered"]) == {"meep", "mpb", "gmsh", "elmer", "optiland"}
    assert payload["missing_adapters"] == []
    assert payload["external_solver_executed"] is False
    assert all(item["coverage_status"] == "pass" for item in payload["coverage_items"])
