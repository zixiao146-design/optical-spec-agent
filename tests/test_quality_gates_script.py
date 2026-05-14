"""Quality gate script safety and coverage checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_quality_gates_script_exists_and_runs_expected_local_gates():
    script = ROOT / "scripts" / "run_quality_gates.sh"
    assert script.exists()
    text = script.read_text(encoding="utf-8")
    assert "NO UPLOAD PERFORMED" in text
    assert "NO GMSH EXECUTION PERFORMED" in text
    assert "NO MEEP EXECUTION PERFORMED" in text
    assert "NO SOLVER EXECUTION PERFORMED" in text
    assert "NO TAG CREATED" in text
    assert "NO RELEASE CREATED" in text
    assert "testpypi_preflight.sh" in text
    assert "open_solver_validation_preflight.sh" in text
    assert "run_optional_gmsh_validation.sh" in text
    assert "run_optional_meep_validation.sh" in text
    assert "OSA_RUN_OPTIONAL_GMSH_VALIDATION=1" not in text
    assert "OSA_RUN_OPTIONAL_MEEP_VALIDATION=1" not in text
    assert "smoke_release.sh" in text
    assert "-m pytest" in text
    assert "-m build" in text
    assert "OSA_QUALITY_TEST_VENV" in text
    assert "make check" in text
    assert "optical-spec --help" in text
    assert "optical-spec adapter-list --json" in text
    assert "optical-spec workflow-plan examples/e2e/local_optical_workflow.json --json" in text
    assert (ROOT / "docs" / "quality_gates.md").exists()
    assert (ROOT / "docs" / "ci_quality_gate_parity.md").exists()
    assert (ROOT / "docs" / "release_dry_run_operations.md").exists()
    assert (ROOT / "docs" / "open_solver_validation_harness.md").exists()


def test_quality_gates_script_contains_no_publish_tag_or_release_commands():
    text = (ROOT / "scripts" / "run_quality_gates.sh").read_text(encoding="utf-8").lower()
    forbidden = [
        "twine upload",
        "python -m twine upload",
        "gh release create",
        "git push",
        "git tag",
    ]
    for phrase in forbidden:
        assert phrase not in text


def test_makefile_exposes_no_upload_quality_targets():
    makefile = (ROOT / "Makefile").read_text(encoding="utf-8")
    assert "quality:" in makefile
    assert "./scripts/run_quality_gates.sh" in makefile
    assert "testpypi-preflight:" in makefile
    assert "./scripts/testpypi_preflight.sh" in makefile
