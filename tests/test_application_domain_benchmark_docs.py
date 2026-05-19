"""Application-domain benchmark documentation tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_application_domain_benchmark_docs_exist_and_bound_claims():
    for rel in [
        "docs/application_domain_benchmarks.md",
        "docs/application_domain_benchmarks.zh-CN.md",
        "docs/domain_benchmark_results_policy.md",
        "docs/domain_benchmark_results_policy.zh-CN.md",
    ]:
        path = ROOT / rel
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "preview" in text.lower()
        assert "positive" in text or "明确" in text
        assert "ambiguous" in text or "歧义" in text
        assert "underconstrained" in text or "输入不足" in text
        assert "unsupported" in text or "不支持" in text
        assert "production-grade" in text or "生产级" in text
        assert "formal convergence" in text or "形式化收敛" in text
