"""GitHub Actions workflow guardrails for operations readiness."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"


def _workflow_files() -> list[Path]:
    if not WORKFLOW_DIR.exists():
        return []
    return sorted(path for path in WORKFLOW_DIR.iterdir() if path.is_file())


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
