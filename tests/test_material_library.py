from optical_spec_agent.materials.catalog import (
    get_material,
    list_materials,
    suggest_materials_for_application,
)


def test_material_catalog_contains_starter_materials_and_preview_boundaries():
    ids = {material.material_id for material in list_materials()}
    for material_id in {
        "air",
        "water",
        "sio2",
        "si",
        "si3n4",
        "tio2",
        "al2o3",
        "au",
        "ag",
        "ito",
        "gaas",
        "glass_bk7_preview",
        "glass_fused_silica_preview",
    }:
        assert material_id in ids
    for material in list_materials():
        assert material.production_grade is False
        assert material.validation_level == "preview"
        assert "preview" in material.source_note.lower()


def test_material_aliases_and_suggestions_work_without_overclaiming():
    assert get_material("silica").material_id == "sio2"
    assert get_material("bk7").material_id == "glass_bk7_preview"
    suggestions = suggest_materials_for_application("nanoparticle plasmonics")
    ids = {material.material_id for material in suggestions}
    assert {"au", "ag", "sio2"}.issubset(ids)
    assert all(material.production_grade is False for material in suggestions)
