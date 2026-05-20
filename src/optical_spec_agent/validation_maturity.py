"""Conservative backend validation maturity records.

The maturity model is intentionally about evidence boundaries, not physical
truth claims. Records describe what is documented, fixture-guarded, sanity
checked, or benchmark checked by the local backend without executing external
solvers by default.
"""

from __future__ import annotations

from collections import Counter
from typing import Literal

from pydantic import BaseModel, Field


ValidationMaturityLevel = Literal[
    "documented_preview",
    "fixture_guarded_preview",
    "sanity_checked_preview",
    "benchmark_checked_preview",
    "optional_manual_solver_validated",
    "production_grade_not_claimed",
]


class ValidationMaturityRecord(BaseModel):
    area: str
    component_id: str
    maturity_level: ValidationMaturityLevel
    evidence_refs: list[str] = Field(default_factory=list)
    tests_or_scripts: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)
    production_grade_physical_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False
    external_solver_required: bool = False
    external_solver_executed_by_default: bool = False


class BackendValidationMaturityResponse(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    records: list[ValidationMaturityRecord] = Field(default_factory=list)
    summary: dict[str, object] = Field(default_factory=dict)
    preview_boundary_summary: dict[str, object] = Field(default_factory=dict)
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


CALCULATOR_IDS = [
    "thin_film",
    "paraxial",
    "gaussian_beam",
    "waveguide",
    "fiber_coupling",
    "polarization",
]


def _record(
    *,
    area: str,
    component_id: str,
    maturity_level: ValidationMaturityLevel,
    evidence_refs: list[str],
    tests_or_scripts: list[str],
    limitations: list[str],
    external_solver_required: bool = False,
) -> ValidationMaturityRecord:
    return ValidationMaturityRecord(
        area=area,
        component_id=component_id,
        maturity_level=maturity_level,
        evidence_refs=evidence_refs,
        tests_or_scripts=tests_or_scripts,
        limitations=limitations,
        external_solver_required=external_solver_required,
    )


def build_backend_validation_maturity_records() -> list[ValidationMaturityRecord]:
    """Return local-only validation maturity records for backend evidence areas."""

    records: list[ValidationMaturityRecord] = [
        _record(
            area="materials",
            component_id="material_library",
            maturity_level="documented_preview",
            evidence_refs=[
                "docs/material_provenance_policy.md",
                "docs/material_library.md",
            ],
            tests_or_scripts=[
                "tests/test_material_provenance.py",
                "tests/test_material_suitability_diagnostics.py",
            ],
            limitations=[
                "Local curated preview catalog only.",
                "User must verify optical constants before physical conclusions.",
                "Not a production-grade optical constants database.",
            ],
        ),
        _record(
            area="requirements",
            component_id="design_requirement_templates",
            maturity_level="fixture_guarded_preview",
            evidence_refs=[
                "docs/design_requirement_templates.md",
                "examples/design_requirements/",
            ],
            tests_or_scripts=[
                "tests/test_design_requirement_templates.py",
                "tests/test_requirement_matching.py",
            ],
            limitations=[
                "Deterministic heuristic matching only.",
                "Ambiguous goals produce questions rather than solver actions.",
            ],
        ),
        _record(
            area="requirements",
            component_id="natural_language_to_optical_language",
            maturity_level="fixture_guarded_preview",
            evidence_refs=[
                "docs/natural_language_to_optical_language.md",
                "docs/ambiguous_requirement_matching.md",
            ],
            tests_or_scripts=[
                "tests/test_ambiguous_requirement_matching.py",
                "tests/test_missing_input_diagnostics_deepening.py",
            ],
            limitations=[
                "No external LLM is used by default.",
                "Confidence is routing evidence, not a correctness guarantee.",
            ],
        ),
        _record(
            area="application_domains",
            component_id="application_domain_benchmarks",
            maturity_level="benchmark_checked_preview",
            evidence_refs=[
                "docs/application_domain_benchmarks.md",
                "examples/application_domain_benchmarks/",
            ],
            tests_or_scripts=[
                "scripts/evaluate_application_domain_benchmarks.py",
                "tests/test_application_domain_benchmark_evaluator.py",
            ],
            limitations=[
                "Benchmarks test deterministic routing, diagnostics, and blocked actions.",
                "Benchmarks do not establish physical accuracy.",
            ],
        ),
        _record(
            area="optical_language",
            component_id="source_monitor_diagnostics",
            maturity_level="fixture_guarded_preview",
            evidence_refs=[
                "docs/optical_language_source_monitor.md",
                "docs/source_monitor_missing_input_diagnostics.md",
            ],
            tests_or_scripts=[
                "tests/test_optical_language_inference.py",
                "tests/test_optical_language_diagnostics.py",
            ],
            limitations=[
                "Source and monitor records are preview metadata.",
                "No real solver monitor result is claimed.",
            ],
        ),
        _record(
            area="optical_language",
            component_id="observable_diagnostics",
            maturity_level="fixture_guarded_preview",
            evidence_refs=["docs/observable_diagnostics.md"],
            tests_or_scripts=[
                "tests/test_observable_diagnostics.py",
                "tests/test_optical_language_observable_api.py",
            ],
            limitations=[
                "Observable taxonomy describes requested outputs and adapter fit.",
                "Real physical outputs require separately approved solver execution.",
            ],
        ),
        _record(
            area="adapters",
            component_id="adapter_native_mapping",
            maturity_level="fixture_guarded_preview",
            evidence_refs=["docs/adapter_native_source_monitor_mapping.md"],
            tests_or_scripts=[
                "tests/test_adapter_source_monitor_mapping.py",
                "tests/test_adapter_preview_source_monitor_metadata.py",
            ],
            limitations=[
                "Adapter-native mapping is metadata preview only.",
                "External solvers are not run by default.",
            ],
            external_solver_required=True,
        ),
        _record(
            area="adapters",
            component_id="adapter_golden_coverage",
            maturity_level="fixture_guarded_preview",
            evidence_refs=[
                "docs/adapter_native_golden_coverage_matrix.md",
                "examples/adapter_native_golden/",
            ],
            tests_or_scripts=[
                "scripts/check_adapter_native_golden.py",
                "tests/test_adapter_native_golden_metadata_diff.py",
            ],
            limitations=[
                "Golden cases check preview metadata and expected fragments.",
                "Golden cases are not real solver monitor results.",
            ],
            external_solver_required=True,
        ),
        _record(
            area="agents",
            component_id="sub_agent_task_sessions",
            maturity_level="fixture_guarded_preview",
            evidence_refs=[
                "docs/sub_agent_architecture.md",
                "docs/backend_evidence_review_pack.md",
            ],
            tests_or_scripts=[
                "scripts/audit_sub_agents.py",
                "tests/test_agent_task_session.py",
            ],
            limitations=[
                "Sub-agents are deterministic backend roles in one local process.",
                "They are not independent autonomous services.",
            ],
        ),
        _record(
            area="agents",
            component_id="tool_call_ledger",
            maturity_level="fixture_guarded_preview",
            evidence_refs=["docs/tool_call_reality_matrix.md"],
            tests_or_scripts=["tests/test_tool_call_ledger.py"],
            limitations=[
                "Ledger records backend tool-call reality for local sessions.",
                "Blocked external actions remain disabled unless separately approved.",
            ],
        ),
        _record(
            area="frontend",
            component_id="agent_studio",
            maturity_level="documented_preview",
            evidence_refs=[
                "docs/frontend_mvp_product_spec.md",
                "docs/agent_command_center.md",
            ],
            tests_or_scripts=[
                "tests/test_frontend_mvp_files.py",
                "tests/test_frontend_visual_smoke_plan.py",
            ],
            limitations=[
                "Frontend is a UI/demo surface, not validation evidence.",
                "Backend evidence remains the source of validation maturity status.",
            ],
        ),
    ]

    calculator_refs = {
        "thin_film": [
            "thin_film_single_interface_air_glass",
            "thin_film_quarter_wave_ar_550nm",
        ],
        "paraxial": [
            "paraxial_thin_lens_1to1",
            "abcd_free_space_matrix",
            "two_lens_4f_relay_1_to_1",
        ],
        "gaussian_beam": [
            "gaussian_beam_rayleigh_range",
            "gaussian_beam_radius_at_rayleigh_range",
        ],
        "waveguide": [
            "waveguide_v_number_sanity",
            "slab_waveguide_v_number_sweep",
        ],
        "fiber_coupling": [
            "fiber_gaussian_perfect_overlap",
            "fiber_gaussian_offset_loss",
            "fiber_gaussian_tilt_loss",
        ],
        "polarization": [
            "jones_linear_polarizer_malus",
            "jones_half_waveplate_preview",
            "jones_quarter_waveplate_phase_preview",
        ],
    }
    for calculator_id in CALCULATOR_IDS:
        records.append(
            _record(
                area="calculators",
                component_id=f"{calculator_id}_calculator",
                maturity_level="sanity_checked_preview",
                evidence_refs=[
                    "docs/optical_calculator_reference_cases.md",
                    *calculator_refs[calculator_id],
                ],
                tests_or_scripts=[
                    f"tests/test_optics_{calculator_id}_reference_cases.py"
                    if calculator_id not in {"gaussian_beam", "thin_film"}
                    else (
                        "tests/test_optics_gaussian_beam_reference_cases.py"
                        if calculator_id == "gaussian_beam"
                        else "tests/test_optics_thin_film_reference_cases.py"
                    ),
                    "scripts/smoke_backend_capabilities.sh",
                ],
                limitations=[
                    "Analytic/local preview calculation only.",
                    "Reference cases are sanity checks, not production-grade validation.",
                    "No formal convergence proof is claimed.",
                ],
            )
        )

    optional_solver_micro_benchmarks: list[
        tuple[str, ValidationMaturityLevel, list[str], str]
    ] = [
        (
            "gmsh_optional_solver_micro_benchmark",
            "optional_manual_solver_validated",
            [
                "docs/solver_validation_micro_benchmarks.md",
                "docs/optional_solver_micro_benchmark_approval_matrix.md",
                "docs/optional_solver_micro_benchmark_readiness_status.md",
                "docs/optional_solver_environment_profiles.md",
                "docs/optional_solver_micro_benchmark_execution_packet.md",
                "docs/optional_solver_execution_sequence.md",
                "validation/solver_validation_micro_benchmarks.json",
                "validation/solver_environment_profiles.json",
                "validation/gmsh/gmsh_micro_benchmark_2026-05-20.md",
                "docs/optional_solver_approval_records/gmsh_micro_benchmark_approval_2026-05-20.md",
                "docs/optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md",
                "validation/gmsh/gmsh_validation_pilot_2026-05-14.md",
            ],
            "Gmsh has a reviewed and accepted optional manual mesh-generation smoke pass from 2026-05-20.",
        ),
        (
            "meep_optional_solver_micro_benchmark",
            "optional_manual_solver_validated",
            [
                "docs/solver_validation_micro_benchmarks.md",
                "docs/optional_solver_micro_benchmark_approval_matrix.md",
                "docs/optional_solver_micro_benchmark_readiness_status.md",
                "docs/optional_solver_environment_profiles.md",
                "docs/optional_solver_micro_benchmark_execution_packet.md",
                "docs/optional_solver_execution_sequence.md",
                "docs/optional_solver_approval_records/meep_micro_benchmark_decision_packet.md",
                "docs/optional_solver_approval_records/meep_micro_benchmark_approval_2026-05-20.md",
                "validation/solver_validation_micro_benchmarks.json",
                "validation/solver_environment_profiles.json",
                "validation/meep/meep_micro_benchmark_2026-05-20.md",
                "validation/meep/meep_validation_pilot_2026-05-14.md",
            ],
            "Meep has a separate approved optional manual PyMeep/FDTD smoke pass from 2026-05-20.",
        ),
        (
            "mpb_optional_solver_micro_benchmark",
            "optional_manual_solver_validated",
            [
                "docs/solver_validation_micro_benchmarks.md",
                "docs/optional_solver_micro_benchmark_approval_matrix.md",
                "docs/optional_solver_micro_benchmark_readiness_status.md",
                "docs/optional_solver_environment_profiles.md",
                "docs/optional_solver_micro_benchmark_execution_packet.md",
                "docs/optional_solver_execution_sequence.md",
                "validation/solver_validation_micro_benchmarks.json",
                "validation/solver_environment_profiles.json",
                "validation/mpb/mpb_validation_pilot_2026-05-14.md",
            ],
            "MPB has a recorded narrow optional manual validation report.",
        ),
        (
            "optiland_optional_solver_micro_benchmark",
            "optional_manual_solver_validated",
            [
                "docs/solver_validation_micro_benchmarks.md",
                "docs/optional_solver_micro_benchmark_approval_matrix.md",
                "docs/optional_solver_micro_benchmark_readiness_status.md",
                "docs/optional_solver_environment_profiles.md",
                "docs/optional_solver_micro_benchmark_execution_packet.md",
                "docs/optional_solver_execution_sequence.md",
                "validation/solver_validation_micro_benchmarks.json",
                "validation/solver_environment_profiles.json",
                "validation/optiland/optiland_micro_benchmark_2026-05-20.md",
                "docs/optional_solver_approval_records/optiland_micro_benchmark_approval_2026-05-20.md",
                "docs/optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md",
                "validation/optiland/optiland_validation_pilot_2026-05-14.md",
            ],
            "Optiland has a reviewed and accepted optional manual ray/path smoke pass from 2026-05-20.",
        ),
        (
            "elmer_optional_solver_micro_benchmark",
            "documented_preview",
            [
                "docs/solver_validation_micro_benchmarks.md",
                "docs/optional_solver_micro_benchmark_approval_matrix.md",
                "docs/optional_solver_micro_benchmark_readiness_status.md",
                "docs/optional_solver_environment_profiles.md",
                "docs/optional_solver_micro_benchmark_execution_packet.md",
                "docs/optional_solver_execution_sequence.md",
                "validation/solver_validation_micro_benchmarks.json",
                "validation/solver_environment_profiles.json",
                "validation/elmer/elmer_install_deferred_2026-05-15.md",
            ],
            "Elmer remains deferred until a maintainable ElmerSolver install route exists.",
        ),
    ]
    for component_id, maturity_level, evidence_refs, status_note in optional_solver_micro_benchmarks:
        records.append(
            _record(
                area="optional_solver_micro_benchmarks",
                component_id=component_id,
                maturity_level=maturity_level,
                evidence_refs=evidence_refs,
                tests_or_scripts=[
                    "scripts/check_optional_solver_readiness.py",
                    "scripts/run_optional_solver_micro_benchmarks.sh",
                    "tests/test_optional_solver_readiness_script.py",
                    "tests/test_optional_solver_micro_benchmarks_script.py",
                ],
                limitations=[
                    status_note,
                    "Readiness checks detect availability only and do not execute solvers.",
                    "Readiness is profile/environment-specific and can use OSA_SOLVER_PYTHON for import-only probes.",
                    "Only the recorded Gmsh, Optiland, and Meep runs were explicitly approved and executed; MPB and Elmer remain pending/deferred.",
                    "The Meep optional micro-benchmark used OSA_SOLVER_PYTHON and records PyMeep/FDTD smoke evidence only.",
                    "Optional solver-backed micro-benchmarks require explicit opt-in.",
                    "Default pytest, smoke, release gates, and quality gates do not run solvers.",
                    "No production-grade physical validation or formal convergence proof is claimed.",
                ],
                external_solver_required=True,
            )
        )

    return records


def build_backend_validation_maturity_summary() -> BackendValidationMaturityResponse:
    """Build the backend validation maturity summary for reports and API."""

    records = build_backend_validation_maturity_records()
    by_level = Counter(record.maturity_level for record in records)
    by_area = Counter(record.area for record in records)
    return BackendValidationMaturityResponse(
        records=records,
        summary={
            "record_count": len(records),
            "areas": sorted(by_area),
            "levels": sorted(by_level),
            "by_area": dict(sorted(by_area.items())),
            "by_level": dict(sorted(by_level.items())),
            "calculator_maturity_level": "sanity_checked_preview",
            "application_domain_maturity_level": "benchmark_checked_preview",
            "adapter_source_monitor_maturity_level": "fixture_guarded_preview",
            "material_maturity_level": "documented_preview_user_must_verify",
            "optional_solver_micro_benchmark_default": "no_solver_execution",
            "optional_solver_micro_benchmarks_opt_in_required": True,
            "optional_solver_readiness_available": True,
            "optional_solver_approval_matrix_available": True,
            "optional_solver_environment_profiles_available": True,
            "optional_solver_execution_approval_packet_available": True,
            "optional_solver_approval_records_present": True,
            "optional_solver_execution_default": False,
            "explicit_solver_approval_required": True,
            "all_optional_solver_execution_authorized": False,
            "gmsh_optional_micro_benchmark_status": "passed_2026-05-20",
            "gmsh_optional_micro_benchmark_review_status": "accepted_as_optional_manual_mesh_generation_smoke_evidence",
            "optiland_optional_micro_benchmark_status": "passed_2026-05-20",
            "optiland_optional_micro_benchmark_review_status": "accepted_as_optional_manual_ray_path_smoke_evidence",
            "meep_optional_micro_benchmark_decision_packet_available": True,
            "meep_optional_micro_benchmark_status": "passed_2026-05-20",
            "meep_optional_micro_benchmark_readiness_profile": "osa-solvers_import_only",
            "next_optional_solver_candidate": "mpb_requires_osa_solver_python_not_approved",
            "elmer_micro_benchmark_status": "deferred",
        },
        preview_boundary_summary={
            "calculators": (
                "Sanity-checked preview/design-assist calculators; physical "
                "validation remains user responsibility."
            ),
            "materials": (
                "Local curated preview catalog; not a production-grade optical "
                "constants database."
            ),
            "adapters": (
                "Adapter-native source/monitor mappings are preview metadata; "
                "real results require explicit solver execution."
            ),
            "application_domains": (
                "Benchmarks verify deterministic routing, missing-input "
                "diagnostics, and blocked actions, not physical correctness."
            ),
            "sub_agents": (
                "Sub-agent traces show deterministic local role execution, not "
                "independent autonomous services."
            ),
            "pypi": "PyPI publication would not imply production-grade validation.",
            "optional_solver_micro_benchmarks": (
                "Open-source solver-backed micro-benchmarks are optional/manual/"
                "explicit opt-in only; readiness checks detect availability only, "
                "can be calibrated with OSA_SOLVER_PYTHON for solver-specific "
                "Python profiles, include pending/deferred per-solver approval "
                "records and one-solver-at-a-time sequencing, record the Gmsh-only "
                "optional manual micro-benchmark pass from 2026-05-20 as reviewed "
                "mesh-generation smoke evidence, record the separately approved "
                "Optiland-only pass from 2026-05-20 as reviewed ray/path smoke evidence, "
                "record the separately approved Meep-only pass from 2026-05-20 "
                "as optional manual PyMeep/FDTD smoke evidence through "
                "OSA_SOLVER_PYTHON, keep MPB unapproved pending "
                "OSA_SOLVER_PYTHON-specific approval, "
                "and default gates do not run solvers."
            ),
        },
    )
