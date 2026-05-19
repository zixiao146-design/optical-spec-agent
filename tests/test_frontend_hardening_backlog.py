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
        "Chinese step-by-step tutorial before any public demo",
        "Chinese tutorial entry in the frontend",
        "Per-step operation instructions",
        "Per-step expected results",
        "Per-step API endpoint reference",
        "Per-step safety boundary",
        "One-click Chinese nanoparticle example loading",
        "待进一步 demo 反馈确认",
        "Do not invent page-by-page issues",
        "No upload controls",
        "No tag/release controls",
        "No default solver execution",
        "No default external LLM",
        "No production-grade validation claim",
        "No formal convergence proof claim",
        "Elmer Level 3 validation remains deferred",
        "PyPI published: no",
        "v0.9.0rc8 tag: not created",
        "v1.0.0 tag: not created",
    ]
    for phrase in required:
        assert phrase in text
