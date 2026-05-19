"""Adapter-native golden preview coverage reporting."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field


API_CONTRACT_VERSION = "0.1"
CASE_ROOT = Path(__file__).resolve().parents[3] / "examples" / "adapter_native_golden"
REGISTERED_PREVIEW_ADAPTERS = ("meep", "mpb", "gmsh", "elmer", "optiland")


class AdapterGoldenCoverageItem(BaseModel):
    adapter_name: str
    case_id: str
    source_type: str
    monitor_type: str
    observable_kinds: list[str] = Field(default_factory=list)
    native_source_terms: list[str] = Field(default_factory=list)
    native_monitor_terms: list[str] = Field(default_factory=list)
    expected_supported_observables: list[str] = Field(default_factory=list)
    expected_unsupported_observables: list[str] = Field(default_factory=list)
    requires_solver_for_real_result: bool
    external_solver_executed: bool = False
    preview_only: bool = True
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False
    coverage_status: str = "pass"


class AdapterGoldenCoverageReport(BaseModel):
    api_contract_version: str = API_CONTRACT_VERSION
    status: str = "ok"
    generated_from_cases: list[str] = Field(default_factory=list)
    adapters_covered: list[str] = Field(default_factory=list)
    missing_adapters: list[str] = Field(default_factory=list)
    coverage_items: list[AdapterGoldenCoverageItem] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    safety_summary: dict[str, bool] = Field(default_factory=dict)
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False
    preview_only: bool = True


def build_adapter_golden_coverage_report(
    case_root: Path = CASE_ROOT,
) -> AdapterGoldenCoverageReport:
    """Build a local coverage matrix from adapter-native golden preview cases.

    This function only reads local fixture files. It does not run adapter
    solvers, call external LLMs, access the network, upload, tag, or release.
    """

    warnings: list[str] = []
    items: list[AdapterGoldenCoverageItem] = []
    case_dirs = sorted(path for path in case_root.iterdir() if path.is_dir()) if case_root.exists() else []
    if not case_dirs:
        warnings.append(f"No adapter-native golden case directories found at {case_root}.")

    for case_dir in case_dirs:
        case_id = case_dir.name
        try:
            source_model = _load_json(case_dir / "source_model.json")
            monitor_model = _load_json(case_dir / "monitor_model.json")
            observables = _load_json(case_dir / "observable_diagnostics.json")
            mapping = _load_json(case_dir / "adapter_mapping.json")
            expected_metadata = _load_optional_json(case_dir / "expected_metadata.json")
        except FileNotFoundError as exc:
            warnings.append(f"{case_id}: missing {exc.filename}")
            continue
        except json.JSONDecodeError as exc:
            warnings.append(f"{case_id}: invalid JSON in {exc.doc[:40]!r}")
            continue

        coverage_status = "pass"
        if expected_metadata:
            coverage_status = _metadata_coverage_status(
                case_id,
                source_model,
                monitor_model,
                observables,
                mapping,
                expected_metadata,
                warnings,
            )
        elif not (case_dir / "expected_metadata.json").exists():
            coverage_status = "warning"
            warnings.append(f"{case_id}: expected_metadata.json is not present.")

        items.append(
            AdapterGoldenCoverageItem(
                adapter_name=mapping.get("adapter_name", "unknown"),
                case_id=case_id,
                source_type=source_model.get("source_type", "unknown"),
                monitor_type=monitor_model.get("monitor_type", "unknown"),
                observable_kinds=[
                    item.get("observable_kind", "unknown") for item in observables
                ],
                native_source_terms=list(mapping.get("native_source_terms", [])),
                native_monitor_terms=list(mapping.get("native_monitor_terms", [])),
                expected_supported_observables=list(
                    mapping.get("supported_observables", [])
                ),
                expected_unsupported_observables=list(
                    mapping.get("unsupported_observables", [])
                ),
                requires_solver_for_real_result=bool(
                    mapping.get("requires_solver_for_real_result", True)
                ),
                external_solver_executed=bool(
                    mapping.get("external_solver_executed", False)
                ),
                preview_only=bool(mapping.get("preview_only", True)),
                production_grade_validation_claimed=bool(
                    mapping.get("production_grade_validation_claimed", False)
                ),
                formal_convergence_proof_claimed=bool(
                    mapping.get("formal_convergence_proof_claimed", False)
                ),
                coverage_status=coverage_status,
            )
        )

    adapters_covered = sorted({item.adapter_name for item in items})
    missing_adapters = [
        adapter for adapter in REGISTERED_PREVIEW_ADAPTERS if adapter not in adapters_covered
    ]
    if missing_adapters:
        warnings.append(
            "Missing adapter-native golden coverage for: " + ", ".join(missing_adapters)
        )
    safety_ok = all(
        item.external_solver_executed is False
        and item.preview_only is True
        and item.production_grade_validation_claimed is False
        and item.formal_convergence_proof_claimed is False
        for item in items
    )
    status = "ok"
    if missing_adapters or any(item.coverage_status == "fail" for item in items):
        status = "needs_review"
    elif warnings or not safety_ok:
        status = "warning"
    return AdapterGoldenCoverageReport(
        status=status,
        generated_from_cases=[item.case_id for item in items],
        adapters_covered=adapters_covered,
        missing_adapters=missing_adapters,
        coverage_items=items,
        warnings=warnings,
        safety_summary={
            "no_solver_execution": safety_ok,
            "no_external_llm": True,
            "preview_only": all(item.preview_only for item in items),
            "no_production_grade_validation_claim": all(
                item.production_grade_validation_claimed is False for item in items
            ),
            "no_formal_convergence_proof_claim": all(
                item.formal_convergence_proof_claimed is False for item in items
            ),
        },
        external_solver_executed=False,
        external_llm_required=False,
        proprietary_solver_required=False,
        production_grade_validation_claimed=False,
        formal_convergence_proof_claimed=False,
        preview_only=True,
    )


def _metadata_coverage_status(
    case_id: str,
    source_model: dict[str, Any],
    monitor_model: dict[str, Any],
    observables: list[dict[str, Any]],
    mapping: dict[str, Any],
    expected_metadata: dict[str, Any],
    warnings: list[str],
) -> str:
    expected_observables = set(expected_metadata.get("observable_kinds", []))
    actual_observables = {item.get("observable_kind") for item in observables}
    actual_native_terms = _serialized_terms(
        mapping.get("native_source_terms", []),
        mapping.get("native_monitor_terms", []),
        mapping.get("supported_observables", []),
        mapping.get("unsupported_observables", []),
        mapping.get("preview_metadata", {}),
        mapping.get("diagnostics", []),
        mapping.get("warnings", []),
    )
    checks = {
        "adapter_name": mapping.get("adapter_name")
        == expected_metadata.get("adapter_name"),
        "source_type": source_model.get("source_type")
        == expected_metadata.get("source_type"),
        "monitor_type": monitor_model.get("monitor_type")
        == expected_metadata.get("monitor_type"),
        "observable_kinds": expected_observables.issubset(actual_observables),
        "requires_solver_for_real_result": mapping.get("requires_solver_for_real_result")
        is expected_metadata.get("requires_solver_for_real_result"),
        "external_solver_executed": mapping.get("external_solver_executed")
        is expected_metadata.get("external_solver_executed"),
        "preview_only": mapping.get("preview_only")
        is expected_metadata.get("preview_only"),
        "production_grade_validation_claimed": mapping.get(
            "production_grade_validation_claimed"
        )
        is expected_metadata.get("production_grade_validation_claimed"),
        "formal_convergence_proof_claimed": mapping.get(
            "formal_convergence_proof_claimed"
        )
        is expected_metadata.get("formal_convergence_proof_claimed"),
        "required_native_terms": all(
            str(term).lower() in actual_native_terms
            for term in expected_metadata.get("required_native_terms", [])
        ),
    }
    failed = [name for name, passed in checks.items() if not passed]
    if failed:
        warnings.append(f"{case_id}: expected metadata mismatch in {', '.join(failed)}.")
        return "fail"
    return "pass"


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _load_optional_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return _load_json(path)


def _serialized_terms(*values: Any) -> str:
    return json.dumps(values, ensure_ascii=False, sort_keys=True).lower()
