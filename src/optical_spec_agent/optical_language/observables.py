"""Observable taxonomy and diagnostics for local optical previews."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from .source_monitor import OpticalMonitorModel, OpticalSourceModel


ObservableKind = Literal[
    "scattering_spectrum",
    "extinction_spectrum",
    "reflectance",
    "transmittance",
    "absorptance",
    "near_field",
    "far_field",
    "dft_field",
    "band_structure",
    "mode_frequency",
    "mode_overlap",
    "focal_spot",
    "image_plane",
    "ray_fan",
    "phase_profile",
    "mesh_region",
    "unknown",
]


class ObservableDiagnostic(BaseModel):
    observable_kind: ObservableKind
    user_facing_label: str
    user_facing_label_zh: str
    required_inputs: list[str] = Field(default_factory=list)
    default_assumptions: list[str] = Field(default_factory=list)
    adapter_compatibility: dict[str, str] = Field(default_factory=dict)
    preview_supported: bool = True
    solver_execution_required_for_real_result: bool = True
    notes: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


def suggest_observables_for_template(template_id: str | None) -> list[ObservableKind]:
    """Return expected observable kinds for a design requirement template."""

    return list(_TEMPLATE_OBSERVABLES.get(template_id or "unknown", ["unknown"]))


def diagnose_observable(
    source_model: OpticalSourceModel,
    monitor_model: OpticalMonitorModel,
    template_id: str | None = None,
) -> list[ObservableDiagnostic]:
    """Diagnose observables implied by source/monitor metadata.

    This is local deterministic metadata. It never executes a solver and never
    claims the observable has been physically computed.
    """

    kinds = suggest_observables_for_template(template_id)
    if kinds == ["unknown"]:
        kinds = _observable_kinds_from_monitor(monitor_model)
    return [
        _diagnostic_for_kind(kind, source_model=source_model, monitor_model=monitor_model)
        for kind in kinds
    ]


def _observable_kinds_from_monitor(monitor_model: OpticalMonitorModel) -> list[ObservableKind]:
    monitor_type = monitor_model.monitor_type
    observable = monitor_model.observable.lower()
    if monitor_type == "scattering_spectrum":
        return ["scattering_spectrum", "extinction_spectrum"]
    if monitor_type == "reflectance_transmittance":
        return ["reflectance", "transmittance", "absorptance"]
    if monitor_type == "near_field":
        return ["near_field", "dft_field"]
    if monitor_type == "far_field":
        return ["far_field"]
    if monitor_type == "band_structure":
        return ["band_structure", "mode_frequency"]
    if monitor_type == "mode_overlap":
        return ["mode_overlap", "mode_frequency"]
    if monitor_type == "focal_spot":
        return ["focal_spot"]
    if monitor_type == "image_plane":
        return ["image_plane", "ray_fan"]
    if monitor_type == "phase_profile":
        return ["phase_profile", "far_field"]
    if "mesh" in observable:
        return ["mesh_region"]
    return ["unknown"]


def _diagnostic_for_kind(
    kind: ObservableKind,
    *,
    source_model: OpticalSourceModel,
    monitor_model: OpticalMonitorModel,
) -> ObservableDiagnostic:
    payload = dict(_OBSERVABLE_LIBRARY.get(kind, _OBSERVABLE_LIBRARY["unknown"]))
    required = list(payload["required_inputs"])
    defaults = list(payload["default_assumptions"])
    notes = list(payload["notes"])
    warnings = list(payload["warnings"])
    if source_model.preview_only or monitor_model.preview_only:
        notes.append("Source and monitor metadata are preview-only.")
    if monitor_model.monitor_type == "unknown":
        warnings.append("Monitor type is unknown; confirm observable before solver setup.")
    return ObservableDiagnostic(
        observable_kind=kind,
        user_facing_label=payload["label"],
        user_facing_label_zh=payload["label_zh"],
        required_inputs=required,
        default_assumptions=defaults,
        adapter_compatibility=dict(payload["adapter_compatibility"]),
        preview_supported=payload["preview_supported"],
        solver_execution_required_for_real_result=payload[
            "solver_execution_required_for_real_result"
        ],
        notes=notes,
        warnings=warnings,
    )


_TEMPLATE_OBSERVABLES: dict[str, list[ObservableKind]] = {
    "nanoparticle_plasmonics": ["scattering_spectrum", "extinction_spectrum"],
    "thin_film_ar_coating": ["reflectance", "transmittance", "absorptance"],
    "gaussian_beam_focus": ["focal_spot"],
    "slab_waveguide_single_mode": ["mode_overlap", "mode_frequency"],
    "paraxial_lens_imaging": ["image_plane", "ray_fan"],
    "photonic_crystal_band_preview": ["band_structure", "mode_frequency"],
    "dielectric_metasurface_preview": ["phase_profile", "far_field"],
    "unknown": ["unknown"],
}


_COMMON_ADAPTER_COMPATIBILITY = {
    "meep": "preview metadata; real FDTD result requires Meep execution",
    "mpb": "preview metadata only unless the observable is eigenmode/band-oriented",
    "gmsh": "geometry/mesh annotation only; no optical observable computed by Gmsh alone",
    "elmer": "FEM placeholder metadata; real result requires ElmerSolver execution",
    "optiland": "ray/object/image metadata only unless ray tracing is explicitly run",
}


_OBSERVABLE_LIBRARY: dict[str, dict[str, object]] = {
    "scattering_spectrum": {
        "label": "Scattering spectrum",
        "label_zh": "散射谱",
        "required_inputs": ["wavelength_range_nm", "source polarization", "flux/field monitor region"],
        "default_assumptions": ["Spectrum is normalized preview metadata until a solver run exists."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": True,
        "notes": ["Useful for nanoparticle/FDTD preview planning."],
        "warnings": ["No scattering spectrum has been computed by this preview."],
    },
    "extinction_spectrum": {
        "label": "Extinction spectrum",
        "label_zh": "消光谱",
        "required_inputs": ["incident flux reference", "scattered/total flux monitor"],
        "default_assumptions": ["Extinction is treated as a planned observable, not a result."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": True,
        "notes": ["Pairs with scattering/absorption diagnostics in FDTD-style workflows."],
        "warnings": ["Incident/reference normalization must be reviewed before solver use."],
    },
    "reflectance": {
        "label": "Reflectance",
        "label_zh": "反射率",
        "required_inputs": ["incident medium index", "layer stack", "substrate index", "wavelength"],
        "default_assumptions": ["Normal-incidence local thin-film preview unless specified."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": False,
        "notes": ["Local calculator can produce design-assist R values."],
        "warnings": ["Calculator result is sanity-checked preview, not production validation."],
    },
    "transmittance": {
        "label": "Transmittance",
        "label_zh": "透射率",
        "required_inputs": ["incident medium index", "layer stack", "substrate index", "wavelength"],
        "default_assumptions": ["Lossless simplifications may apply in local previews."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": False,
        "notes": ["Local calculator can produce design-assist T values."],
        "warnings": ["Oblique/vector effects are limited in preview formulas."],
    },
    "absorptance": {
        "label": "Absorptance estimate",
        "label_zh": "吸收率估计",
        "required_inputs": ["R", "T", "loss model when available"],
        "default_assumptions": ["A is estimated from 1-R-T when applicable."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": False,
        "notes": ["Useful as a sanity balance in thin-film previews."],
        "warnings": ["Lossy dispersive films need verified material data."],
    },
    "near_field": {
        "label": "Near-field distribution",
        "label_zh": "近场分布",
        "required_inputs": ["field component", "monitor plane/volume", "sampling"],
        "default_assumptions": ["DFT/field monitor semantics are preview metadata only."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": True,
        "notes": ["Maps naturally to FDTD field monitor concepts."],
        "warnings": ["No near-field array has been generated."],
    },
    "far_field": {
        "label": "Far-field pattern",
        "label_zh": "远场分布",
        "required_inputs": ["near-to-far region or equivalent", "angular sampling"],
        "default_assumptions": ["Far-field is a planned observable unless solver output exists."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": True,
        "notes": ["Useful for metasurface and scattering preview workflows."],
        "warnings": ["No angular far-field result has been computed."],
    },
    "dft_field": {
        "label": "DFT field monitor",
        "label_zh": "DFT 场监测器",
        "required_inputs": ["field component", "frequency sampling", "monitor region"],
        "default_assumptions": ["DFT field monitor is a native FDTD preview concept."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": True,
        "notes": ["Maps to Meep DFT field monitor metadata."],
        "warnings": ["Real DFT field data requires an FDTD run."],
    },
    "band_structure": {
        "label": "Band structure",
        "label_zh": "能带结构",
        "required_inputs": ["lattice", "k-point path", "number of bands"],
        "default_assumptions": ["MPB k-point/band metadata remains a scaffold."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": True,
        "notes": ["Maps to MPB band-frequency planning."],
        "warnings": ["No eigenfrequency solve was run."],
    },
    "mode_frequency": {
        "label": "Mode frequency / effective index",
        "label_zh": "模式频率 / 有效折射率",
        "required_inputs": ["mode index", "wavelength/frequency", "geometry cross-section"],
        "default_assumptions": ["Mode metadata is scalar/design-assist unless a mode solver runs."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": True,
        "notes": ["Useful for waveguide and MPB/Elmer preview paths."],
        "warnings": ["No vector eigenmode has been solved."],
    },
    "mode_overlap": {
        "label": "Mode overlap",
        "label_zh": "模式重叠",
        "required_inputs": ["input mode", "target mode", "overlap region"],
        "default_assumptions": ["Mode overlap is planned metadata in this backend sprint."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": True,
        "notes": ["Maps to waveguide/mode-solver planning."],
        "warnings": ["No overlap integral has been computed."],
    },
    "focal_spot": {
        "label": "Focal spot",
        "label_zh": "焦斑",
        "required_inputs": ["wavelength", "beam waist or ray bundle", "focal plane"],
        "default_assumptions": ["Paraxial/Gaussian approximations are design-assist only."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": False,
        "notes": ["Local Gaussian/paraxial calculators can produce preview estimates."],
        "warnings": ["Diffraction/vector/aberration effects may be absent."],
    },
    "image_plane": {
        "label": "Image plane",
        "label_zh": "像面",
        "required_inputs": ["object distance", "focal length", "ray/image plane convention"],
        "default_assumptions": ["First-order paraxial approximation."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": False,
        "notes": ["Local paraxial calculators can estimate image distance."],
        "warnings": ["No real raytrace/MTF/spot diagram has been computed."],
    },
    "ray_fan": {
        "label": "Ray fan",
        "label_zh": "光线扇形图",
        "required_inputs": ["ray bundle", "surface sequence", "image plane"],
        "default_assumptions": ["Ray fan remains an Optiland preview concept."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": True,
        "notes": ["Maps to ray-tracing preview metadata."],
        "warnings": ["No ray fan has been traced."],
    },
    "phase_profile": {
        "label": "Phase profile",
        "label_zh": "相位分布",
        "required_inputs": ["wavelength", "polarization", "monitor plane"],
        "default_assumptions": ["Phase profile is planned metadata unless solver/RCWA output exists."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": True,
        "notes": ["Useful for metasurface preview workflows."],
        "warnings": ["No phase map has been computed."],
    },
    "mesh_region": {
        "label": "Mesh/geometry region",
        "label_zh": "网格/几何区域",
        "required_inputs": ["geometry region", "physical group or mesh size"],
        "default_assumptions": ["Mesh regions are geometry annotations, not optical observables."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": True,
        "solver_execution_required_for_real_result": False,
        "notes": ["Maps to Gmsh physical groups / region annotations."],
        "warnings": ["No optical field quantity is computed by mesh generation alone."],
    },
    "unknown": {
        "label": "Unknown observable",
        "label_zh": "未知观测量",
        "required_inputs": ["observable", "monitor region"],
        "default_assumptions": ["No observable defaults can be trusted for this goal."],
        "adapter_compatibility": _COMMON_ADAPTER_COMPATIBILITY,
        "preview_supported": False,
        "solver_execution_required_for_real_result": True,
        "notes": ["Clarify the requested output before solver setup."],
        "warnings": ["Observable is ambiguous."],
    },
}
