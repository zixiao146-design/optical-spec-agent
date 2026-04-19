"""Meep adapter — translator from OpticalSpec to MeepInputModel.

Validates that the spec is compatible with the Meep nanoparticle-on-film path,
then extracts and converts fields from the nested StatusField structure into
the flat MeepInputModel.
"""

from __future__ import annotations

import re

from optical_spec_agent.adapters.base import AdapterResult, BaseAdapter
from optical_spec_agent.models.spec import OpticalSpec

from .models import MeepInputModel
from .template import render_script


class AdapterError(Exception):
    """Raised when the adapter cannot handle a spec."""


# Refractive index lookup for common gap media
_GAP_N = {
    "SiO2": 1.45,
    "sio2": 1.45,
    "Si": 1.45,   # parser often extracts "Si" when it means "SiO2"
    "si": 1.45,
    "Al2O3": 1.76,
    "al2o3": 1.76,
    "Si3N4": 2.0,
    "si3n4": 2.0,
    "Water": 1.33,
    "water": 1.33,
    "Air": 1.0,
    "air": 1.0,
    "Glass": 1.52,
    "TiO2": 2.4,
}

# Default film thickness when not specified
_DEFAULT_FILM_THICKNESS_NM = 100.0

# Supported shapes → Meep geometry type
_SHAPE_MAP = {
    "sphere": "sphere",
    "cube": "cube",
    "rod": "cylinder",
}


def _get_sf_value(spec: OpticalSpec, dotted: str):
    """Get StatusField value by dotted path, or None if missing."""
    parts = dotted.split(".", 1)
    if len(parts) != 2:
        return None
    section = getattr(spec, parts[0], None)
    if section is None:
        return None
    sf = getattr(section, parts[1], None)
    if sf is None:
        return None
    from optical_spec_agent.models.base import StatusField
    if isinstance(sf, StatusField) and sf.status != "missing":
        return sf.value
    return None


def _parse_wavelength_range(source_setting) -> tuple[float, float] | None:
    """Parse wavelength range from SourceSetting or string, return (min_um, max_um)."""
    if source_setting is None:
        return None

    # If it's a SourceSetting object
    wl_raw = getattr(source_setting, "wavelength_range", "")
    if not wl_raw:
        return None

    # Parse "400-900 nm" or "400-900nm"
    m = re.match(r"([\d.]+)\s*[-–到至~]\s*([\d.]+)\s*(nm|μm|um)", str(wl_raw), re.IGNORECASE)
    if not m:
        return None

    low, high, unit = float(m.group(1)), float(m.group(2)), m.group(3).lower()
    if unit in ("nm",):
        return (low / 1000.0, high / 1000.0)  # nm → μm
    elif unit in ("μm", "um"):
        return (low, high)
    return None


def _extract_dimension_nm(dimensions: dict, keys: list[str]) -> float | None:
    """Try to extract a numeric value in nm from a dimensions dict."""
    if not isinstance(dimensions, dict):
        return None
    for key in keys:
        val = dimensions.get(key)
        if val is None:
            continue
        # Extract first number from the value string (e.g. "直径80nm" → 80)
        m = re.search(r"([\d.]+)", str(val))
        if m:
            return float(m.group(1))
    return None


