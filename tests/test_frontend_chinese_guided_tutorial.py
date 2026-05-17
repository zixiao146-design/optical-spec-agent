from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend" / "src"


def test_frontend_contains_chinese_guided_tutorial_surface():
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in FRONTEND.rglob("*")
        if path.suffix in {".ts", ".tsx"}
    )
    required = [
        "ChineseGuidedTutorial",
        "中文手把手教程",
        "加载中文纳米颗粒示例",
        "示例库",
        "本地解析",
        "验证规格",
        "适配器矩阵",
        "材料库",
        "多智能体协作轨迹",
        "工作流计划",
        "适配器产物",
        "验证证据",
        "下一步建议",
        "GET /api/examples",
        "POST /api/parse",
        "POST /api/validate",
        "POST /api/examples/{example_id}/agent-trace",
        "POST /api/workflow-plan",
        "POST /api/adapter-preview",
        "examples/quickstart/zh_nanoparticle_prompt.txt",
    ]
    for phrase in required:
        assert phrase in source
    forbidden = [
        "twine upload",
        "gh release create",
        "git tag",
        "Upload to PyPI",
        "Upload to TestPyPI",
        "Create release",
        "Run solver",
        "External LLM provider",
    ]
    for phrase in forbidden:
        assert phrase not in source
