"""Missing-input diagnostics documentation tests."""

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_missing_input_diagnostics_docs_exist_and_document_boundaries():
    for path in [
        ROOT / "docs" / "missing_input_diagnostics.md",
        ROOT / "docs" / "missing_input_diagnostics.zh-CN.md",
    ]:
        text = path.read_text(encoding="utf-8")
        assert "critical" in text or "关键" in text
        assert "optional" in text or "可选" in text
        assert "safe_to_run_solver=false" in text
        assert "production-grade" in text or "生产级" in text
