"""Meep adapter — translator from OpticalSpec to MeepInputModel.

Validates that the spec is compatible with the Meep nanoparticle-on-film path,
then extracts and converts fields from the nested StatusField structure into
the flat MeepInputModel.
"""

from __future__ import annotations

import re

from pydantic import BaseModel, Field

from optical_spec_agent.adapters.base import AdapterResult, BaseAdapter
from optical_spec_agent.models.spec import OpticalSpec

from .models import MeepInputModel
from .template import render_script


class AdapterError(Exception):
    """Standardized adapter error.

    Categories:
    - unsupported_path: spec targets a system/solver/software not supported
    - missing_required_field: a required spec field is absent or empty
    - invalid_adapter_input: field value cannot be processed by this adapter
    """

    def __init__(self, category: str, field: str, detail: str = ""):
        self.category = category
        self.field = field
        self.detail = detail
        parts = [f"[{category}]", field]
        if detail:
            parts.append(detail)
        super().__init__(" ".join(parts))


class AdapterValidationResult(BaseModel):
    """Adapter-specific readiness result for Meep script generation."""

    adapter_ready: bool = False
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    defaults_applied: list[str] = Field(default_factory=list)


# --- Centralized adapter defaults ---
_ADAPTER_DEFAULTS = {
    "gap_medium": "SiO2",
    "gap_medium_n": 1.45,
    "gap_thickness_nm": 5.0,
    "film_thickness_nm": 100.0,
    "wavelength_range_nm": (400.0, 900.0),
    "excitation_source": "plane_wave",
    "resolution": 50,
    "pml_thickness_um": 1.0,
    "freq_points": 200,
}

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

# Default film thickness when not specified — alias for readability
_DEFAULT_FILM_THICKNESS_NM = _ADAPTER_DEFAULTS["film_thickness_nm"]

# Supported shapes → Meep geometry type
_SHAPE_MAP = {
    "sphere": "sphere",
    "cube": "cube",
    "rod": "cylinder",
}

_SUPPORTED_SCRIPT_MODES = {"preview", "research_preview", "smoke"}
_SUPPORTED_BOUNDARY_TYPES = {"pml", "absorber"}
_SUPPORTED_MATERIAL_MODES = {
    "library",
    "dielectric_sanity",
    "particle_library_film_dielectric",
    "particle_dielectric_film_library",
}
_SUPPORTED_DIAGNOSTIC_PROFILES = {"normal", "low_cost", "physical_probe"}
_SUPPORTED_SOURCE_COMPONENTS = {"Ex", "Ey", "Ez"}
_SUPPORTED_STOP_STRATEGIES = {"decay", "fixed"}
_SUPPORTED_FLUX_MODES = {"closed_box", "single_plane"}

