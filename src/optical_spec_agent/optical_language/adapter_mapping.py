"""Adapter-native source/monitor mapping for preview-only artifacts."""

from __future__ import annotations

from pydantic import BaseModel, Field

from .observables import ObservableDiagnostic
from .source_monitor import OpticalMonitorModel, OpticalSourceModel


class AdapterSourceMonitorMapping(BaseModel):
    adapter_name: str
    source_mapping_summary: str
    monitor_mapping_summary: str
    native_source_terms: list[str] = Field(default_factory=list)
    native_monitor_terms: list[str] = Field(default_factory=list)
    supported_observables: list[str] = Field(default_factory=list)
    unsupported_observables: list[str] = Field(default_factory=list)
    preview_metadata: dict[str, object] = Field(default_factory=dict)
    requires_solver_for_real_result: bool = True
    external_solver_executed: bool = False
    diagnostics: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    preview_only: bool = True
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


def map_source_monitor_to_adapter(
    adapter_name: str,
    source_model: OpticalSourceModel,
    monitor_model: OpticalMonitorModel,
    observable_diagnostics: list[ObservableDiagnostic],
) -> AdapterSourceMonitorMapping:
    """Map inferred optical-language metadata to an adapter-native preview.

    This function only creates metadata. It does not run Meep, MPB, Gmsh,
    ElmerSolver, Optiland, or any other external solver.
    """

    normalized = _normalize_adapter_name(adapter_name)
    observable_kinds = [item.observable_kind for item in observable_diagnostics]
    if normalized == "meep":
        return _meep_mapping(source_model, monitor_model, observable_kinds)
    if normalized == "mpb":
        return _mpb_mapping(source_model, monitor_model, observable_kinds)
    if normalized == "gmsh":
        return _gmsh_mapping(source_model, monitor_model, observable_kinds)
    if normalized == "elmer":
        return _elmer_mapping(source_model, monitor_model, observable_kinds)
    if normalized == "optiland":
        return _optiland_mapping(source_model, monitor_model, observable_kinds)
    return AdapterSourceMonitorMapping(
        adapter_name=adapter_name or "unknown",
        source_mapping_summary="Unknown adapter; source mapping is not available.",
        monitor_mapping_summary="Unknown adapter; monitor mapping is not available.",
        unsupported_observables=observable_kinds or ["unknown"],
        preview_metadata={
            "source_type": source_model.source_type,
            "monitor_type": monitor_model.monitor_type,
            "observable": monitor_model.observable,
        },
        diagnostics=["Adapter name did not match a registered open-source preview adapter."],
        warnings=["Use /api/adapters to inspect supported adapter names."],
    )


def _normalize_adapter_name(adapter_name: str) -> str:
    lowered = (adapter_name or "").lower()
    for candidate in ("meep", "mpb", "gmsh", "elmer", "optiland"):
        if candidate in lowered:
            return candidate
    return lowered or "unknown"


def _split_supported(
    observable_kinds: list[str],
    supported: set[str],
) -> tuple[list[str], list[str]]:
    return (
        [kind for kind in observable_kinds if kind in supported],
        [kind for kind in observable_kinds if kind not in supported],
    )


def _meep_mapping(
    source_model: OpticalSourceModel,
    monitor_model: OpticalMonitorModel,
    observable_kinds: list[str],
) -> AdapterSourceMonitorMapping:
    supported, unsupported = _split_supported(
        observable_kinds,
        {
            "scattering_spectrum",
            "extinction_spectrum",
            "near_field",
            "far_field",
            "dft_field",
            "reflectance",
            "transmittance",
            "phase_profile",
        },
    )
    native_source = ["mp.Source", "GaussianSource/broadband pulse metadata"]
    if source_model.source_type == "plane_wave":
        native_source.append("planewave-like current source placeholder")
    native_monitor = ["flux monitor metadata", "DFT field monitor metadata"]
    if monitor_model.monitor_type == "scattering_spectrum":
        native_monitor.append("closed flux box / incident-flux normalization plan")
    return AdapterSourceMonitorMapping(
        adapter_name="meep",
        source_mapping_summary=(
            f"{source_model.source_type} maps to Meep source metadata; broadband bands map "
            "to GaussianSource/broadband pulse preview terms."
        ),
        monitor_mapping_summary=(
            f"{monitor_model.monitor_type} maps to Meep flux/DFT monitor metadata only."
        ),
        native_source_terms=native_source,
        native_monitor_terms=native_monitor,
        supported_observables=supported,
        unsupported_observables=unsupported,
        preview_metadata={
            "wavelength_start_nm": source_model.wavelength_start_nm,
            "wavelength_stop_nm": source_model.wavelength_stop_nm,
            "polarization": source_model.polarization,
            "monitor_region": monitor_model.region,
            "observable": monitor_model.observable,
        },
        requires_solver_for_real_result=True,
        diagnostics=["Meep preview generation can describe source and monitor intent."],
        warnings=["Real flux, DFT field, scattering, or extinction results require a Meep run."],
    )


