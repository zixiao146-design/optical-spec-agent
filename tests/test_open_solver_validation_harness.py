"""Open-source solver validation harness documentation checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_open_solver_validation_harness_docs_exist_and_stay_optional():
    harness = ROOT / "docs" / "open_solver_validation_harness.md"
    template = ROOT / "docs" / "manual_solver_validation_report_template.md"
    marker_policy = ROOT / "docs" / "pytest_marker_policy.md"
    plan = ROOT / "docs" / "open_source_solver_validation_plan.md"
    micro_doc = ROOT / "docs" / "solver_validation_micro_benchmarks.md"
    micro_manifest = ROOT / "validation" / "solver_validation_micro_benchmarks.json"
    micro_script = ROOT / "scripts" / "run_optional_solver_micro_benchmarks.sh"

    for path in [harness, template, marker_policy, plan, micro_doc, micro_manifest, micro_script]:
        assert path.exists()

    harness_text = harness.read_text(encoding="utf-8")
    assert "does not run solvers" in harness_text
    assert "Candidate availability does not mean validation was run" in harness_text
    assert "An unavailable solver does not fail default tests" in harness_text
    assert "no production-grade physical validation claim" in harness_text
    assert "Gmsh optional validation pilot" in harness_text
    assert "does not run Gmsh unless explicitly enabled" in harness_text
    assert "validation/gmsh/gmsh_validation_pilot_2026-05-14.md" in harness_text
    assert "validation/meep/meep_validation_pilot_2026-05-14.md" in harness_text
    assert "validation/mpb/mpb_validation_pilot_2026-05-14.md" in harness_text
    assert "validation/optiland/optiland_validation_pilot_2026-05-14.md" in harness_text
    assert "docs/elmer_level3_readiness.md" in harness_text
    assert "scripts/run_optional_elmer_validation.sh" in harness_text
    assert "no completed Elmer manual validation report exists yet" in harness_text
    assert "validation/elmer/elmer_install_deferred_2026-05-15.md" in harness_text
    assert "Meep opt-in pilot" in harness_text
    assert "MPB opt-in pilot" in harness_text
    assert "Optiland opt-in pilot" in harness_text
    assert "run_optional_solver_micro_benchmarks.sh" in harness_text
    assert "default no-execute" in harness_text
    assert "production-grade physical validation" in harness_text
    assert "not a default dependency" in harness_text

    template_text = template.read_text(encoding="utf-8")
    assert "does not by itself imply production-grade validation" in template_text
    assert "Manual validation is optional and not part of default CI" in template_text
    assert "gmsh_validation_pilot_template.md" in template_text
    assert "mpb_validation_report_schema.json" in template_text
    assert "optiland_validation_report_schema.json" in template_text
    assert "elmer_validation_report_schema.json" in template_text

    marker_text = marker_policy.read_text(encoding="utf-8")
    assert "Default tests must remain offline and no-solver" in marker_text
    assert "Default `pytest` remains no-solver" in marker_text
    assert "Proprietary solver tests are not default tests" in marker_text
    assert "OSA_RUN_OPTIONAL_GMSH_VALIDATION=1" in marker_text
    assert "OSA_RUN_OPTIONAL_MEEP_VALIDATION=1" in marker_text
    assert "OSA_RUN_OPTIONAL_MPB_VALIDATION=1" in marker_text
    assert "OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1" in marker_text
    assert "OSA_RUN_OPTIONAL_ELMER_VALIDATION=1" in marker_text

    plan_text = plan.read_text(encoding="utf-8")
    assert "records availability only" in plan_text
    assert "first pilot-ready candidate is Gmsh" in plan_text
    assert "docs/gmsh_level3_readiness.md" in plan_text
    assert "docs/meep_level3_readiness.md" in plan_text
    assert "validation/meep/meep_validation_pilot_2026-05-14.md" in plan_text
    assert "docs/mpb_level3_readiness.md" in plan_text
    assert "validation/mpb/mpb_validation_pilot_2026-05-14.md" in plan_text
    assert "docs/optiland_level3_readiness.md" in plan_text
    assert "validation/optiland/optiland_validation_pilot_2026-05-14.md" in plan_text
    assert "docs/elmer_level3_readiness.md" in plan_text
    assert "scripts/run_optional_elmer_validation.sh" in plan_text
    assert "no Elmer execution or completed report exists yet" in plan_text
    assert "validation/elmer/elmer_install_deferred_2026-05-15.md" in plan_text
    assert "Tests should not be part of default `pytest`" in plan_text
    assert "Marker policy is documented in `docs/pytest_marker_policy.md`" in plan_text
    assert "solver_validation_micro_benchmarks.md" in plan_text
    assert "run_optional_solver_micro_benchmarks.sh" in plan_text

    micro_text = micro_doc.read_text(encoding="utf-8")
    assert "explicit opt-in" in micro_text
    assert "pytest does not run solvers by default" in micro_text
    assert "Elmer remains deferred" in micro_text
    script_text = micro_script.read_text(encoding="utf-8")
    assert "NO SOLVER EXECUTION PERFORMED BY DEFAULT" in script_text
