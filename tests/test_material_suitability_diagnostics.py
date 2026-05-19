"""Material suitability diagnostic tests."""

from optical_spec_agent.materials.catalog import diagnose_material_suitability


def test_ag_nanoparticle_plasmonics_is_likely_suitable_preview():
    diagnostic = diagnose_material_suitability("ag", "nanoparticle plasmonics")
    assert diagnostic.suitable is True
    assert diagnostic.suitability == "suitable"
    assert "recommended" not in diagnostic.rationale.lower()
    assert diagnostic.recommended_verification
    assert diagnostic.production_grade_optical_constants is False


def test_bk7_plasmonics_warns_not_suitable_preview():
    diagnostic = diagnose_material_suitability("glass_bk7_preview", "nanoparticle plasmonics")
    assert diagnostic.suitable is False
    assert diagnostic.suitability == "not_suitable"
    assert diagnostic.warnings
    assert diagnostic.recommended_verification
    assert diagnostic.production_grade_optical_constants is False


def test_unknown_material_returns_stable_unknown_diagnostic():
    diagnostic = diagnose_material_suitability("unobtainium", "waveguide")
    assert diagnostic.suitable is None
    assert diagnostic.suitability == "unknown"
    assert "material_catalog_entry" in diagnostic.missing_context
    assert diagnostic.requires_user_verification is True
    assert diagnostic.production_grade_optical_constants is False
