from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_chinese_quickstart_examples_and_docs_exist():
    prompt = ROOT / "examples" / "quickstart" / "zh_nanoparticle_prompt.txt"
    notes = ROOT / "examples" / "quickstart" / "zh_quickstart_notes.md"
    assert prompt.exists()
    assert notes.exists()
    assert "银纳米颗粒" in prompt.read_text(encoding="utf-8")
    assert "默认不运行外部求解器" in prompt.read_text(encoding="utf-8")
    assert "不调用外部 LLM" in prompt.read_text(encoding="utf-8")

    zh_quickstart = (ROOT / "docs" / "quickstart.zh-CN.md").read_text(encoding="utf-8")
    readme_zh = (ROOT / "README.zh-CN.md").read_text(encoding="utf-8")
    notes_text = notes.read_text(encoding="utf-8")

    assert "English / 中文切换" in zh_quickstart
    assert "中文 guided demo" in zh_quickstart
    assert "examples/quickstart/zh_nanoparticle_prompt.txt" in zh_quickstart
    assert "Agent Studio 前端支持 English / 中文界面切换" in readme_zh
    assert "docs/frontend_i18n_zh_CN.md" in readme_zh
    for phrase in [
        "不访问网络",
        "不运行外部求解器",
        "不调用外部 LLM",
        "不执行 PyPI/TestPyPI 上传",
        "不创建 GitHub tag 或 release",
    ]:
        assert phrase in notes_text
