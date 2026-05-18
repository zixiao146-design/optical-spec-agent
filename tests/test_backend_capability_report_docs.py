"""Backend capability report docs tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_backend_capability_report_docs_exist_and_describe_reality():
    for doc in [
        ROOT / "docs" / "backend_capability_report.md",
        ROOT / "docs" / "backend_capability_report.zh-CN.md",
    ]:
        assert doc.exists()
        text = doc.read_text(encoding="utf-8")
        assert "backend capability report" in text.lower() or "后端能力报告" in text
        assert "sub-agent" in text.lower() or "子智能体" in text
        assert "tool_call_ledger" in text
        assert "production-grade" in text or "生产级" in text
        assert "formal convergence proof" in text or "形式化收敛证明" in text
        assert "NO SOLVER EXECUTION PERFORMED" in text or "默认不执行外部求解器" in text


def test_design_case_cross_check_docs_exist_and_document_statuses():
    for doc in [
        ROOT / "docs" / "design_case_cross_checks.md",
        ROOT / "docs" / "design_case_cross_checks.zh-CN.md",
    ]:
        assert doc.exists()
        text = doc.read_text(encoding="utf-8")
        assert "thin_film_coating" in text
        assert "waveguide_mode" in text
        assert "lens_raytrace_preview" in text
        assert "pass" in text
        assert "warning" in text
        assert "fail" in text
        assert "No production-grade" in text or "不声明生产级" in text
