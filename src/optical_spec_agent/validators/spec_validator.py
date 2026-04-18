"""Spec validation — completeness and cross-field consistency rules."""

from __future__ import annotations

from optical_spec_agent.models.base import ValidationStatus
from optical_spec_agent.models.spec import OpticalSpec


# ---------------------------------------------------------------------------
# Required fields per task_type
# ---------------------------------------------------------------------------

# Fields that are *always* required
_BASE_REQUIRED = [
    "task.task_type",
    "task.research_goal",
]

# Additional required fields when task_type == "simulation"
_SIMULATION_REQUIRED = [
    "simulation.solver_method",
    "simulation.software_tool",
    "simulation.excitation_source",
    "simulation.source_setting",
    "simulation.boundary_condition",
    "simulation.monitor_setting",
]

# Additional required fields when task_type == "fitting"
_FITTING_REQUIRED = [
    "output.output_observables",
]

# Recommended fields (warnings if missing)
_RECOMMENDED = [
    "physics.physical_mechanism",
    "physics.structure_type",
    "geometry_material.material_system",
    "geometry_material.key_parameters",
    "simulation.polarization",
    "output.output_observables",
]


class SpecValidator:
    """Validates an OpticalSpec for completeness and consistency."""

    def validate(self, spec: OpticalSpec) -> OpticalSpec:
        """Run validation and update spec.validation_status in-place."""
        errors: list[str] = []
        warnings: list[str] = []

        spec.collect_all()
        missing_set = set(spec.missing_fields)
        confirmed = spec.confirmed_fields
        inferred = spec.inferred_fields

        # --- Determine required fields based on task_type ---
        task_type = self._get_field_value(spec, "task.task_type")
        required = list(_BASE_REQUIRED)

        if task_type == "simulation":
            required.extend(_SIMULATION_REQUIRED)
        elif task_type == "fitting":
            required.extend(_FITTING_REQUIRED)

        # --- Check required fields ---
        for path in required:
            if path in missing_set:
                errors.append(f"缺少必填字段: {path}")

        # --- Check recommended fields ---
        for path in _RECOMMENDED:
            if path in missing_set:
                warnings.append(f"建议补充字段: {path}")

        # --- Task-type-specific semantic rules ---
        self._check_simulation_rules(spec, errors, warnings)
        self._check_physical_system_rules(spec, errors, warnings)
        self._check_postprocess_rules(spec, errors, warnings)
        self._check_consistency(spec, errors, warnings)

        spec.validation_status = ValidationStatus(
            is_executable=(len(errors) == 0),
            errors=errors,
            warnings=warnings,
        )
        return spec

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _get_field_value(self, spec: OpticalSpec, dotted_path: str) -> str | None:
        """Get the value of a StatusField by dotted path like 'task.task_type'."""
        parts = dotted_path.split(".", 1)
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

    def _is_missing(self, spec: OpticalSpec, dotted_path: str) -> bool:
        return dotted_path in spec.missing_fields

    # ------------------------------------------------------------------
    # Semantic rule groups
    # ------------------------------------------------------------------

    def _check_simulation_rules(
        self, spec: OpticalSpec, errors: list[str], warnings: list[str]
    ) -> None:
        """Rules specific to task_type == simulation."""
        task_type = self._get_field_value(spec, "task.task_type")
        if task_type != "simulation":
            return

        solver = self._get_field_value(spec, "simulation.solver_method")
        software = self._get_field_value(spec, "simulation.software_tool")

        # solver_method / software_tool consistency
        if solver and software:
            _solver_sw_warnings(solver, software, warnings)

        # FDTD-specific: source + boundary + monitor minimum executable check
        if solver == "fdtd":
            fdtd_critical = [
                ("simulation.excitation_source", "激励源"),
                ("simulation.source_setting", "光源设置"),
                ("simulation.boundary_condition", "边界条件"),
                ("simulation.monitor_setting", "监视器设置"),
            ]
            missing_critical = []
            for path, label in fdtd_critical:
                if self._is_missing(spec, path):
                    missing_critical.append(label)
            if len(missing_critical) >= 3:
                errors.append(
                    f"FDTD 仿真缺少关键设置（{', '.join(missing_critical)}），无法生成可执行仿真脚本"
                )

        # FEM-specific: boundary + monitor minimum executable check
        if solver == "fem":
            fem_critical = [
                ("simulation.boundary_condition", "边界条件"),
                ("simulation.monitor_setting", "监视器设置"),
            ]
            missing_fem = []
            for path, label in fem_critical:
                if self._is_missing(spec, path):
                    missing_fem.append(label)
            if len(missing_fem) >= 2:
                errors.append(
                    f"FEM 仿真缺少关键设置（{', '.join(missing_fem)}），无法生成可执行仿真脚本"
                )

        # dimension vs structure
        dim = self._get_field_value(spec, "physics.model_dimension")
        struct = self._get_field_value(spec, "physics.structure_type")
        if dim == "2d" and struct in ("single_particle", "array"):
            warnings.append("2d 模型可能不适合颗粒/阵列结构，建议确认")

    def _check_physical_system_rules(
        self, spec: OpticalSpec, errors: list[str], warnings: list[str]
    ) -> None:
        """Rules based on physical_system type."""
        phys_sys = self._get_field_value(spec, "physics.physical_system")

        if phys_sys == "nanoparticle_on_film":
            # particle_info / substrate_or_film_info / gap_medium should exist
            missing_geom = []
            for path, label in [
                ("geometry_material.particle_info", "颗粒信息"),
                ("geometry_material.substrate_or_film_info", "薄膜/基底信息"),
                ("geometry_material.gap_medium", "间隙介质"),
            ]:
                if self._is_missing(spec, path):
                    missing_geom.append(label)

            if len(missing_geom) >= 3:
                errors.append(
                    f"nanoparticle_on_film 体系严重缺少几何信息（{', '.join(missing_geom)}），无法构建仿真结构"
                )
            elif len(missing_geom) >= 1:
                for label in missing_geom:
                    warnings.append(
                        f"物理系统为 nanoparticle_on_film，建议补充{label}"
                    )

        if phys_sys == "waveguide":
            if self._is_missing(spec, "geometry_material.geometry_definition"):
                warnings.append("波导系统建议补充 geometry_definition")

        # physical_system + structure_type combination consistency
        struct = self._get_field_value(spec, "physics.structure_type")
        if phys_sys and struct:
            _valid_combos = {
                "nanoparticle_on_film": {"sphere_on_film", "rod_on_film", "cube_on_film", "cross_structure", "single_particle", "other"},
                "single_particle": {"single_particle"},
                "waveguide": {"waveguide"},
                "grating": {"gratings"},
                "metasurface": {"metasurface", "array"},
                "particle_array": {"array"},
                "thin_film": {"film"},
                "multilayer": {"multilayer"},
                "coupled_system": {"other"},
            }
            valid = _valid_combos.get(phys_sys)
            if valid and struct not in valid:
                warnings.append(
                    f"physical_system={phys_sys} 与 structure_type={struct} 组合不常见，请确认"
                )

    def _check_postprocess_rules(
        self, spec: OpticalSpec, errors: list[str], warnings: list[str]
    ) -> None:
        """Rules linking postprocess_target to output_observables."""
        pp_raw = self._get_field_value(spec, "output.postprocess_target")
        if not pp_raw:
            return

        # pp_raw may be a list of dicts from PostprocessTargetSpec
        target_types: list[str] = []
        if isinstance(pp_raw, list):
            for item in pp_raw:
                if isinstance(item, dict) and "target_type" in item:
                    target_types.append(item["target_type"])
                elif isinstance(item, str):
                    target_types.append(item)
        elif isinstance(pp_raw, str):
            target_types.append(pp_raw)

        # If FWHM or T2 extraction → need spectrum-type output (ERROR level)
        needs_spectrum = {"fwhm_extraction", "T2_extraction", "lorentzian_fit", "peak_finding"}
        if any(t in needs_spectrum for t in target_types):
            obs_raw = self._get_field_value(spec, "output.output_observables")
            obs_list = obs_raw if isinstance(obs_raw, list) else []
            spectrum_types = {
                "spectrum", "scattering_spectrum", "transmission_spectrum",
                "reflection_spectrum", "absorption_spectrum", "cross_section",
                "FWHM", "resonance_wavelength",
            }
            has_spectrum = any(o in spectrum_types for o in obs_list)
            if not has_spectrum:
                errors.append(
                    "后处理包含 FWHM/T2/拟合 目标，但 output_observables 缺少 spectrum 类输出，无法执行后处理"
                )

        # If postprocess mentions mode analysis → need mode_profile or field_distribution
        needs_mode = {"band_diagram"}
        if any(t in needs_mode for t in target_types):
            obs_raw = self._get_field_value(spec, "output.output_observables")
            obs_list = obs_raw if isinstance(obs_raw, list) else []
            mode_types = {"mode_profile", "field_distribution"}
            if not any(o in mode_types for o in obs_list):
                warnings.append(
                    "后处理包含能带分析目标，建议补充 mode_profile 或 field_distribution"
                )

    def _check_consistency(
        self, spec: OpticalSpec, errors: list[str], warnings: list[str]
    ) -> None:
        """General cross-field consistency rules."""
        # If model_dimension == axisymmetric, solver should support it
        dim = self._get_field_value(spec, "physics.model_dimension")
        solver = self._get_field_value(spec, "simulation.solver_method")
        if dim == "axisymmetric" and solver == "fdtd":
            warnings.append("axisymmetric 通常用 FEM 而非 FDTD 实现，请确认")


def _solver_sw_warnings(solver: str, software: str, warnings: list[str]) -> None:
    """Emit warnings for solver-software mismatches."""
    pairs: dict[str, set[str]] = {
        "fdtd": {"meep", "lumerical"},
        "fem": {"comsol"},
        "rcwa": {"python", "matlab", "custom"},
    }
    expected = pairs.get(solver)
    if expected and software not in expected and software != "not_specified":
        warnings.append(f"{solver.upper()} 通常用 {'/'.join(expected)}，当前指定 {software}")