def _mpb_mapping(
    source_model: OpticalSourceModel,
    monitor_model: OpticalMonitorModel,
    observable_kinds: list[str],
) -> AdapterSourceMonitorMapping:
    supported, unsupported = _split_supported(
        observable_kinds,
        {"band_structure", "mode_frequency", "mode_overlap"},
    )
    return AdapterSourceMonitorMapping(
        adapter_name="mpb",
        source_mapping_summary=(
            "Time-domain source metadata is interpreted as eigenmode/band context; MPB does "
            "not use a driven FDTD source in this preview."
        ),
        monitor_mapping_summary=(
            f"{monitor_model.monitor_type} maps to k-point, band-frequency, or mode metadata."
        ),
        native_source_terms=["lattice/eigenmode context", "mode parity / mode index metadata"],
        native_monitor_terms=["k-points", "num_bands", "band frequencies", "mode field output plan"],
        supported_observables=supported,
        unsupported_observables=unsupported,
        preview_metadata={
            "mode_index": source_model.mode_index,
            "sampling": monitor_model.frequency_or_wavelength_sampling,
            "observable": monitor_model.observable,
        },
        requires_solver_for_real_result=True,
        diagnostics=["MPB mapping is meaningful for band/eigenmode-oriented observables."],
        warnings=["Real band frequencies or mode fields require MPB execution."],
    )


def _gmsh_mapping(
    source_model: OpticalSourceModel,
    monitor_model: OpticalMonitorModel,
    observable_kinds: list[str],
) -> AdapterSourceMonitorMapping:
    supported, unsupported = _split_supported(observable_kinds, {"mesh_region"})
    if not supported:
        unsupported = observable_kinds
    return AdapterSourceMonitorMapping(
        adapter_name="gmsh",
        source_mapping_summary=(
            "Gmsh does not execute optical sources; source intent is attached as geometry/mesh "
            "annotation metadata."
        ),
        monitor_mapping_summary=(
            "Monitor intent maps to physical group / mesh region annotations, not optical fields."
        ),
        native_source_terms=["geometry comments", "mesh-size hints", "source-region annotation"],
        native_monitor_terms=["Physical Surface/Volume groups", "monitor-region annotation"],
        supported_observables=supported,
        unsupported_observables=unsupported,
        preview_metadata={
            "source_annotation": source_model.source_type,
            "monitor_annotation": monitor_model.region,
            "observable": monitor_model.observable,
        },
        requires_solver_for_real_result=True,
        diagnostics=["Gmsh preview can preserve optical intent as mesh annotations."],
        warnings=["No optical observable is computed by Gmsh alone."],
    )


def _elmer_mapping(
    source_model: OpticalSourceModel,
    monitor_model: OpticalMonitorModel,
    observable_kinds: list[str],
) -> AdapterSourceMonitorMapping:
    supported, unsupported = _split_supported(
        observable_kinds,
        {"mode_frequency", "mode_overlap", "near_field", "far_field", "reflectance", "transmittance"},
    )
    return AdapterSourceMonitorMapping(
        adapter_name="elmer",
        source_mapping_summary=(
            f"{source_model.source_type} maps to FEM source/boundary placeholders."
        ),
        monitor_mapping_summary=(
            f"{monitor_model.monitor_type} maps to FEM solver/output section placeholders."
        ),
        native_source_terms=["Boundary Condition placeholders", "Body Force/source section metadata"],
        native_monitor_terms=["ResultOutputSolver placeholder", "field/output variable plan"],
        supported_observables=supported,
        unsupported_observables=unsupported,
        preview_metadata={
            "source_boundary_placeholder": source_model.source_type,
            "monitor_output_placeholder": monitor_model.monitor_type,
            "observable": monitor_model.observable,
        },
        requires_solver_for_real_result=True,
        diagnostics=["Elmer preview preserves source/monitor intent as SIF placeholders."],
        warnings=["Real FEM fields require ElmerSolver execution and reviewed mesh/material setup."],
    )


def _optiland_mapping(
    source_model: OpticalSourceModel,
    monitor_model: OpticalMonitorModel,
    observable_kinds: list[str],
) -> AdapterSourceMonitorMapping:
    supported, unsupported = _split_supported(
        observable_kinds,
        {"focal_spot", "image_plane", "ray_fan"},
    )
    return AdapterSourceMonitorMapping(
        adapter_name="optiland",
        source_mapping_summary=(
            f"{source_model.source_type} maps to object/ray-bundle metadata for ray optics previews."
        ),
        monitor_mapping_summary=(
            f"{monitor_model.monitor_type} maps to image-plane, spot, or ray-fan preview metadata."
        ),
        native_source_terms=["object point/field metadata", "ray bundle", "Gaussian beam note"],
        native_monitor_terms=["image plane", "focal spot", "spot diagram plan", "ray fan plan"],
        supported_observables=supported,
        unsupported_observables=unsupported,
        preview_metadata={
            "wavelength_nm": source_model.wavelength_nm,
            "beam_waist_um": source_model.beam_waist_um,
            "monitor_region": monitor_model.region,
            "observable": monitor_model.observable,
        },
        requires_solver_for_real_result=True,
        diagnostics=["Optiland preview can carry ray source and image-plane intent."],
        warnings=["Real raytrace, spot, or ray fan results require Optiland execution."],
    )
