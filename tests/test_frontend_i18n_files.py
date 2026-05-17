from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend" / "src"


def test_frontend_i18n_files_and_language_switcher_exist():
    assert (FRONTEND / "i18n" / "en.ts").exists()
    assert (FRONTEND / "i18n" / "zhCN.ts").exists()
    assert (FRONTEND / "i18n" / "useI18n.tsx").exists()
    assert (FRONTEND / "components" / "LanguageSwitcher.tsx").exists()
    assert (ROOT / "docs" / "frontend_i18n_zh_CN.md").exists()

    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            FRONTEND / "i18n" / "types.ts",
            FRONTEND / "i18n" / "useI18n.tsx",
            FRONTEND / "components" / "LanguageSwitcher.tsx",
        ]
    )
    assert "agent-studio-language" in source
    assert "localStorage" in source
    assert "navigator.language" in source


def test_chinese_localization_doc_records_contract_boundaries():
    text = (ROOT / "docs" / "frontend_i18n_zh_CN.md").read_text(encoding="utf-8")
    required = [
        "Agent Studio 支持 English / 中文",
        "API 字段名保持英文稳定",
        "agent-studio-language",
        "默认不执行外部求解器",
        "默认不调用外部 LLM",
        "预览产物不代表生产级物理验证",
        "不声明形式化收敛证明",
        "API JSON keys",
        "adapter tool names",
        "api_contract_version",
    ]
    for phrase in required:
        assert phrase in text


def test_i18n_dictionaries_preserve_english_and_chinese_safety_copy():
    english = (FRONTEND / "i18n" / "en.ts").read_text(encoding="utf-8")
    chinese = (FRONTEND / "i18n" / "zhCN.ts").read_text(encoding="utf-8")

    for phrase in [
        "No solver is executed by default.",
        "No external LLM is called by default.",
        "Preview artifacts are not production-grade physical validation.",
        "Formal convergence proof is not claimed.",
        "This UI does not control PyPI/TestPyPI publication or GitHub releases.",
    ]:
        assert phrase in english

    for phrase in [
        "默认不执行外部求解器",
        "默认不调用外部 LLM",
        "预览产物不代表生产级物理验证",
        "不声明形式化收敛证明",
        "本界面不控制 PyPI/TestPyPI 上传",
        "本演示是本地优先、同步、预览优先的 Agent Studio",
    ]:
        assert phrase in chinese
