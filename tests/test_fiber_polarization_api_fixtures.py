"""Fixture coverage for fiber/polarization reference API cases."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
API_EXAMPLES = ROOT / "examples" / "api"


def _load(name: str) -> dict:
    return json.loads((API_EXAMPLES / name).read_text(encoding="utf-8"))


def test_fiber_polarization_reference_fixtures_exist_and_are_safe():
    fixtures = [
        ("fiber_coupling_perfect_match_response.json", "fiber_gaussian_perfect_overlap"),
        ("fiber_coupling_offset_response.json", "fiber_gaussian_offset_loss"),
        ("polarization_linear_polarizer_response.json", "jones_linear_polarizer_malus"),
        ("polarization_waveplate_response.json", "jones_quarter_waveplate_phase_preview"),
    ]
    for filename, reference_case in fixtures:
        payload = _load(filename)
        assert payload["api_contract_version"] == "0.1"
        assert payload["status"] == "ok"
        assert payload["quality"]["quality_level"] == "sanity_checked_preview"
        assert payload["quality"]["reference_case"] == reference_case
        assert payload["quality"]["production_grade_validation_claimed"] is False
        assert payload["quality"]["formal_convergence_proof_claimed"] is False
        assert payload["external_solver_executed"] is False
        assert payload["external_llm_required"] is False
        assert payload["production_grade_validation_claimed"] is False
        assert payload["formal_convergence_proof_claimed"] is False
        assert payload["assumptions"]
        assert payload["diagnostics"]


def test_fiber_polarization_reference_requests_exist():
    for filename in [
        "fiber_coupling_perfect_match_request.json",
        "fiber_coupling_offset_request.json",
        "polarization_linear_polarizer_request.json",
        "polarization_waveplate_request.json",
    ]:
        payload = _load(filename)
        assert payload
