from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
I18N = ROOT / "frontend" / "src" / "i18n"


def test_chinese_dictionary_contains_core_pages_and_safety_boundaries():
    chinese = (I18N / "zhCN.ts").read_text(encoding="utf-8")
    required = [
        "仪表盘",
        "规格输入",
        "适配器矩阵",
        "工作流计划",
        "适配器预览",
        "验证证据",
        "系统状态",
        "默认不执行外部求解器",
        "默认不调用外部 LLM",
        "不声明形式化收敛证明",
        "不控制 PyPI/TestPyPI 上传",
        "中文手把手教程",
        "开始中文教程",
        "打开 Agent Studio",
        "加载中文纳米颗粒示例",
        "查看验证证据和下一步建议",
    ]
    for phrase in required:
        assert phrase in chinese


def test_english_dictionary_still_contains_core_page_labels():
    english = (I18N / "en.ts").read_text(encoding="utf-8")
    for phrase in [
        "Dashboard",
        "Spec Input",
        "Adapter Matrix",
        "Workflow Plan",
        "Artifact Preview",
        "Validation Evidence",
        "System Status",
    ]:
        assert phrase in english
