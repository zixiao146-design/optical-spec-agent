from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"


def _read(relative: str) -> str:
    return (FRONTEND / relative).read_text(encoding="utf-8")


def _i18n_text() -> str:
    return "\n".join(
        (FRONTEND / "src" / "i18n" / name).read_text(encoding="utf-8")
        for name in ["en.ts", "zhCN.ts"]
    )


def test_frontend_interaction_polish_components_exist():
    for relative in [
        "src/components/DemoModeBanner.tsx",
        "src/components/ApiModeIndicator.tsx",
        "src/components/DiagnosticsPanel.tsx",
        "src/components/RecommendedActions.tsx",
    ]:
        assert (FRONTEND / relative).exists()

    combined = "\n".join(
        _read(relative)
        for relative in [
            "src/components/DemoModeBanner.tsx",
            "src/components/ApiModeIndicator.tsx",
            "src/components/DiagnosticsPanel.tsx",
            "src/components/RecommendedActions.tsx",
        ]
    ) + "\n" + _i18n_text()
    for phrase in [
        "Demo fixture loaded",
        "API connected",
        "API disconnected",
        "Demo fixture mode",
        "API base URL",
        "Diagnostics",
        "Recommended next actions",
    ]:
        assert phrase in combined


def test_frontend_fixture_buttons_and_live_api_clarity_exist():
    spec_page = _read("src/pages/SpecInputPage.tsx")
    workflow_page = _read("src/pages/WorkflowPlanPage.tsx")
    preview_page = _read("src/pages/ArtifactPreviewPage.tsx")
    dashboard_page = _read("src/pages/DashboardPage.tsx")
    system_status_page = _read("src/pages/SystemStatusPage.tsx")
    i18n = _i18n_text()

    assert "Load example spec" in i18n
    assert "Load fixture" in i18n
    assert "Load workflow fixture" in i18n
    assert "Load minimal spec" in i18n
    assert "Demo fixture loaded - not live validation until submitted." in _read("src/fixtures/demoData.ts")
    assert "ApiModeIndicator" in dashboard_page
    assert "ApiModeIndicator" in system_status_page
    assert "DiagnosticsPanel" in spec_page + workflow_page + preview_page
    assert "RecommendedActions" in spec_page + workflow_page + preview_page + dashboard_page


def test_workflow_and_preview_ergonomics_keep_safety_copy():
    workflow_page = _read("src/pages/WorkflowPlanPage.tsx")
    preview_page = _read("src/pages/ArtifactPreviewPage.tsx")
    json_panel = _read("src/components/JsonPanel.tsx")
    i18n = _i18n_text()

    assert "No solver is executed by default." in i18n
    assert "Preview-only artifact" in i18n
    assert "output_language" in _read("src/components/ArtifactPreviewPanel.tsx")
    assert "details open={initiallyOpen}" in json_panel
    assert "No JSON payload is available yet." in i18n
    assert "state.emptyJson" in json_panel
