from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_quickstart_docs_exist_and_preserve_safety_boundaries():
    english = ROOT / "docs" / "quickstart.md"
    chinese = ROOT / "docs" / "quickstart.zh-CN.md"
    assert english.exists()
    assert chinese.exists()
    combined = english.read_text(encoding="utf-8") + "\n" + chinese.read_text(encoding="utf-8")
    required = [
        "bootstrap_demo_env.sh",
        "run_quickstart_demo.sh",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:8000/docs",
        "Load example spec",
        "Parse locally",
        "Validate",
        "View adapter matrix",
        "Generate workflow plan",
        "Preview artifact",
        "Review validation evidence",
        "Readiness / next actions",
        "English / 中文切换",
        "中文手把手教程",
        "docs/agent_studio_chinese_guided_tutorial.md",
        "docs/frontend_chinese_terminology.md",
        "加载中文纳米颗粒示例",
        "本地解析",
        "验证规格",
        "examples/quickstart/zh_nanoparticle_prompt.txt",
        "No solver executed",
        "No external LLM called",
        "Does not publish PyPI/TestPyPI",
        "Does not create tags/releases",
        "production-grade physical validation",
        "formal convergence proof",
    ]
    for phrase in required:
        assert phrase in combined
