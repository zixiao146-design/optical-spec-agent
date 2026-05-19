"""Backend capabilities smoke script tests."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_smoke_backend_capabilities_script_is_safe_and_covers_endpoints():
    path = ROOT / "scripts" / "smoke_backend_capabilities.sh"
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for phrase in [
        "scripts/audit_sub_agents.py",
        "scripts/check_adapter_native_golden.py",
        "scripts/audit_validation_claims.py",
        "/api/tool-capabilities",
        "/api/backend-validation-maturity",
        "/api/agent-session",
        "/api/optical-language/infer",
        "/api/optical-language/diagnose",
        "/api/optical-language/observables/diagnose",
        "/api/optical-language/adapter-mapping",
        "/api/adapter-native-golden-coverage",
        "/api/optics/thin-film",
        "/api/optics/thin-film-spectrum",
        "/api/optics/quarter-wave-ar",
        "/api/optics/paraxial-lens",
        "/api/optics/paraxial-system",
        "/api/optics/two-lens-relay",
        "/api/optics/gaussian-beam",
        "/api/optics/gaussian-beam-series",
        "/api/optics/gaussian-beam-focus",
        "/api/optics/waveguide-estimate",
        "/api/optics/waveguide-sweep",
        "/api/optics/waveguide-single-mode-range",
        "CALCULATOR SANITY CHECKS PASSED",
        "SOURCE/MONITOR INFERENCE PASSED",
        "MISSING INPUT DIAGNOSTICS PASSED",
        "OBSERVABLE DIAGNOSTICS PASSED",
        "ADAPTER SOURCE/MONITOR MAPPING PASSED",
        "ADAPTER NATIVE GOLDEN CHECKS PASSED",
        "ADAPTER NATIVE METADATA DIFF PASSED",
        "ADAPTER GOLDEN COVERAGE REPORT PASSED",
        "VALIDATION MATURITY CHECKS PASSED",
        "VALIDATION CLAIM AUDIT PASSED",
        "NO SOLVER EXECUTION PERFORMED",
        "NO EXTERNAL LLM CALLED",
        "NO UPLOAD PERFORMED",
        "NO TAG CREATED",
        "NO RELEASE CREATED",
    ]:
        assert phrase in text
    assert "twine upload" not in text
    assert "gh release create" not in text
    assert "git tag" not in text
