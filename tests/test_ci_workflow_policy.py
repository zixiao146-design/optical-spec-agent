"""GitHub Actions workflow guardrails for operations readiness."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"


def _workflow_files() -> list[Path]:
    if not WORKFLOW_DIR.exists():
        return []
    return sorted(path for path in WORKFLOW_DIR.iterdir() if path.is_file())


def _read_workflow(name: str) -> str:
    return (WORKFLOW_DIR / name).read_text(encoding="utf-8")


def _is_automatic_workflow(text: str) -> bool:
    return "push:" in text or "pull_request:" in text


def test_workflows_are_documented_in_ci_quality_parity_inventory():
    docs = (ROOT / "docs" / "ci_quality_gate_parity.md").read_text(encoding="utf-8")
    for path in _workflow_files():
        assert path.name in docs


def test_default_workflows_do_not_publish_tag_or_release():
    forbidden_default = [
        "twine upload",
        "python -m twine upload",
        "git tag",
        "git push origin v",
    ]
    for path in _workflow_files():
        text = path.read_text(encoding="utf-8")
        lowered = text.lower()
        is_manual = "workflow_dispatch" in lowered

        if "gh release create" in lowered:
            assert is_manual, f"{path.name} creates a release outside manual dispatch"
            assert (
                "CREATE_PRERELEASE" in text
            ), f"{path.name} must require explicit release confirmation"
            continue

        for phrase in forbidden_default:
            assert phrase not in lowered, f"{path.name} contains default publish/tag command: {phrase}"


def test_workflow_secret_mentions_are_backed_by_token_hygiene_policy():
    combined = "\n".join(path.read_text(encoding="utf-8") for path in _workflow_files())
    policy = ROOT / "docs" / "secrets_and_token_hygiene.md"
    assert policy.exists()
    if "secrets." in combined or "github.token" in combined:
        text = policy.read_text(encoding="utf-8")
        assert "Never paste tokens into chat" in text
        assert "Never commit tokens" in text
        assert "Release creation tasks may require a GitHub token" in text


def test_workflows_do_not_require_proprietary_solvers():
    proprietary_names = ["Zemax", "Lumerical", "COMSOL", "proprietary Ansys"]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in _workflow_files())
    for name in proprietary_names:
        assert name not in combined


def test_automatic_ci_workflows_match_local_dependency_baseline():
    for path in _workflow_files():
        text = path.read_text(encoding="utf-8")
        if not _is_automatic_workflow(text):
            continue

        assert 'python-version: "3.11"' in text, f"{path.name} should pin Python 3.11"
        assert "3.12" not in text, f"{path.name} should not run the old Python 3.12 matrix"
        assert '.[test]' in text, f"{path.name} should install the test extra"
        assert '.[dev]' not in text, f"{path.name} should not depend on the dev extra in CI"


def test_ci_workflow_runs_build_tests_and_cli_examples_without_uploading():
    text = _read_workflow("ci.yml")
    lowered = text.lower()
    assert "push:" in text
    assert "pull_request:" in text
    assert 'python-version: "3.11"' in text
    assert '.[test]' in text
    assert "python -m pytest" in text
    assert "python -m build" in text
    assert "optical-spec --help" in text
    assert "optical-spec adapter-list --json" in text
    assert "optical-spec validate examples/specs/minimal_nanoparticle.json" in text
    assert "optical-spec parse examples/specs/minimal_nanoparticle.json --json" in text
    assert (
        "optical-spec workflow-plan examples/workflows/local_preview_request.json --json"
        in text
    )
    assert "twine upload" not in lowered
    assert "gh release create" not in lowered
    assert "git tag" not in lowered


def test_test_workflow_is_manual_extended_benchmark_workflow():
    text = _read_workflow("test.yml")
    lowered = text.lower()
    assert "name: Benchmarks and Extended Tests" in text
    assert "workflow_dispatch:" in text
    assert "push:" not in text
    assert "pull_request:" not in text
    assert 'python-version: "3.11"' in text
    assert '.[test]' in text
    assert "mkdir -p outputs outputs/workflow_benchmark" in text
    assert "python -m pytest" in text
    assert "python benchmarks/run_benchmark.py --mode key_fields" in text
    assert "python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json" in text
    assert "python benchmarks/run_llm_benchmark.py" in text
    assert "python benchmarks/run_workflow_benchmark.py" in text
    assert "actions/upload-artifact" in text
    assert "twine upload" not in lowered
    assert "gh release create" not in lowered
    assert "git tag" not in lowered


def test_workflows_do_not_enable_optional_solver_or_llm_execution_by_default():
    combined = "\n".join(path.read_text(encoding="utf-8") for path in _workflow_files())
    forbidden_env = [
        "OSA_RUN_OPTIONAL_GMSH_VALIDATION=1",
        "OSA_RUN_OPTIONAL_MEEP_VALIDATION=1",
        "OSA_RUN_OPTIONAL_MPB_VALIDATION=1",
        "OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1",
        "OSA_RUN_OPTIONAL_ELMER_VALIDATION=1",
        "OSA_ENABLE_EXTERNAL_LLM=1",
    ]
    for phrase in forbidden_env:
        assert phrase not in combined


def test_release_and_publish_workflows_are_manual_and_scoped():
    release_dry_run = _read_workflow("release-dry-run.yml")
    assert "workflow_dispatch:" in release_dry_run
    assert "push:" not in release_dry_run
    assert "pull_request:" not in release_dry_run
    assert "python -m twine check dist/*" in release_dry_run
    assert "twine upload" not in release_dry_run.lower()
    assert "gh release create" not in release_dry_run.lower()
    assert "git tag" not in release_dry_run.lower()

    create_prerelease = _read_workflow("create-prerelease.yml")
    assert "name: Create Historical v0.9.0rc1 Pre-release" in create_prerelease
    assert "workflow_dispatch:" in create_prerelease
    assert "push:" not in create_prerelease
    assert "pull_request:" not in create_prerelease
    assert "CREATE_PRERELEASE" in create_prerelease
    assert "Historical helper" in create_prerelease

    testpypi = _read_workflow("testpypi-trusted-publish.yml")
    assert "workflow_dispatch:" in testpypi
    assert "UPLOAD_TESTPYPI" in testpypi
    assert "id-token: write" in testpypi
    assert "repository-url: https://test.pypi.org/legacy/" in testpypi
    assert "password:" not in testpypi.lower()


def test_workflow_docs_state_no_default_upload_or_release():
    combined = "\n".join(
        [
            (ROOT / "docs" / "ci_quality_gate_parity.md").read_text(encoding="utf-8"),
            (ROOT / "docs" / "release_dry_run_operations.md").read_text(encoding="utf-8"),
        ]
    )
    assert "never upload PyPI/TestPyPI" in combined
    assert "never create tags or GitHub releases from default CI" in combined
    assert "no GitHub release creation" in combined
    assert "no PyPI/TestPyPI upload" in combined
