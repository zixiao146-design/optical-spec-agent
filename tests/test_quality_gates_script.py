"""Quality gate script safety and coverage checks."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_quality_gates_script_exists_and_runs_expected_local_gates():
    script = ROOT / "scripts" / "run_quality_gates.sh"
    assert script.exists()
    text = script.read_text(encoding="utf-8")
    assert "NO UPLOAD PERFORMED" in text
    assert "NO TAG CREATED" in text
    assert "NO RELEASE CREATED" in text
    assert "testpypi_preflight.sh" in text
    assert "smoke_release.sh" in text
    assert "python -m pytest" in text
    assert "python -m build" in text
    assert "make check" in text
    assert "optical-spec --help" in text
    assert "optical-spec adapter-list --json" in text
    assert "optical-spec workflow-plan examples/e2e/local_optical_workflow.json --json" in text


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

