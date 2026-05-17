from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"


def _read(relative: str) -> str:
    return (FRONTEND / relative).read_text(encoding="utf-8")


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
    )
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

    assert "Load example spec" in spec_page
    assert "Load fixture" in spec_page
    assert "Load workflow fixture" in workflow_page
    assert "Load minimal spec" in preview_page
    assert "Demo fixture loaded - not live validation until submitted." in _read("src/fixtures/demoData.ts")
    assert "ApiModeIndicator" in dashboard_page
    assert "ApiModeIndicator" in system_status_page
    assert "DiagnosticsPanel" in spec_page + workflow_page + preview_page
    assert "RecommendedActions" in spec_page + workflow_page + preview_page + dashboard_page


def test_workflow_and_preview_ergonomics_keep_safety_copy():
    workflow_page = _read("src/pages/WorkflowPlanPage.tsx")
    preview_page = _read("src/pages/ArtifactPreviewPage.tsx")
    json_panel = _read("src/components/JsonPanel.tsx")

    assert "No solver is executed by default." in workflow_page
    assert "No solver is executed by default." in preview_page
    assert "Preview-only artifact" in preview_page
    assert "output_language" in _read("src/components/ArtifactPreviewPanel.tsx")
    assert "details open={initiallyOpen}" in json_panel
    assert "No JSON payload is available yet." in json_panel
