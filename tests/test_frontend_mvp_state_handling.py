from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "frontend"


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_frontend_state_components_and_demo_fixtures_exist():
    for relative in [
        "src/api/state.ts",
        "src/components/LoadingState.tsx",
        "src/components/EmptyState.tsx",
        "src/components/ErrorState.tsx",
        "src/components/SafetyNotice.tsx",
        "src/components/ApiDisconnectedNotice.tsx",
        "src/components/ApiModeIndicator.tsx",
        "src/components/DemoModeBanner.tsx",
        "src/components/DiagnosticsPanel.tsx",
        "src/components/RecommendedActions.tsx",
        "src/fixtures/demoData.ts",
    ]:
        assert (FRONTEND / relative).exists()

    state_text = _read(FRONTEND / "src" / "api" / "state.ts")
    assert "frontend_request_error" in state_text
    assert "invalid_json" in state_text
    assert "external_solver_executed: false" in state_text
    assert "external_llm_required: false" in state_text

    demo_text = _read(FRONTEND / "src" / "fixtures" / "demoData.ts")
    assert "Demo fixture mode: this is not live validation." in demo_text
    assert "Demo fixture loaded - not live validation until submitted." in demo_text
    assert "0.9.0rc7" in demo_text
    assert "v0.9.0rc6" in demo_text
    assert "Level 2 + Level-3-ready" in demo_text


def test_frontend_pages_use_loading_empty_error_and_disconnected_states():
    source = "\n".join(
        _read(path)
        for path in (FRONTEND / "src" / "pages").glob("*.tsx")
    )
    for phrase in [
        "LoadingState",
        "EmptyState",
        "ErrorState",
        "ApiDisconnectedNotice",
        "ApiModeIndicator",
        "DiagnosticsPanel",
        "RecommendedActions",
        "disabled={",
        "aria-live",
    ]:
        assert phrase in source

    app_text = _read(FRONTEND / "src" / "App.tsx")
    assert "SafetyNotice" in app_text


def test_frontend_fixture_manifest_marks_demo_mode_as_not_live_validation():
    manifest = _read(ROOT / "examples" / "api" / "frontend_fixture_manifest.json")
    assert '"frontend_implementation": "mvp implemented under frontend/"' in manifest
    assert "demo fixtures are not live validation" in manifest
