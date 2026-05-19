"""Deterministic source/monitor inference for local optical-language previews."""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Literal

from pydantic import BaseModel, Field


SourceType = Literal[
    "plane_wave",
    "gaussian_beam",
    "mode_source",
    "broadband_pulse",
    "ray_bundle",
    "unknown",
]
MonitorType = Literal[
    "scattering_spectrum",
    "reflectance_transmittance",
    "near_field",
    "far_field",
    "mode_overlap",
    "focal_spot",
    "image_plane",
    "phase_profile",
    "band_structure",
    "unknown",
]


class OpticalSourceModel(BaseModel):
    source_type: SourceType = "unknown"
    wavelength_start_nm: float | None = None
    wavelength_stop_nm: float | None = None
    wavelength_nm: float | None = None
    polarization: str | None = None
    incidence_direction: str | None = None
    beam_waist_um: float | None = None
    mode_index: int | None = None
    notes: str = ""
    defaulted_fields: list[str] = Field(default_factory=list)
    preview_only: bool = True


class OpticalMonitorModel(BaseModel):
    monitor_type: MonitorType = "unknown"
    observable: str = "unknown"
    region: str = "not specified"
    frequency_or_wavelength_sampling: str = "not specified"
    output_units: str = "preview_units"
    notes: str = ""
    defaulted_fields: list[str] = Field(default_factory=list)
    preview_only: bool = True


class OpticalLanguageDiagnostics(BaseModel):
    missing_required_inputs: list[str] = Field(default_factory=list)
    missing_critical_inputs: list[str] = Field(default_factory=list)
    missing_optional_inputs: list[str] = Field(default_factory=list)
    default_assumptions_applied: list[str] = Field(default_factory=list)
    ambiguity_notes: list[str] = Field(default_factory=list)
    blocking_questions: list[str] = Field(default_factory=list)
    safe_to_preview: bool = True
    safe_to_run_solver: bool = False


