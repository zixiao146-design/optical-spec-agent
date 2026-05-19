"""Expected metadata tests for adapter-native golden cases."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CASE_ROOT = ROOT / "examples" / "adapter_native_golden"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_every_adapter_native_golden_case_has_expected_metadata():
    case_dirs = sorted(path for path in CASE_ROOT.iterdir() if path.is_dir())
    assert len(case_dirs) == 5
    for case_dir in case_dirs:
        metadata_path = case_dir / "expected_metadata.json"
        assert metadata_path.exists(), case_dir.name
        metadata = _load(metadata_path)
        for field in [
            "adapter_name",
            "source_type",
            "monitor_type",
            "observable_kinds",
            "requires_solver_for_real_result",
            "external_solver_executed",
            "preview_only",
            "production_grade_validation_claimed",
            "formal_convergence_proof_claimed",
            "required_native_terms",
            "forbidden_claims",
        ]:
            assert field in metadata, f"{case_dir.name}/{field}"
        assert metadata["external_solver_executed"] is False
        assert metadata["preview_only"] is True
        assert metadata["production_grade_validation_claimed"] is False
        assert metadata["formal_convergence_proof_claimed"] is False
        assert metadata["required_native_terms"]
        assert {
            "production-grade",
            "formal convergence",
            "solver executed",
            "real monitor result",
        }.issubset(set(metadata["forbidden_claims"]))