class MeepAdapter(BaseAdapter):
    """Meep FDTD adapter — nanoparticle_on_film → scattering_spectrum script."""

    tool_name = "meep"

    def can_handle(self, spec: OpticalSpec) -> bool:
        phys_sys = _get_sf_value(spec, "physics.physical_system")
        solver = _get_sf_value(spec, "simulation.solver_method")
        software = _get_sf_value(spec, "simulation.software_tool")
        return (
            phys_sys == "nanoparticle_on_film"
            and solver == "fdtd"
            and software == "meep"
        )

    def generate(self, spec: OpticalSpec) -> AdapterResult:
        if not self.can_handle(spec):
            raise AdapterError(
                "Meep adapter only supports: physical_system=nanoparticle_on_film, "
                "solver_method=fdtd, software_tool=meep"
            )

        model = self._translate(spec)
        script = render_script(model)
        return AdapterResult(
            tool="meep",
            content=script,
            language="python",
        )

    def _translate(self, spec: OpticalSpec) -> MeepInputModel:
        # --- Particle info ---
        particle_raw = _get_sf_value(spec, "geometry_material.particle_info")
        if not particle_raw:
            raise AdapterError("Missing required field: geometry_material.particle_info")

        p_type = getattr(particle_raw, "particle_type", "") or ""
        p_mat = getattr(particle_raw, "material", "") or ""
        p_dims = getattr(particle_raw, "dimensions", {}) or {}

        shape = _SHAPE_MAP.get(p_type)
        if not shape:
            raise AdapterError(f"Unsupported particle shape: '{p_type}'. Supported: {list(_SHAPE_MAP)}")

        # Extract radius from dimensions
        diameter_nm = _extract_dimension_nm(p_dims, ["直径", "diameter", "边长"])
        if diameter_nm is None:
            # fallback: try to find any numeric dimension and halve it
            first_dim = _extract_dimension_nm(p_dims, list(p_dims.keys())[:1]) if p_dims else None
            if first_dim:
                diameter_nm = first_dim
            else:
                raise AdapterError(
                    "Cannot determine particle size from particle_info.dimensions. "
                    "Add a '直径' or 'diameter' key, e.g. {'直径': '80 nm'}"
                )
        radius_um = (diameter_nm / 2.0) / 1000.0

        # --- Film info ---
        film_raw = _get_sf_value(spec, "geometry_material.substrate_or_film_info")
        if not film_raw:
            raise AdapterError("Missing required field: geometry_material.substrate_or_film_info")

        film_mat = getattr(film_raw, "film_material", "") or ""
        if not film_mat:
            raise AdapterError("substrate_or_film_info.film_material is empty")

        film_thick_str = getattr(film_raw, "film_thickness", "") or ""
        film_thick_nm = _DEFAULT_FILM_THICKNESS_NM
        if film_thick_str:
            m = re.match(r"([\d.]+)", str(film_thick_str))
            if m:
                film_thick_nm = float(m.group(1))
        film_thick_um = film_thick_nm / 1000.0

        # --- Gap medium ---
        gap_name = _get_sf_value(spec, "geometry_material.gap_medium") or ""
        gap_n = _GAP_N.get(gap_name)
        if gap_n is None:
            if gap_name:
                raise AdapterError(
                    f"Unknown gap medium '{gap_name}'. "
                    f"Known: {sorted(_GAP_N.keys())}"
                )
            gap_n = 1.45  # default SiO2

        # --- Wavelength range ---
        # Try source_setting first, then sweep_plan (wavelength type), then default
        source_raw = _get_sf_value(spec, "simulation.source_setting")
        wl_range = _parse_wavelength_range(source_raw)

        # Validate that source_setting wavelength is actually a wavelength range
        # (not a parameter sweep range that got mis-parsed)
        if wl_range and (wl_range[0] < 0.2 or wl_range[1] > 30.0):
            wl_range = None  # Unreasonable for optical wavelength — probably a parameter range

        if not wl_range:
            # Try sweep_plan with wavelength type
            sweep_raw = _get_sf_value(spec, "simulation.sweep_plan")
            if sweep_raw and getattr(sweep_raw, "sweep_type", "") == "wavelength":
                sw_start = getattr(sweep_raw, "range_start", None)
                sw_end = getattr(sweep_raw, "range_end", None)
                sw_unit = getattr(sweep_raw, "unit", "nm")
                if sw_start and sw_end:
                    factor = 0.001 if sw_unit == "nm" else 1.0
                    wl_range = (sw_start * factor, sw_end * factor)

        if not wl_range:
            # Default wavelength range for visible/near-IR plasmonics
            wl_range = (0.4, 0.9)  # 400-900 nm
            import warnings
            warnings.warn(
                "Wavelength range not specified in spec. Defaulting to 400-900 nm. "
                "Set source_setting.wavelength_range explicitly for accurate results."
            )

        # --- Sweep plan (gap sweep) ---
        sweep_raw = _get_sf_value(spec, "simulation.sweep_plan")
        sweep_variable = None
        sweep_start = None
        sweep_end = None
        sweep_steps = None

        if sweep_raw and getattr(sweep_raw, "sweep_type", "") == "parameter":
            var = getattr(sweep_raw, "variable", "") or ""
            if "gap" in var.lower():
                sweep_variable = "gap_thickness_um"
                r_start = getattr(sweep_raw, "range_start", None)
                r_end = getattr(sweep_raw, "range_end", None)
                step = getattr(sweep_raw, "step", None)
                unit = getattr(sweep_raw, "unit", "nm")
                factor = 0.001 if unit == "nm" else 1.0
                if r_start is not None and r_end is not None:
                    sweep_start = r_start * factor
                    sweep_end = r_end * factor
                    if step and step > 0:
                        sweep_steps = int(round((r_end - r_start) / step)) + 1

        # Default gap thickness from sweep or fixed
        gap_thick_um = sweep_start if sweep_start else 0.005  # default 5nm

        # --- Postprocess ---
        postprocess: list[str] = []
        pp_raw = _get_sf_value(spec, "output.postprocess_target")
        if pp_raw and isinstance(pp_raw, list):
            for item in pp_raw:
                if isinstance(item, dict):
                    tt = item.get("target_type", "")
                    if tt in ("resonance_wavelength", "fwhm_extraction", "T2_extraction"):
                        postprocess.append(tt)
                elif isinstance(item, str):
                    if item in ("resonance_wavelength", "fwhm_extraction", "T2_extraction"):
                        postprocess.append(item)

        return MeepInputModel(
            particle_material=p_mat,
            particle_shape=shape,
            particle_radius_um=radius_um,
            film_material=film_mat,
            film_thickness_um=film_thick_um,
            gap_medium_n=gap_n,
            gap_thickness_um=gap_thick_um,
            wavelength_min_um=wl_range[0],
            wavelength_max_um=wl_range[1],
            sweep_variable=sweep_variable,
            sweep_start_um=sweep_start,
            sweep_end_um=sweep_end,
            sweep_steps=sweep_steps,
            postprocess=postprocess,
        )
