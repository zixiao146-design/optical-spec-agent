from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_frontend_mvp_files_exist_and_scripts_are_defined():
    assert (FRONTEND / "package.json").exists()
    assert (FRONTEND / "src" / "App.tsx").exists()
    assert (FRONTEND / "src" / "api" / "client.ts").exists()
    assert (FRONTEND / "src" / "api" / "types.ts").exists()

    package_json = _read(FRONTEND / "package.json")
    assert '"dev"' in package_json
    assert '"build"' in package_json
    assert '"typecheck"' in package_json


def test_frontend_source_has_no_release_or_upload_controls():
    source = "\n".join(
        _read(path)
        for path in (FRONTEND / "src").rglob("*")
        if path.suffix in {".ts", ".tsx", ".css"}
    )
    forbidden_control_phrases = [
        "twine upload",
        "gh release create",
        "git tag",
        "create release",
        "publish package",
        "upload package",
        "external llm provider",
        "Run solver",
        "Execute solver",
        "Upload to PyPI",
        "Upload to TestPyPI",
        "Create tag",
        "Create release",
    ]
    for phrase in forbidden_control_phrases:
        assert phrase not in source
    assert "No solver run" in source
    assert "No external LLM" in source


def test_frontend_generated_artifacts_are_not_present():
    assert not (FRONTEND / "node_modules").exists()
    assert not (FRONTEND / "dist").exists()
    assert not (FRONTEND / "build").exists()
