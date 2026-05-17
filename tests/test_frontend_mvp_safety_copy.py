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
        "默认不执行外部求解器",
        "默认不调用外部 LLM",
        "预览产物不代表生产级物理验证",
        "不声明形式化收敛证明",
        "本界面不控制 PyPI/TestPyPI 上传",
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
        "external llm provider",
    ]
    for phrase in forbidden:
        assert phrase not in source
