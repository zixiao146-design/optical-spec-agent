"""Material provenance coverage tests."""

from optical_spec_agent.materials.catalog import list_materials


def test_all_materials_have_preview_provenance_fields():
    materials = list_materials()
    assert materials
    for material in materials:
        assert material.provenance_type
        assert material.source_note
        assert material.wavelength_validity_note
        assert material.known_limitations
        assert material.requires_user_verification is True
        assert material.production_grade_optical_constants is False
        assert material.production_grade is False
        assert material.validation_level == "preview"
