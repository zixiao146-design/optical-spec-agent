from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_source_monitor_docs_exist_and_document_preview_boundary():
    docs = [
        ROOT / "docs" / "optical_language_source_monitor.md",
        ROOT / "docs" / "optical_language_source_monitor.zh-CN.md",
        ROOT / "docs" / "source_monitor_missing_input_diagnostics.md",
        ROOT / "docs" / "source_monitor_missing_input_diagnostics.zh-CN.md",
    ]
    for path in docs:
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "source" in text.lower() or "光源" in text
        assert "monitor" in text.lower() or "监测" in text
        assert "preview" in text.lower()
        assert "solver" in text.lower() or "求解器" in text
        assert "production-grade" in text.lower() or "生产级" in text


def test_source_monitor_docs_list_core_types_and_diagnostics():
    text = (ROOT / "docs" / "optical_language_source_monitor.md").read_text(
        encoding="utf-8"
    )
    for phrase in [
        "plane_wave",
        "gaussian_beam",
        "mode_source",
        "scattering_spectrum",
        "reflectance_transmittance",
        "focal_spot",
        "band_structure",
    ]:
        assert phrase in text

    diagnostics = (ROOT / "docs" / "source_monitor_missing_input_diagnostics.md").read_text(
        encoding="utf-8"
    )
    assert "safe_to_preview" in diagnostics
    assert "safe_to_run_solver" in diagnostics
    assert "optical_language.infer_source_monitor" in diagnostics
    assert "optical_language.diagnose_missing_inputs" in diagnostics
