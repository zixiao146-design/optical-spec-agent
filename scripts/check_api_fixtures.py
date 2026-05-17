#!/usr/bin/env python3
"""Check local Agent API fixtures against live TestClient response shapes."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from fastapi.testclient import TestClient  # noqa: E402

from optical_spec_agent.api.app import app  # noqa: E402


API_EXAMPLES = ROOT / "examples" / "api"
MANIFEST = API_EXAMPLES / "frontend_fixture_manifest.json"
API_CONTRACT_VERSION = "0.1"

ERROR_PAYLOADS: dict[str, dict[str, Any]] = {
    "error-invalid-spec": {},
    "error-unsupported-adapter": {
        "path": "examples/specs/minimal_nanoparticle.json",
        "tool": "unknown",
    },
    "error-invalid-workflow-request": {},
    "error-external-llm-not-enabled": {
        "text": "Use MPB for a band diagram.",
        "parser": "llm",
    },
    "error-agent-session-empty-goal": {"goal": "   "},
}

SAFETY_FLAGS = (
    "external_solver_executed",
    "external_llm_required",
    "proprietary_solver_required",
    "production_grade_validation_claimed",
    "formal_convergence_proof_claimed",
)


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _request_payload(entry: dict[str, Any]) -> Any:
    request_file = entry.get("request_file")
    if request_file:
        return _load_json(API_EXAMPLES / request_file)
    return ERROR_PAYLOADS.get(entry["name"])


def _call(client: TestClient, entry: dict[str, Any]) -> dict[str, Any]:
    method = entry["method"].upper()
    endpoint = entry["endpoint"]
    if method == "GET":
        response = client.get(endpoint)
    elif method == "POST":
        response = client.post(endpoint, json=_request_payload(entry) or {})
    else:
        raise AssertionError(f"Unsupported fixture method: {method}")
    if response.status_code >= 500:
        raise AssertionError(f"{entry['name']} returned {response.status_code}")
    return response.json()


def _assert_safe(payload: dict[str, Any], *, name: str) -> None:
    if payload.get("api_contract_version") is not None:
        assert payload["api_contract_version"] == API_CONTRACT_VERSION, name
    for flag in SAFETY_FLAGS:
        if flag in payload:
            assert payload[flag] is False, f"{name} changed safety flag {flag}"


def main() -> int:
    manifest = _load_json(MANIFEST)
    assert manifest["api_contract_version"] == API_CONTRACT_VERSION
    client = TestClient(app)

    checked = 0
    for entry in manifest["fixtures"]:
        if entry.get("request_file") is not None:
            assert (API_EXAMPLES / entry["request_file"]).exists(), entry["name"]
        response_path = API_EXAMPLES / entry["response_file"]
        assert response_path.exists(), entry["name"]

        fixture_payload = _load_json(response_path)
        live_payload = _call(client, entry)

        assert set(live_payload) == set(fixture_payload), (
            f"{entry['name']} top-level keys differ: "
            f"live={sorted(live_payload)} fixture={sorted(fixture_payload)}"
        )
        _assert_safe(fixture_payload, name=f"{entry['name']} fixture")
        _assert_safe(live_payload, name=f"{entry['name']} live")
        assert entry["no_network"] is True, entry["name"]
        assert entry["external_solver_executed"] is False, entry["name"]
        assert entry["external_llm_required"] is False, entry["name"]
        assert entry["proprietary_solver_required"] is False, entry["name"]
        assert entry["production_grade_validation_claimed"] is False, entry["name"]
        assert entry["formal_convergence_proof_claimed"] is False, entry["name"]
        checked += 1

    print(f"Checked {checked} local Agent API fixture(s).")
    print("NO SOLVER EXECUTION PERFORMED")
    print("NO EXTERNAL LLM CALLED")
    print("NO PROPRIETARY SOLVER REQUIRED")
    print("NO NETWORK ACCESS REQUIRED")
    print("NO UPLOAD PERFORMED")
    print("NO TAG CREATED")
    print("NO RELEASE CREATED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
