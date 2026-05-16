from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"


def test_frontend_global_safety_copy_is_visible_and_specific():
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (FRONTEND / "src").rglob("*")
        if path.suffix in {".ts", ".tsx"}
    )
    required = [
        "No solver is executed by default.",
        "No external LLM is called by default.",
        "Preview artifacts are not production-grade physical validation.",
        "Formal convergence proof is not claimed.",
        "This UI does not control PyPI/TestPyPI publication or GitHub releases.",
        "not live validation",
    ]
    for phrase in required:
        assert phrase in source


def test_frontend_keeps_publication_release_and_solver_controls_absent():
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in (FRONTEND / "src").rglob("*")
        if path.suffix in {".ts", ".tsx", ".css"}
    ).lower()
    forbidden = [
        "twine upload",
        "gh release create",
        "git tag",
        "upload to pypi",
        "upload to testpypi",
        "create tag",
        "create release",
        "run solver",
        "execute solver",
        "external llm provider",
    ]
    for phrase in forbidden:
        assert phrase not in source