_LENGTH_TO_NM = {
    "nm": 1.0,
    "um": 1000.0,
    "μm": 1000.0,
    "mm": 1_000_000.0,
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


def _parse_length_nm(raw_value) -> float | None:
    """Parse a scalar length-like value into nm."""
    if raw_value is None:
        return None
    if isinstance(raw_value, (int, float)):
        return float(raw_value)

    m = re.search(r"([\d.]+)\s*(nm|μm|um|mm)?", str(raw_value), re.IGNORECASE)
    if not m:
        return None

    value = float(m.group(1))
    unit = (m.group(2) or "nm").lower()
    return value * _LENGTH_TO_NM.get(unit, 1.0)


def _extract_dimension_nm(dimensions: dict, keys: list[str]) -> float | None:
    """Try to extract a numeric value in nm from a dimensions dict."""
    if not isinstance(dimensions, dict):
        return None
    for key in keys:
        val = dimensions.get(key)
        if val is None:
            continue
        parsed = _parse_length_nm(val)
        if parsed is not None:
            return parsed
    return None


def _extract_gap_thickness_nm(spec: OpticalSpec) -> float | None:
    """Resolve a fixed gap thickness from geometry_definition or key_parameters."""
    geom_raw = _get_sf_value(spec, "geometry_material.geometry_definition")
    if geom_raw:
        dims = getattr(geom_raw, "dimensions", {}) or {}
        for key in ("gap_thickness_nm", "gap_nm", "gap", "间隙"):
            parsed = _parse_length_nm(dims.get(key))
            if parsed is not None:
                return parsed

    key_params = _get_sf_value(spec, "geometry_material.key_parameters")
    if isinstance(key_params, list):
        for item in key_params:
            if not isinstance(item, str) or not re.search(r"(gap|间隙|间距)", item, re.IGNORECASE):
                continue
            parsed = _parse_length_nm(item)
            if parsed is not None:
                return parsed

    return None


def _resolve_wavelength_range(spec: OpticalSpec) -> tuple[tuple[float, float] | None, bool]:
    """Return wavelength range in um and whether adapter default was needed."""
    source_raw = _get_sf_value(spec, "simulation.source_setting")
    wl_range = _parse_wavelength_range(source_raw)

    if wl_range and (wl_range[0] < 0.2 or wl_range[1] > 30.0):
        wl_range = None

    if not wl_range:
        sweep_raw = _get_sf_value(spec, "simulation.sweep_plan")
        if sweep_raw and getattr(sweep_raw, "sweep_type", "") == "wavelength":
            sw_start = getattr(sweep_raw, "range_start", None)
            sw_end = getattr(sweep_raw, "range_end", None)
            sw_unit = getattr(sweep_raw, "unit", "nm")
            if sw_start is not None and sw_end is not None:
                factor = 0.001 if sw_unit == "nm" else 1.0
                wl_range = (sw_start * factor, sw_end * factor)

    return wl_range, wl_range is None


def _normalize_script_mode(script_mode: str) -> str:
    """Normalize CLI / caller script modes into the internal adapter values."""
    normalized = (script_mode or "preview").strip().lower().replace("-", "_")
    if normalized not in _SUPPORTED_SCRIPT_MODES:
        raise ValueError(
            f"Unsupported Meep script mode '{script_mode}'. "
            f"Choose from {sorted(_SUPPORTED_SCRIPT_MODES)}."
        )
    return normalized


def _normalize_boundary_type(boundary_type: str) -> str:
    """Normalize research-preview boundary layer mode."""
    normalized = (boundary_type or "pml").strip().lower().replace("-", "_")
    if normalized not in _SUPPORTED_BOUNDARY_TYPES:
        raise ValueError(
            f"Unsupported Meep boundary_type '{boundary_type}'. "
            f"Choose from {sorted(_SUPPORTED_BOUNDARY_TYPES)}."
        )
    return normalized


def _normalize_material_mode(material_mode: str) -> str:
    """Normalize research-preview material mode."""
    normalized = (material_mode or "library").strip().lower().replace("-", "_")
    if normalized not in _SUPPORTED_MATERIAL_MODES:
        raise ValueError(
            f"Unsupported Meep material_mode '{material_mode}'. "
            f"Choose from {sorted(_SUPPORTED_MATERIAL_MODES)}."
        )
    return normalized


def _normalize_diagnostic_profile(diagnostic_profile: str) -> str:
    """Normalize research-preview diagnostic profile."""
    normalized = (diagnostic_profile or "normal").strip().lower().replace("-", "_")
    if normalized not in _SUPPORTED_DIAGNOSTIC_PROFILES:
        raise ValueError(
            f"Unsupported Meep diagnostic_profile '{diagnostic_profile}'. "
            f"Choose from {sorted(_SUPPORTED_DIAGNOSTIC_PROFILES)}."
        )
    return normalized


def _normalize_source_component(source_component: str) -> str:
    """Normalize research-preview source component."""
    normalized = (source_component or "Ez").strip()
    if normalized not in _SUPPORTED_SOURCE_COMPONENTS:
        raise ValueError(
            f"Unsupported Meep source_component '{source_component}'. "
            f"Choose from {sorted(_SUPPORTED_SOURCE_COMPONENTS)}."
        )
    return normalized


def _normalize_stop_strategy(stop_strategy: str | None) -> str | None:
    """Normalize optional research-preview stop strategy."""
    if stop_strategy is None:
        return None
    normalized = stop_strategy.strip().lower().replace("-", "_")
    if normalized not in _SUPPORTED_STOP_STRATEGIES:
        raise ValueError(
            f"Unsupported Meep stop_strategy '{stop_strategy}'. "
            f"Choose from {sorted(_SUPPORTED_STOP_STRATEGIES)}."
        )
    return normalized


def _normalize_flux_mode(flux_mode: str) -> str:
    """Normalize research-preview flux mode."""
    normalized = (flux_mode or "closed_box").strip().lower().replace("-", "_")
    if normalized not in _SUPPORTED_FLUX_MODES:
        raise ValueError(
            f"Unsupported Meep flux_mode '{flux_mode}'. "
            f"Choose from {sorted(_SUPPORTED_FLUX_MODES)}."
        )
    return normalized


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

    def validate_ready(self, spec: OpticalSpec) -> AdapterValidationResult:
        """Check whether a spec is ready for Meep script generation."""
        errors: list[str] = []
        warnings: list[str] = []
        defaults_applied: list[str] = []

        phys_sys = _get_sf_value(spec, "physics.physical_system")
        solver = _get_sf_value(spec, "simulation.solver_method")
        software = _get_sf_value(spec, "simulation.software_tool")
        source_type = _get_sf_value(spec, "simulation.excitation_source")

        if phys_sys != "nanoparticle_on_film":
            errors.append("physics.physical_system 必须为 nanoparticle_on_film")
        if solver != "fdtd":
            errors.append("simulation.solver_method 必须为 fdtd")
        if software != "meep":
            errors.append("simulation.software_tool 必须为 meep")
        if source_type and source_type != "plane_wave":
            errors.append("Meep adapter 当前仅支持 plane_wave 激励")
        elif not source_type:
            defaults_applied.append("excitation_source: plane_wave")
            warnings.append("simulation.excitation_source 缺失，Meep adapter 将按 plane_wave 生成脚本")

        particle_raw = _get_sf_value(spec, "geometry_material.particle_info")
        if not particle_raw:
            errors.append("缺少 geometry_material.particle_info")
        else:
            p_type = getattr(particle_raw, "particle_type", "") or ""
            p_mat = getattr(particle_raw, "material", "") or ""
            p_dims = getattr(particle_raw, "dimensions", {}) or {}

            if p_type not in _SHAPE_MAP:
                errors.append("particle_info.particle_type 必须是 sphere/cube/rod 之一")
            if not p_mat:
                errors.append("缺少 particle_info.material")

            size_keys = ["直径", "diameter_nm", "diameter"]
            if p_type == "cube":
                size_keys = ["边长", "edge_length_nm", "edge_length", *size_keys]
            particle_size_nm = _extract_dimension_nm(p_dims, size_keys)
            if particle_size_nm is None:
                errors.append("缺少可解析的 particle size（例如 80 nm 金纳米球 或 直径 80 nm）")

        film_raw = _get_sf_value(spec, "geometry_material.substrate_or_film_info")
        if not film_raw:
            errors.append("缺少 geometry_material.substrate_or_film_info")
        else:
            film_mat = getattr(film_raw, "film_material", "") or ""
            if not film_mat:
                errors.append("缺少 substrate_or_film_info.film_material")
            film_thick_nm = _parse_length_nm(getattr(film_raw, "film_thickness", "") or "")
            if film_thick_nm is None:
                defaults_applied.append(f"film_thickness: {_DEFAULT_FILM_THICKNESS_NM:.0f} nm")
                warnings.append("film_thickness 缺失，Meep adapter 将使用 100 nm 默认金膜厚度")

        gap_name = _get_sf_value(spec, "geometry_material.gap_medium") or ""
        if gap_name:
            if _GAP_N.get(gap_name) is None:
                errors.append(f"未知 gap_medium: {gap_name}")
        else:
            defaults_applied.append(f"gap_medium: {_ADAPTER_DEFAULTS['gap_medium']} (n={_ADAPTER_DEFAULTS['gap_medium_n']})")
            warnings.append("gap_medium 缺失，Meep adapter 将使用 SiO2 默认间隙介质")

        wl_range, wl_defaulted = _resolve_wavelength_range(spec)
        if wl_defaulted:
            wl_min, wl_max = _ADAPTER_DEFAULTS["wavelength_range_nm"]
            defaults_applied.append(f"wavelength_range: {wl_min:.0f}–{wl_max:.0f} nm")
            warnings.append("wavelength_range 缺失，Meep adapter 将使用 400–900 nm 默认波长范围")

        gap_thick_nm = _extract_gap_thickness_nm(spec)
        sweep_raw = _get_sf_value(spec, "simulation.sweep_plan")
        has_gap_sweep = bool(
            sweep_raw
            and getattr(sweep_raw, "sweep_type", "") == "parameter"
            and "gap" in (getattr(sweep_raw, "variable", "") or "").lower()
        )
        if gap_thick_nm is None and not has_gap_sweep:
            defaults_applied.append(f"gap_thickness: {_ADAPTER_DEFAULTS['gap_thickness_nm']:.0f} nm")
            warnings.append("gap thickness 缺失，Meep adapter 将使用 5 nm 默认间隙厚度")

        observables = _get_sf_value(spec, "output.output_observables")
        if isinstance(observables, list) and "scattering_spectrum" not in observables:
            warnings.append("output.output_observables 未显式包含 scattering_spectrum，生成脚本仍会输出散射谱预览")

        return AdapterValidationResult(
            adapter_ready=(len(errors) == 0),
            errors=errors,
            warnings=warnings,
            defaults_applied=defaults_applied,
        )

    def generate(
        self,
        spec: OpticalSpec,
        script_mode: str = "preview",
        *,
        boundary_type: str = "pml",
        courant: float | None = None,
        eps_averaging: bool | None = None,
        material_mode: str = "library",
        diagnostic_profile: str = "normal",
        source_component: str = "Ez",
        stop_strategy: str | None = None,
        fixed_run_time: float | None = None,
        decay_threshold: float | None = None,
        flux_mode: str = "closed_box",
        resolution: int | None = None,
        freq_points: int | None = None,
    ) -> AdapterResult:
        normalized_mode = _normalize_script_mode(script_mode)
        normalized_boundary_type = _normalize_boundary_type(boundary_type)
        normalized_material_mode = _normalize_material_mode(material_mode)
        normalized_diagnostic_profile = _normalize_diagnostic_profile(diagnostic_profile)
        normalized_source_component = _normalize_source_component(source_component)
        normalized_stop_strategy = _normalize_stop_strategy(stop_strategy)
        normalized_flux_mode = _normalize_flux_mode(flux_mode)

        if not self.can_handle(spec):
            raise AdapterError(
                "unsupported_path", "physical_system/solver_method/software_tool",
                "Meep adapter requires nanoparticle_on_film + fdtd + meep",
            )

        readiness = self.validate_ready(spec)
        source_type = _get_sf_value(spec, "simulation.excitation_source")
        if source_type and source_type != "plane_wave":
            raise AdapterError(
                "unsupported_path",
                "simulation.excitation_source",
                "Meep adapter currently supports plane_wave only",
            )

        model = self._translate(
            spec,
            script_mode=normalized_mode,
            boundary_type=normalized_boundary_type,
            courant=courant,
            eps_averaging=eps_averaging,
            material_mode=normalized_material_mode,
            diagnostic_profile=normalized_diagnostic_profile,
            source_component=normalized_source_component,
            stop_strategy=normalized_stop_strategy,
            fixed_run_time=fixed_run_time,
            decay_threshold=decay_threshold,
            flux_mode=normalized_flux_mode,
            resolution=resolution,
            freq_points=freq_points,
        )
        script = render_script(model)
        return AdapterResult(
            tool="meep",
            content=script,
            language="python",
        )

    def _translate(
        self,
        spec: OpticalSpec,
        script_mode: str = "preview",
        *,
        boundary_type: str = "pml",
        courant: float | None = None,
        eps_averaging: bool | None = None,
        material_mode: str = "library",
        diagnostic_profile: str = "normal",
        source_component: str = "Ez",
        stop_strategy: str | None = None,
        fixed_run_time: float | None = None,
        decay_threshold: float | None = None,
        flux_mode: str = "closed_box",
        resolution: int | None = None,
        freq_points: int | None = None,
    ) -> MeepInputModel:
        normalized_mode = _normalize_script_mode(script_mode)
        normalized_boundary_type = _normalize_boundary_type(boundary_type)
        normalized_material_mode = _normalize_material_mode(material_mode)
        normalized_diagnostic_profile = _normalize_diagnostic_profile(diagnostic_profile)
        normalized_source_component = _normalize_source_component(source_component)
        normalized_stop_strategy = _normalize_stop_strategy(stop_strategy)
        normalized_flux_mode = _normalize_flux_mode(flux_mode)
        resolved_resolution = resolution or _ADAPTER_DEFAULTS["resolution"]
        pml_thickness_um = _ADAPTER_DEFAULTS["pml_thickness_um"]
        resolved_freq_points = freq_points or _ADAPTER_DEFAULTS["freq_points"]
        if normalized_mode == "research_preview" and normalized_diagnostic_profile == "low_cost":
            normalized_boundary_type = "absorber"
            normalized_material_mode = "dielectric_sanity"
            courant = 0.25 if courant is None else courant
            resolved_resolution = resolution or 8
            pml_thickness_um = 0.5
            resolved_freq_points = freq_points or 5
            normalized_stop_strategy = normalized_stop_strategy or "fixed"
            fixed_run_time = fixed_run_time or 30
            decay_threshold = decay_threshold or 1e-3
        defaults_applied: list[str] = []

        # --- Particle info ---
        particle_raw = _get_sf_value(spec, "geometry_material.particle_info")
        if not particle_raw:
            raise AdapterError("missing_required_field", "geometry_material.particle_info")

        p_type = getattr(particle_raw, "particle_type", "") or ""
        p_mat = getattr(particle_raw, "material", "") or ""
        p_dims = getattr(particle_raw, "dimensions", {}) or {}

        shape = _SHAPE_MAP.get(p_type)
        if not shape:
            raise AdapterError(
                "unsupported_path", "particle_shape",
                f"unsupported '{p_type}', supported: {list(_SHAPE_MAP)}",
            )

        # Extract radius from dimensions
        size_keys = ["直径", "diameter_nm", "diameter"]
        if p_type == "cube":
            size_keys = ["边长", "edge_length_nm", "edge_length", *size_keys]
        diameter_nm = _extract_dimension_nm(p_dims, size_keys)
        if diameter_nm is None:
            # fallback: try to find any numeric dimension and halve it
            first_dim = _extract_dimension_nm(p_dims, list(p_dims.keys())[:1]) if p_dims else None
            if first_dim:
                diameter_nm = first_dim
            else:
                raise AdapterError(
                    "invalid_adapter_input", "particle_info.dimensions",
                    "cannot determine particle size; add a '直径' or 'diameter' key",
                )
        radius_um = (diameter_nm / 2.0) / 1000.0

        # --- Film info ---
        film_raw = _get_sf_value(spec, "geometry_material.substrate_or_film_info")
        if not film_raw:
            raise AdapterError("missing_required_field", "geometry_material.substrate_or_film_info")

        film_mat = getattr(film_raw, "film_material", "") or ""
        if not film_mat:
            raise AdapterError("missing_required_field", "substrate_or_film_info.film_material")

        film_thick_str = getattr(film_raw, "film_thickness", "") or ""
        film_thick_nm = _DEFAULT_FILM_THICKNESS_NM
        parsed_film_thickness = _parse_length_nm(film_thick_str)
        if parsed_film_thickness is not None:
            film_thick_nm = parsed_film_thickness
        else:
            defaults_applied.append(f"film_thickness: {film_thick_nm:.0f} nm")
        film_thick_um = film_thick_nm / 1000.0

        # --- Gap medium ---
        gap_name = _get_sf_value(spec, "geometry_material.gap_medium") or ""
        gap_n = _GAP_N.get(gap_name)
        if gap_n is None:
            if gap_name:
                raise AdapterError(
                    "invalid_adapter_input", "geometry_material.gap_medium",
                    f"unknown '{gap_name}', known: {sorted(_GAP_N.keys())}",
                )
            gap_name = _ADAPTER_DEFAULTS["gap_medium"]
            gap_n = _ADAPTER_DEFAULTS["gap_medium_n"]
            defaults_applied.append(f"gap_medium: {_ADAPTER_DEFAULTS['gap_medium']} (n={gap_n})")

        # --- Wavelength range ---
        # Try source_setting first, then sweep_plan (wavelength type), then default
        wl_range, wl_defaulted = _resolve_wavelength_range(spec)
        if wl_defaulted:
            wl_min, wl_max = _ADAPTER_DEFAULTS["wavelength_range_nm"]
            wl_range = (wl_min / 1000.0, wl_max / 1000.0)
            defaults_applied.append(f"wavelength_range: {wl_min:.0f}–{wl_max:.0f} nm")
            import warnings
            warnings.warn(
                "Wavelength range not specified in spec. Defaulting to "
                f"{wl_min:.0f}–{wl_max:.0f} nm. Set source_setting.wavelength_range "
                "explicitly for accurate results."
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

        # Default gap thickness from explicit geometry, sweep, or fixed fallback
        explicit_gap_nm = _extract_gap_thickness_nm(spec)
        if explicit_gap_nm is not None:
            gap_thick_um = explicit_gap_nm / 1000.0
        elif sweep_start:
            gap_thick_um = sweep_start
        else:
            gap_thick_um = _ADAPTER_DEFAULTS["gap_thickness_nm"] / 1000.0

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
            script_mode=normalized_mode,
            particle_material=p_mat,
            particle_shape=shape,
            particle_radius_um=radius_um,
            film_material=film_mat,
            film_thickness_um=film_thick_um,
            gap_medium_name=gap_name,
            gap_medium_n=gap_n,
            gap_thickness_um=gap_thick_um,
            wavelength_min_um=wl_range[0],
            wavelength_max_um=wl_range[1],
            resolution=resolved_resolution,
            pml_thickness_um=pml_thickness_um,
            freq_points=resolved_freq_points,
            boundary_type=normalized_boundary_type,
            courant=courant,
            eps_averaging=eps_averaging,
            material_mode=normalized_material_mode,
            diagnostic_profile=normalized_diagnostic_profile,
            source_component=normalized_source_component,
            stop_strategy=normalized_stop_strategy,
            fixed_run_time=fixed_run_time,
            decay_threshold=decay_threshold,
            flux_mode=normalized_flux_mode,
            sweep_variable=sweep_variable,
            sweep_start_um=sweep_start,
            sweep_end_um=sweep_end,
            sweep_steps=sweep_steps,
            postprocess=postprocess,
            smoke=(normalized_mode == "smoke"),
            defaults_applied=defaults_applied,
        )
