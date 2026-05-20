"""Optional solver approval record template tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_optional_solver_approval_record_templates_require_phrase_and_exclusions():
    required_phrase = (
        "I approve running the optional <solver> micro-benchmark for optical-spec-agent."
    )
    paths = [
        ROOT / "docs" / "optional_solver_micro_benchmark_approval_record_template.md",
        ROOT / "docs" / "optional_solver_micro_benchmark_approval_record_template.zh-CN.md",
    ]
    for path in paths:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert required_phrase in text
        for phrase in [
            "PyPI publication: not approved",
            "TestPyPI upload: not approved",
            "Tag or GitHub release creation: not approved",
            "`v1.0.0` release: not approved",
        ]:
            assert phrase in text
        assert "no production-grade" in text.lower() or "Production-grade" in text
        assert "Expected Command" in text or "预期命令" in text
        assert "Expected Output" in text or "预期输出" in text