class SourceMonitorInference(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    matched_template_id: str | None = None
    source_model: OpticalSourceModel
    monitor_model: OpticalMonitorModel
    diagnostics: OpticalLanguageDiagnostics
    recommended_next_actions: list[str] = Field(default_factory=list)
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


def template_source_monitor_defaults(
    template_id: str,
) -> tuple[
    OpticalSourceModel,
    OpticalMonitorModel,
    list[str],
    list[str],
    list[str],
    list[str],
]:
    """Return source/monitor defaults for a local requirement template."""

    try:
        payload = deepcopy(_TEMPLATE_SOURCE_MONITOR[template_id])
    except KeyError:
        payload = deepcopy(_TEMPLATE_SOURCE_MONITOR["unknown"])
    return (
        OpticalSourceModel(**payload["source_model"]),
        OpticalMonitorModel(**payload["monitor_model"]),
        list(payload["required_source_inputs"]),
        list(payload["required_monitor_inputs"]),
        list(payload["default_source_assumptions"]),
        list(payload["default_monitor_assumptions"]),
    )


def infer_source_monitor_from_goal(
    goal: str,
    template_id: str | None = None,
) -> SourceMonitorInference:
    """Infer preview source and monitor metadata with deterministic heuristics."""

    text = goal.strip()
    matched_template_id = template_id
    if matched_template_id is None and text:
        from optical_spec_agent.examples.requirements import match_goal_to_template

        match = match_goal_to_template(text)
        matched_template_id = match.matched_template_id
    inferred_template = matched_template_id or _template_id_from_keywords(text)
    source, monitor, required_source, required_monitor, default_source, default_monitor = (
        template_source_monitor_defaults(inferred_template or "unknown")
    )
    diagnostics = diagnose_missing_inputs(
        goal=text,
        template_id=inferred_template,
        required_source_inputs=required_source,
        required_monitor_inputs=required_monitor,
        source_model=source,
        monitor_model=monitor,
        default_source_assumptions=default_source,
        default_monitor_assumptions=default_monitor,
    )
    status = "ok" if diagnostics.safe_to_preview else "needs_review"
    return SourceMonitorInference(
        status=status,
        matched_template_id=inferred_template,
        source_model=source,
        monitor_model=monitor,
        diagnostics=diagnostics,
        recommended_next_actions=[
            "Review source and monitor defaults before adapter preview.",
            "Answer blocking questions before any optional solver execution.",
            "Treat monitor metadata as preview-only; no solver monitor was executed.",
        ],
    )


def diagnose_missing_inputs(
    *,
    goal: str,
    template_id: str | None = None,
    spec: dict[str, Any] | None = None,
    required_source_inputs: list[str] | None = None,
    required_monitor_inputs: list[str] | None = None,
    source_model: OpticalSourceModel | None = None,
    monitor_model: OpticalMonitorModel | None = None,
    default_source_assumptions: list[str] | None = None,
    default_monitor_assumptions: list[str] | None = None,
) -> OpticalLanguageDiagnostics:
    """Return missing-input diagnostics for local source/monitor previews."""

    template = template_id or _template_id_from_keywords(goal)
    if (
        source_model is None
        or monitor_model is None
        or required_source_inputs is None
        or required_monitor_inputs is None
    ):
        (
            source_model,
            monitor_model,
            required_source_inputs,
            required_monitor_inputs,
            default_source_assumptions,
            default_monitor_assumptions,
        ) = template_source_monitor_defaults(template or "unknown")
    spec_values = _flatten_spec_values(spec or {})
    missing = []
    for field in [*required_source_inputs, *required_monitor_inputs]:
        value = _model_field_value(field, source_model, monitor_model)
        if value is None and not _field_present(field, spec_values):
            missing.append(field)
    missing_critical, missing_optional = _template_missing_inputs(template, goal, spec_values)
    defaulted = [
        *(default_source_assumptions or []),
        *(default_monitor_assumptions or []),
    ]
    ambiguity = []
    blocking = []
    if source_model.source_type == "unknown":
        ambiguity.append("Source type is unknown; clarify illumination or excitation.")
        blocking.append("What source type should drive the design preview?")
    if monitor_model.monitor_type == "unknown":
        ambiguity.append("Monitor type is unknown; clarify observable/output target.")
        blocking.append("What observable should be monitored?")
    if "polarization" in source_model.defaulted_fields:
        ambiguity.append("Polarization was defaulted; confirm before solver execution.")
    if "wavelength_range_nm" in source_model.defaulted_fields:
        ambiguity.append("Wavelength range was defaulted; confirm the design band.")
    if missing_critical:
        ambiguity.append("Critical design inputs are absent; safe preview may proceed with defaults, but solver execution remains blocked.")
    if missing_optional:
        ambiguity.append("Optional design inputs are absent; preview quality may improve if they are provided.")
    blocking.extend(_questions_for_missing(template, missing_critical, missing_optional))
    return OpticalLanguageDiagnostics(
        missing_required_inputs=sorted(set([*missing, *missing_critical])),
        missing_critical_inputs=sorted(set(missing_critical)),
        missing_optional_inputs=sorted(set(missing_optional)),
        default_assumptions_applied=defaulted,
        ambiguity_notes=ambiguity,
        blocking_questions=blocking,
        safe_to_preview=True,
        safe_to_run_solver=False,
    )


def generate_disambiguation_questions(
    *,
    template_id: str | None,
    missing_critical_inputs: list[str],
    missing_optional_inputs: list[str],
    candidate_templates: list[str] | None = None,
) -> list[str]:
    """Generate deterministic questions for ambiguous or under-specified goals."""

    questions: list[str] = []
    if candidate_templates and len(candidate_templates) > 1:
        questions.append(
            "Which candidate template should be prioritized: "
            + ", ".join(candidate_templates[:4])
            + "?"
        )
    questions.extend(_questions_for_missing(template_id, missing_critical_inputs, missing_optional_inputs))
    if not questions:
        questions.append("Confirm that the inferred source, monitor, material, and geometry assumptions are acceptable.")
    questions.append("Confirm whether the backend should remain in local preview mode without running external solvers.")
    return questions


def _template_id_from_keywords(goal: str) -> str | None:
    lowered = goal.lower()
    if any(token in lowered for token in ("nanoparticle", "plasmon", "scattering", "纳米颗粒", "散射")):
        return "nanoparticle_plasmonics"
    if any(token in lowered for token in ("anti-reflection", "antireflection", "coating", "thin film", "增透", "镀膜", "薄膜")):
        return "thin_film_ar_coating"
    if any(token in lowered for token in ("gaussian", "beam waist", "focus", "高斯", "光腰", "聚焦")):
        return "gaussian_beam_focus"
    if any(token in lowered for token in ("waveguide", "single mode", "波导", "单模")):
        return "slab_waveguide_single_mode"
    if any(token in lowered for token in ("lens", "imaging", "ray trace", "透镜", "成像")):
        return "paraxial_lens_imaging"
    if any(token in lowered for token in ("photonic crystal", "band structure", "光子晶体", "能带")):
        return "photonic_crystal_band_preview"
    if any(token in lowered for token in ("metasurface", "metalens", "超表面", "超透镜")):
        return "dielectric_metasurface_preview"
    return None


def _flatten_spec_values(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, dict):
        return " ".join(f"{key} {_flatten_spec_values(item)}" for key, item in value.items()).lower()
    if isinstance(value, list):
        return " ".join(_flatten_spec_values(item) for item in value).lower()
    return str(value).lower()


def _model_field_value(
    field: str,
    source_model: OpticalSourceModel,
    monitor_model: OpticalMonitorModel,
) -> Any:
    if field == "wavelength_range_nm":
        if source_model.wavelength_start_nm is not None and source_model.wavelength_stop_nm is not None:
            return (source_model.wavelength_start_nm, source_model.wavelength_stop_nm)
        return None
    if field == "wavelength_or_frequency":
        return source_model.wavelength_nm or source_model.wavelength_start_nm
    if field == "monitor_region":
        return monitor_model.region if monitor_model.region != "not specified" else None
    if field == "sampling":
        sampling = monitor_model.frequency_or_wavelength_sampling
        return sampling if sampling != "not specified" else None
    if field == "observable":
        return monitor_model.observable if monitor_model.observable != "unknown" else None
    return getattr(source_model, field, None) or getattr(monitor_model, field, None)


def _template_missing_inputs(
    template_id: str | None,
    goal: str,
    spec_values: str,
) -> tuple[list[str], list[str]]:
    text = f"{goal} {spec_values}".lower()
    rules: dict[str, tuple[list[tuple[str, tuple[str, ...]]], list[tuple[str, tuple[str, ...]]]]] = {
        "nanoparticle_plasmonics": (
            [
                ("particle_radius_or_diameter", ("radius", "diameter", "半径", "直径")),
                ("particle_material", ("silver", "gold", "ag", "au", "材料")),
                ("wavelength_band", ("wavelength", "波长", "400", "900")),
            ],
            [
                ("film_thickness", ("film thickness", "薄膜厚度", "thickness")),
                ("background_medium", ("water", "air", "medium", "背景")),
                ("polarization", ("polarization", "偏振")),
            ],
        ),
        "thin_film_ar_coating": (
            [
                ("target_wavelength", ("wavelength", "波长", "550")),
                ("substrate_material", ("substrate", "基底", "glass")),
            ],
            [
                ("incidence_angle", ("angle", "入射角")),
                ("polarization", ("polarization", "偏振")),
            ],
        ),
        "gaussian_beam_focus": (
            [
                ("wavelength", ("wavelength", "波长")),
                ("input_waist", ("waist", "光腰")),
                ("focal_length", ("focal", "焦距")),
            ],
            [("propagation_distance", ("distance", "距离", "z"))],
        ),
        "slab_waveguide_single_mode": (
            [
                ("core_index_or_material", ("core", "芯层", "材料")),
                ("cladding_index_or_material", ("cladding", "包层")),
                ("core_thickness", ("thickness", "厚度")),
                ("wavelength", ("wavelength", "波长")),
            ],
            [("polarization_or_mode_family", ("te", "tm", "polarization", "偏振"))],
        ),
        "paraxial_lens_imaging": (
            [
                ("focal_length", ("focal", "焦距")),
                ("object_distance", ("object distance", "物距")),
            ],
            [
                ("aperture", ("aperture", "孔径")),
                ("field_of_view", ("field", "视场")),
                ("wavelength", ("wavelength", "波长")),
            ],
        ),
        "photonic_crystal_band_preview": (
            [
                ("lattice_constant", ("lattice", "period", "晶格", "周期")),
                ("unit_cell_geometry", ("unit cell", "单胞", "孔", "柱")),
                ("k_point_path", ("k-point", "k point", "能带路径")),
            ],
            [("polarization_or_mode_family", ("te", "tm", "偏振"))],
        ),
        "dielectric_metasurface_preview": (
            [
                ("wavelength", ("wavelength", "波长")),
                ("period", ("period", "周期")),
                ("target_phase_profile", ("phase", "相位")),
            ],
            [("polarization", ("polarization", "偏振")), ("material_stack", ("material", "材料"))],
        ),
    }
    critical_rules, optional_rules = rules.get(template_id or "", ([], []))
    critical = [field for field, tokens in critical_rules if not any(token.lower() in text for token in tokens)]
    optional = [field for field, tokens in optional_rules if not any(token.lower() in text for token in tokens)]
    if template_id is None:
        critical = ["optical_application", "source_type", "target_observable"]
        optional = ["wavelength_band", "material_system", "geometry_scale"]
    return critical, optional


def _questions_for_missing(
    template_id: str | None,
    missing_critical: list[str],
    missing_optional: list[str],
) -> list[str]:
    questions: list[str] = []
    if missing_critical:
        questions.append("Which values should be used for critical inputs: " + ", ".join(missing_critical) + "?")
    if missing_optional:
        questions.append("Can you provide optional context for: " + ", ".join(missing_optional) + "?")
    if template_id == "paraxial_lens_imaging" and ("aperture" in missing_optional or "field_of_view" in missing_optional):
        questions.append("For the lens preview, what aperture and field of view should bound the paraxial assumptions?")
    if template_id == "nanoparticle_plasmonics" and missing_critical:
        questions.append("For nanoparticle scattering, what radius/material/wavelength band should be used before solver setup?")
    return questions


def _field_present(field: str, flattened_spec: str) -> bool:
    aliases = {
        "wavelength_or_frequency": ("wavelength", "frequency", "lambda"),
        "wavelength_range_nm": ("wavelength", "wavelength_range", "400", "900"),
        "wavelength_nm": ("wavelength", "lambda"),
        "polarization": ("polarization", "te", "tm", "linear"),
        "incidence_direction": ("incident", "direction", "normal"),
        "beam_waist_um": ("waist", "beam_waist"),
        "mode_index": ("mode", "mode_index"),
        "monitor_region": ("monitor", "region"),
        "observable": ("observable", "scattering", "reflectance", "transmission", "field"),
        "sampling": ("sampling", "frequency", "wavelength"),
    }
    return any(alias in flattened_spec for alias in aliases.get(field, (field,)))


_TEMPLATE_SOURCE_MONITOR: dict[str, dict[str, Any]] = {
    "nanoparticle_plasmonics": {
        "source_model": {
            "source_type": "plane_wave",
            "wavelength_start_nm": 400.0,
            "wavelength_stop_nm": 900.0,
            "polarization": "linear_x",
            "incidence_direction": "normal",
            "notes": "Preview plane-wave-like broadband excitation for nanoparticle scattering.",
            "defaulted_fields": ["wavelength_range_nm", "polarization", "incidence_direction"],
        },
        "monitor_model": {
            "monitor_type": "scattering_spectrum",
            "observable": "scattering/extinction spectrum preview",
            "region": "closed flux box or equivalent far-field proxy around nanoparticle",
            "frequency_or_wavelength_sampling": "400-900 nm preview band",
            "output_units": "normalized preview spectrum",
            "notes": "Monitor metadata only; no FDTD monitor was executed.",
            "defaulted_fields": ["monitor_region", "sampling"],
        },
        "required_source_inputs": ["wavelength_range_nm", "polarization", "incidence_direction"],
        "required_monitor_inputs": ["observable", "monitor_region", "sampling"],
        "default_source_assumptions": [
            "Default to normal-incidence plane-wave-like source.",
            "Default wavelength band is 400-900 nm for nanoparticle scattering previews.",
            "Default polarization is linear_x until specified.",
        ],
        "default_monitor_assumptions": [
            "Default observable is scattering/extinction spectrum preview.",
            "Default monitor is metadata for a flux/far-field proxy; no solver monitor was executed.",
        ],
    },
    "thin_film_ar_coating": {
        "source_model": {
            "source_type": "plane_wave",
            "wavelength_start_nm": 400.0,
            "wavelength_stop_nm": 800.0,
            "wavelength_nm": 550.0,
            "polarization": "s",
            "incidence_direction": "normal",
            "notes": "Normal-incidence plane-wave preview for thin-film reflectance/transmittance.",
            "defaulted_fields": ["wavelength_range_nm", "polarization", "incidence_direction"],
        },
        "monitor_model": {
            "monitor_type": "reflectance_transmittance",
            "observable": "R/T spectrum preview",
            "region": "incident and substrate half-spaces",
            "frequency_or_wavelength_sampling": "400-800 nm preview sweep",
            "output_units": "dimensionless R/T/A",
            "notes": "Local calculator output, not an external solver monitor.",
            "defaulted_fields": ["sampling"],
        },
        "required_source_inputs": ["wavelength_range_nm", "polarization", "incidence_direction"],
        "required_monitor_inputs": ["observable", "sampling"],
        "default_source_assumptions": [
            "Default to normal incidence.",
            "Default wavelength sweep is 400-800 nm with a 550 nm design point.",
        ],
        "default_monitor_assumptions": [
            "Default observable is reflectance/transmittance from local thin-film preview formulas.",
        ],
    },
    "gaussian_beam_focus": {
        "source_model": {
            "source_type": "gaussian_beam",
            "wavelength_nm": 1064.0,
            "beam_waist_um": 10.0,
            "polarization": "scalar_paraxial",
            "incidence_direction": "z_plus",
            "notes": "Paraxial scalar Gaussian beam preview.",
            "defaulted_fields": ["wavelength_nm", "beam_waist_um"],
        },
        "monitor_model": {
            "monitor_type": "focal_spot",
            "observable": "beam radius and focused waist preview",
            "region": "propagation axis / focal plane",
            "frequency_or_wavelength_sampling": "single design wavelength",
            "output_units": "um and mm",
            "notes": "Calculator metadata only; no field monitor was executed.",
            "defaulted_fields": ["monitor_region"],
        },
        "required_source_inputs": ["wavelength_nm", "beam_waist_um"],
        "required_monitor_inputs": ["observable", "monitor_region"],
        "default_source_assumptions": [
            "Default to a 1064 nm scalar Gaussian beam when not specified.",
            "Default waist is 10 um for propagation preview.",
        ],
        "default_monitor_assumptions": [
            "Default monitor is focal spot / beam radius preview.",
        ],
    },
    "slab_waveguide_single_mode": {
        "source_model": {
            "source_type": "mode_source",
            "wavelength_nm": 1550.0,
            "mode_index": 0,
            "polarization": "TE-like",
            "incidence_direction": "guided",
            "notes": "Mode-source metadata for scalar slab-waveguide estimate.",
            "defaulted_fields": ["wavelength_nm", "mode_index", "polarization"],
        },
        "monitor_model": {
            "monitor_type": "mode_overlap",
            "observable": "V-number and single-mode likelihood preview",
            "region": "slab core/cladding cross-section",
            "frequency_or_wavelength_sampling": "single wavelength",
            "output_units": "dimensionless V-number",
            "notes": "Local scalar estimate, not a mode-solver monitor.",
            "defaulted_fields": ["observable"],
        },
        "required_source_inputs": ["wavelength_nm", "mode_index", "polarization"],
        "required_monitor_inputs": ["observable", "monitor_region"],
        "default_source_assumptions": [
            "Default wavelength is 1550 nm.",
            "Default to fundamental TE-like mode-source metadata.",
        ],
        "default_monitor_assumptions": [
            "Default observable is scalar V-number/single-mode preview.",
        ],
    },
    "paraxial_lens_imaging": {
        "source_model": {
            "source_type": "ray_bundle",
            "wavelength_nm": 550.0,
            "polarization": "not_applicable_first_order",
            "incidence_direction": "z_plus",
            "notes": "First-order ray-bundle metadata for paraxial lens preview.",
            "defaulted_fields": ["wavelength_nm", "incidence_direction"],
        },
        "monitor_model": {
            "monitor_type": "image_plane",
            "observable": "image distance and magnification preview",
            "region": "paraxial image plane",
            "frequency_or_wavelength_sampling": "single design wavelength",
            "output_units": "mm and dimensionless magnification",
            "notes": "ABCD calculator output, not ray-trace validation.",
            "defaulted_fields": ["observable"],
        },
        "required_source_inputs": ["wavelength_nm", "incidence_direction"],
        "required_monitor_inputs": ["observable", "monitor_region"],
        "default_source_assumptions": [
            "Default to a first-order ray bundle at 550 nm.",
        ],
        "default_monitor_assumptions": [
            "Default monitor is paraxial image-plane estimate.",
        ],
    },
    "photonic_crystal_band_preview": {
        "source_model": {
            "source_type": "mode_source",
            "mode_index": 0,
            "notes": "Eigenmode/band-structure context; no time-domain source is executed.",
            "defaulted_fields": ["mode_index"],
        },
        "monitor_model": {
            "monitor_type": "band_structure",
            "observable": "band diagram preview",
            "region": "reciprocal-space k-path",
            "frequency_or_wavelength_sampling": "k-path / band index scaffold",
            "output_units": "normalized frequency preview",
            "notes": "MPB adapter metadata only; no band solver was run.",
            "defaulted_fields": ["sampling"],
        },
        "required_source_inputs": ["mode_index"],
        "required_monitor_inputs": ["observable", "sampling"],
        "default_source_assumptions": [
            "Treat the case as an eigenmode/band-structure preview, not a driven source simulation.",
        ],
        "default_monitor_assumptions": [
            "Default monitor is band-structure metadata over a k-path scaffold.",
        ],
    },
    "dielectric_metasurface_preview": {
        "source_model": {
            "source_type": "plane_wave",
            "wavelength_nm": 633.0,
            "polarization": "linear_x",
            "incidence_direction": "normal",
            "notes": "Normal-incidence plane-wave metadata for metasurface phase preview.",
            "defaulted_fields": ["wavelength_nm", "polarization", "incidence_direction"],
        },
        "monitor_model": {
            "monitor_type": "phase_profile",
            "observable": "phase profile / far-field preview",
            "region": "transmission plane or far-field proxy",
            "frequency_or_wavelength_sampling": "single design wavelength",
            "output_units": "phase radians / normalized field preview",
            "notes": "No FDTD/RCWA field monitor was executed.",
            "defaulted_fields": ["monitor_region"],
        },
        "required_source_inputs": ["wavelength_nm", "polarization", "incidence_direction"],
        "required_monitor_inputs": ["observable", "monitor_region"],
        "default_source_assumptions": [
            "Default to normal-incidence linear_x plane wave at 633 nm.",
        ],
        "default_monitor_assumptions": [
            "Default monitor is phase-profile/far-field preview metadata.",
        ],
    },
    "unknown": {
        "source_model": {
            "source_type": "unknown",
            "notes": "No deterministic source model matched this goal.",
        },
        "monitor_model": {
            "monitor_type": "unknown",
            "observable": "unknown",
            "notes": "No deterministic monitor model matched this goal.",
        },
        "required_source_inputs": ["source_type", "wavelength_or_frequency"],
        "required_monitor_inputs": ["observable", "monitor_region"],
        "default_source_assumptions": [
            "No source defaults applied because the optical case is ambiguous.",
        ],
        "default_monitor_assumptions": [
            "No monitor defaults applied because the observable is ambiguous.",
        ],
    },
}
