from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend" / "src"


def test_frontend_guided_demo_contains_all_steps_and_boundaries():
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in FRONTEND.rglob("*")
        if path.suffix in {".ts", ".tsx"}
    )
    required = [
        "GuidedDemoStepper",
        "ChineseGuidedTutorial",
        "QuickstartPanel",
        "Start guided demo",
        "Load example spec",
        "Parse locally",
        "Validate spec",
        "Review adapter matrix",
        "Generate workflow plan",
        "Preview artifact",
        "Review validation evidence",
        "Review readiness / next action",
        "API connected",
        "api_contract_version 0.1",
        "No solver is executed by default",
        "No external LLM is called by default",
        "Preview artifacts are not production-grade physical validation",
        "Formal convergence proof is not claimed",
        "This UI does not control PyPI/TestPyPI publication or GitHub releases",
        "加载示例规格",
        "本地解析",
        "验证规格",
        "查看适配器矩阵",
        "生成工作流计划",
        "预览适配器产物",
        "查看验证证据",
        "查看 readiness / 下一步建议",
        "中文手把手教程",
        "加载中文纳米颗粒示例",
        "查看验证证据和下一步建议",
    ]
    for phrase in required:
        assert phrase in source
    forbidden = [
        "twine upload",
        "gh release create",
        "git tag",
        "Upload to PyPI",
        "Upload to TestPyPI",
        "Create tag",
        "Create release",
        "Run solver",
        "External LLM provider",
    ]
    for phrase in forbidden:
        assert phrase not in source
