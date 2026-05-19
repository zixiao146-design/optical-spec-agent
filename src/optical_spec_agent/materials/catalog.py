"""Local preview material catalog helpers."""

from __future__ import annotations

from .data import MATERIALS
from .models import MaterialDetail, MaterialSuitabilityDiagnostic, MaterialSummary


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

APPLICATION_SUITABILITY: dict[str, dict[str, tuple[str, ...]]] = {
    "nanoparticle_plasmonics": {
        "suitable": ("ag", "au", "sio2", "water", "air"),
        "not_suitable": ("glass_bk7_preview", "glass_fused_silica_preview"),
    },
    "dielectric_metasurface": {
        "suitable": ("tio2", "si3n4", "si", "sio2", "gaas"),
        "not_suitable": ("ag", "au", "water"),
    },
    "waveguide": {
        "suitable": ("si", "sio2", "si3n4", "gaas", "air"),
        "not_suitable": ("ag", "au"),
    },
    "thin_film_coating": {
        "suitable": ("sio2", "tio2", "al2o3", "glass_bk7_preview", "glass_fused_silica_preview", "air"),
        "not_suitable": ("ag", "au", "water"),
    },
    "lens_ray_optics": {
        "suitable": ("glass_bk7_preview", "glass_fused_silica_preview", "air"),
        "not_suitable": ("ag", "au", "si"),
    },
    "photonic_crystal": {
        "suitable": ("si", "gaas", "sio2", "air", "si3n4"),
        "not_suitable": ("water",),
    },
}


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


def diagnose_material_suitability(
    material_id_or_alias: str,
    application: str,
) -> MaterialSuitabilityDiagnostic:
    """Return local preview suitability diagnostics for one material/application pair.

    The decision is deterministic and catalog-local. It never queries an
    external material database and never upgrades approximate constants into a
    production-grade claim.
    """

    material = get_material(material_id_or_alias)
    if material is None:
        return MaterialSuitabilityDiagnostic(
            material_id=material_id_or_alias,
            application=application,
            suitability="unknown",
            suitable=None,
            rationale="Material is not present in the local preview catalog.",
            warnings=[
                "No external material database lookup was performed.",
                "Suitability cannot be inferred without a local material record.",
            ],
            missing_context=["material_catalog_entry", "wavelength_band", "fabrication_context"],
            recommended_verification=[
                "Add a reviewed local material entry before using this material in an agent session.",
                "Verify wavelength-dependent n/k values from trusted references outside this preview catalog.",
            ],
            provenance_type="user_must_verify",
        )

    normalized_application = _application_key(application)
    rules = APPLICATION_SUITABILITY.get(normalized_application)
    warnings = [
        "Material suitability is preview/design-assist only.",
        "Verify wavelength-dependent n/k, dispersion, loss, and fabrication constraints independently.",
    ]
    missing_context = _missing_context_for_application(normalized_application)
    recommended_verification = [
        "Confirm the operating wavelength band.",
        "Verify material optical constants against trusted data before physical conclusions.",
        "Review fabrication/process compatibility for the intended geometry.",
    ]

    if rules and material.material_id in rules["suitable"]:
        suitability = "suitable"
        suitable: bool | None = True
        rationale = (
            f"{material.display_name} appears in the local preview allow-list for "
            f"{normalized_application.replace('_', ' ')} workflows."
        )
    elif rules and material.material_id in rules["not_suitable"]:
        suitability = "not_suitable"
        suitable = False
        rationale = (
            f"{material.display_name} is flagged as a poor default for "
            f"{normalized_application.replace('_', ' ')} in the starter catalog."
        )
        warnings.append("Use this material only after explicit human review for this application.")
    else:
        suitability = "unknown"
        suitable = None
        rationale = (
            f"No deterministic suitability rule covers {material.display_name} for "
            f"{normalized_application.replace('_', ' ')}."
        )
        warnings.append("The local catalog cannot make a suitability determination for this pair.")

    if material.production_grade_optical_constants is False:
        warnings.append("This material record is not a production-grade optical constants entry.")

    return MaterialSuitabilityDiagnostic(
        material_id=material.material_id,
        application=application,
        suitable=suitable,
        suitability=suitability,
        rationale=rationale,
        warnings=warnings,
        missing_context=missing_context,
        recommended_verification=recommended_verification,
        provenance_type=material.provenance_type,
        requires_user_verification=material.requires_user_verification,
        production_grade_optical_constants=material.production_grade_optical_constants,
    )


def _application_key(application: str) -> str:
    text = _normalize(application)
    if any(token in text for token in ("nanoparticle", "plasmon", "scattering")):
        return "nanoparticle_plasmonics"
    if any(token in text for token in ("metasurface", "metalens")):
        return "dielectric_metasurface"
    if any(token in text for token in ("waveguide", "mode", "integrated_photonics")):
        return "waveguide"
    if any(token in text for token in ("thin_film", "coating", "antireflection", "anti_reflection")):
        return "thin_film_coating"
    if any(token in text for token in ("lens", "ray", "objective", "imaging")):
        return "lens_ray_optics"
    if any(token in text for token in ("photonic_crystal", "band", "mpb")):
        return "photonic_crystal"
    return "unknown_application"


def _missing_context_for_application(application_key: str) -> list[str]:
    common = ["wavelength_band", "geometry_dimensions"]
    if application_key == "nanoparticle_plasmonics":
        return [*common, "particle_radius", "background_medium", "substrate_or_film_stack"]
    if application_key == "dielectric_metasurface":
        return [*common, "target_phase_profile", "period", "polarization"]
    if application_key == "waveguide":
        return [*common, "core_thickness", "cladding_material", "mode_target"]
    if application_key == "thin_film_coating":
        return [*common, "incident_medium", "substrate_material", "incidence_angle"]
    if application_key == "lens_ray_optics":
        return [*common, "aperture", "field_of_view", "target_focal_length"]
    if application_key == "photonic_crystal":
        return [*common, "lattice_constant", "unit_cell_geometry", "k_point_path"]
    return ["application_context", *common]
