"""Simple in-process adapter registry for solver input generation."""

from __future__ import annotations

from optical_spec_agent.adapters.base import AdapterMetadata, BaseAdapter
from optical_spec_agent.adapters.elmer import ElmerAdapter
from optical_spec_agent.adapters.gmsh import GmshAdapter
from optical_spec_agent.adapters.meep import MeepAdapter
from optical_spec_agent.adapters.mpb import MPBAdapter
from optical_spec_agent.adapters.optiland import OptilandAdapter
from optical_spec_agent.adapters.utils import as_lower, get_status_value
from optical_spec_agent.models.spec import OpticalSpec


class AdapterRegistryError(ValueError):
    """Raised when adapter lookup or dispatch cannot be resolved."""


_ADAPTER_CLASSES: dict[str, type[BaseAdapter]] = {
    "meep": MeepAdapter,
    "mpb": MPBAdapter,
    "gmsh": GmshAdapter,
    "elmer": ElmerAdapter,
    "optiland": OptilandAdapter,
}


def list_adapters() -> list[AdapterMetadata]:
    """Return metadata for all registered adapters."""
    return [adapter.metadata() for adapter in _adapter_instances().values()]


def get_adapter(tool_name: str) -> BaseAdapter:
    """Return an adapter by tool name, with aliases normalized."""
    normalized = _normalize_tool(tool_name)
    try:
        return _ADAPTER_CLASSES[normalized]()
    except KeyError as exc:
        known = ", ".join(sorted(_ADAPTER_CLASSES))
        raise AdapterRegistryError(f"Unknown adapter '{tool_name}'. Known adapters: {known}") from exc


def dispatch_adapter(spec: OpticalSpec, preferred_tool: str | None = None) -> BaseAdapter:
    """Select an adapter from explicit preference or spec solver/tool hints."""
    preferred = _normalize_tool(preferred_tool or "auto")
    if preferred != "auto":
        return get_adapter(preferred)

    software = _normalize_tool(get_status_value(spec, "simulation.software_tool") or "")
    if software in _ADAPTER_CLASSES:
        return get_adapter(software)

    solver = as_lower(get_status_value(spec, "simulation.solver_method"))
    solver_map = {
        "fdtd": "meep",
        "band_structure": "mpb",
        "band_diagram": "mpb",
        "mode_solver": "mpb",
        "eigenmode": "mpb",
        "frequency_domain": "mpb",
        "mesh": "gmsh",
        "geometry": "gmsh",
        "fem": "elmer",
        "electromagnetic_fem": "elmer",
        "scattering_fem": "elmer",
        "ray_trace": "optiland",
        "raytracing": "optiland",
        "geometric_optics": "optiland",
    }
    if solver in solver_map:
        return get_adapter(solver_map[solver])

    physical_system = as_lower(get_status_value(spec, "physics.physical_system"))
    physical_map = {
        "photonic_crystal": "mpb",
        "periodic_structure": "mpb",
        "lens": "optiland",
        "imaging_system": "optiland",
        "optical_system": "optiland",
        "ray_tracing": "optiland",
    }
    if physical_system in physical_map:
        return get_adapter(physical_map[physical_system])

    raise AdapterRegistryError(
        "Could not auto-select an adapter. Pass --tool meep|mpb|gmsh|elmer|optiland."
    )


def _adapter_instances() -> dict[str, BaseAdapter]:
    return {name: cls() for name, cls in _ADAPTER_CLASSES.items()}


def _normalize_tool(tool_name: str) -> str:
    return str(tool_name or "").strip().lower().replace("-", "_")
