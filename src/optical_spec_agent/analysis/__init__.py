"""Analysis helpers for local/manual diagnostics."""

from .mesh_sanity import MeshSanityResult, analyze_mesh_resolution
from .physical_diagnostics import (
    CORE_HERO_TASK,
    DIAGNOSTICS_SCHEMA_VERSION,
    FluxMonitorSummary,
    PhysicalDiagnosticsResult,
    analyze_execution_artifacts,
    analyze_flux_artifacts,
    extract_diagnostic_config,
    generate_physical_diagnostics,
    load_optical_spec,
    prepare_diagnostic_spec,
)
from .spectrum_compare import (
    SpectrumComparison,
    SpectrumData,
    analyze_flux_signal,
    compare_spectra,
    load_scattering_csv,
    summarize_comparisons,
)

__all__ = [
    "SpectrumComparison",
    "SpectrumData",
    "MeshSanityResult",
    "CORE_HERO_TASK",
    "DIAGNOSTICS_SCHEMA_VERSION",
    "FluxMonitorSummary",
    "PhysicalDiagnosticsResult",
    "analyze_execution_artifacts",
    "analyze_flux_artifacts",
    "analyze_flux_signal",
    "analyze_mesh_resolution",
    "compare_spectra",
    "extract_diagnostic_config",
    "generate_physical_diagnostics",
    "load_scattering_csv",
    "load_optical_spec",
    "prepare_diagnostic_spec",
    "summarize_comparisons",
]
