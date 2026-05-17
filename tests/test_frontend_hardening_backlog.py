from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_frontend_hardening_backlog_prioritizes_work_and_keeps_boundaries():
    path = ROOT / "docs" / "frontend_hardening_backlog.md"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    required = [
        "P0 Must Fix Before Public Demo",
        "P1 Important Polish",
        "P2 Future Enhancement",
        "Deferred / Non-goals",
        "Capture concrete maintainer demo observations",
        "API disconnected/demo fixture mode",
        "No upload controls",
        "No tag/release controls",
        "No default solver execution",
        "No default external LLM",
        "No production-grade validation claim",
        "No formal convergence proof claim",
        "Elmer Level 3 validation remains deferred",
        "PyPI published: no",
        "v0.9.0rc7 tag: not created",
        "v1.0.0 tag: not created",
    ]
    for phrase in required:
        assert phrase in text
