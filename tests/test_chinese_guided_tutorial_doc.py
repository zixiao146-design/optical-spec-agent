from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_chinese_guided_tutorial_doc_has_safe_agent_workflow_steps():
    path = ROOT / "docs" / "agent_studio_chinese_guided_tutorial.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    required_steps = [
        "打开 Agent Studio",
        "查看 readiness / 系统状态",
        "查看示例库",
        "加载中文纳米颗粒示例",
        "本地解析规格",
        "验证规格",
        "查看适配器矩阵",
        "查看材料库和材料建议",
        "查看多智能体协作轨迹",
        "生成工作流计划",
        "预览适配器产物",
        "查看验证证据和下一步建议",
    ]
    for step in required_steps:
        assert step in text
    for phrase in [
        "用户操作",
        "预期看到的结果",
        "使用的 API endpoint",
        "安全边界说明",
        "POST /api/parse",
        "POST /api/validate",
        "GET /api/examples",
        "POST /api/examples/{example_id}/agent-trace",
        "POST /api/workflow-plan",
        "POST /api/adapter-preview",
        "不默认运行 solver",
        "不默认调用外部 LLM",
        "不上传 PyPI/TestPyPI",
        "不创建 tag/release",
    ]:
        assert phrase in text
