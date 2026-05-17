"""Local preview material catalog helpers."""

from __future__ import annotations

from .data import MATERIALS
from .models import MaterialDetail, MaterialSummary


def _normalize(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _summary(material: MaterialDetail) -> MaterialSummary:
    return MaterialSummary(**material.model_dump(exclude={"wavelength_range_nm", "refractive_index_model", "notes"}))


def list_materials() -> list[MaterialSummary]:
    """Return material summaries sorted by stable material_id."""

    return [_summary(material) for material in sorted(MATERIALS, key=lambda item: item.material_id)]


def get_material(material_id_or_alias: str) -> MaterialDetail | None:
    """Resolve a material by ID or alias."""

    target = _normalize(material_id_or_alias)
    for material in MATERIALS:
        names = {material.material_id, *material.aliases}
        if target in {_normalize(name) for name in names}:
            return material
    return None


def search_materials(query: str) -> list[MaterialSummary]:
    """Search material summaries by ID, aliases, use, category, and role."""

    needle = _normalize(query)
    if not needle:
        return list_materials()
    matches: list[MaterialSummary] = []
    for material in MATERIALS:
        haystack = " ".join(
            [
                material.material_id,
                material.display_name,
                material.category,
                material.optical_role,
                *material.aliases,
                *material.common_use,
            ]
        )
        if needle in _normalize(haystack):
            matches.append(_summary(material))
    return matches


SUGGESTION_RULES: tuple[tuple[tuple[str, ...], tuple[str, ...]], ...] = (
    (("nanoparticle", "plasmon", "antenna", "scattering"), ("au", "ag", "sio2", "water", "air")),
    (("metasurface", "dielectric meta", "metalens"), ("tio2", "si3n4", "si", "sio2")),
    (("waveguide", "mode", "integrated photonics"), ("si", "sio2", "si3n4", "gaas")),
    (("thin film", "coating", "mirror", "antireflection"), ("sio2", "tio2", "al2o3")),
    (("lens", "ray", "objective"), ("glass_bk7_preview", "glass_fused_silica_preview", "air")),
    (("photonic crystal", "band", "mpb"), ("si", "gaas", "sio2", "air")),
)


def suggest_materials_for_application(application: str) -> list[MaterialSummary]:
    """Suggest preview materials for a broad optical application phrase."""

    text = _normalize(application)
    selected: list[str] = []
    for keywords, material_ids in SUGGESTION_RULES:
        if any(_normalize(keyword) in text for keyword in keywords):
            selected.extend(material_ids)
    if not selected:
        selected = ["sio2", "si", "air"]

    unique: list[MaterialSummary] = []
    seen: set[str] = set()
    for material_id in selected:
        material = get_material(material_id)
        if material and material.material_id not in seen:
            unique.append(_summary(material))
            seen.add(material.material_id)
    return unique
