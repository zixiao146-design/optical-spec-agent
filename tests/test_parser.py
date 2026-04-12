"""Comprehensive tests for the RuleBasedParser and MockLLMParser."""

from optical_spec_agent.models.base import (
    GeometryDefinition,
    MaterialSystem,
    ParticleInfo,
    SourceSetting,
    SweepPlan,
)
from optical_spec_agent.parsers.rule_based import RuleBasedParser
from optical_spec_agent.parsers.llm_placeholder import LLMParser


# ═══════════════════════════════════════════════════════════════════════════
# Chinese inputs (5+)
# ═══════════════════════════════════════════════════════════════════════════

TEXT_GAP_PLASMON_SWEEP = (
    "研究金纳米球-金膜体系中 gap 从 5 到 25 nm 变化对散射谱主峰线宽和退相位时间的影响，"
    "使用 Meep FDTD，提取共振波长、FWHM 和 T2。"
)

TEXT_ASYM_CROSS = (
    "建模非对称金纳米十字结构，两臂长度分别为120nm和80nm，宽40nm，厚30nm，"
    "放在SiO2基底上。用Lumerical FDTD计算偏振相关的散射谱，"
    "x偏振和y偏振都要做，波长范围500-1200nm。"
)

TEXT_COMSOL_WAVEGUIDE = (
    "COMSOL模式分析：Si3N4脊波导（宽800nm，高400nm，蚀刻深度250nm），"
    "SiO2下包层，上包层为空气，计算1.55μm波长下的基模有效折射率和模场分布，"
    "TE和TM模式都要计算。"
)

TEXT_LORENTZIAN_FIT = (
    "对实验测得的散射谱进行Lorentzian拟合，数据范围500-900nm，"
    "主峰位于680nm附近，提取FWHM和T2退相干时间。"
    "用Python scipy做曲线拟合。"
)

TEXT_GAP_PLASMON_CUBIC = (
    "用FDTD仿真一个gap plasmon体系：80nm金纳米立方体放在金膜上，"
    "间隙填充SiO2（5 nm），用总场散射场(TFSF)光源正入射，"
    "扫间隙厚度从2nm到20nm，步长2nm，计算散射截面和吸收截面。"
    "波长范围400-900nm。"
)

TEXT_METASURFACE = (
    "设计介质超表面单元结构，周期400nm，TiO2柱高600nm，"
    "用RCWA计算透射谱和反射谱，波长范围400-800nm。"
)


class TestChineseInput01:
    """金纳米球-金膜 gap 扫描"""

    def test_physical_system(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_SWEEP)
        assert spec.physics.physical_system.value == "nanoparticle_on_film"

    def test_structure_type(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_SWEEP)
        assert spec.physics.structure_type.value == "sphere_on_film"

    def test_solver_method(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_SWEEP)
        assert spec.simulation.solver_method.value == "fdtd"

    def test_software_tool(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_SWEEP)
        assert spec.simulation.software_tool.value == "meep"

    def test_sweep_variable(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_SWEEP)
        sweep = spec.simulation.sweep_plan.value
        assert isinstance(sweep, SweepPlan)
        assert sweep.variable == "gap_nm"
        assert sweep.range_start == 5.0
        assert sweep.range_end == 25.0

    def test_output_observables(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_SWEEP)
        obs = spec.output.output_observables.value
        assert isinstance(obs, list)
        assert "scattering_spectrum" in obs

    def test_postprocess_targets(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_SWEEP)
        pp = spec.output.postprocess_target.value
        assert isinstance(pp, list)
        target_types = [p["target_type"] for p in pp]
        assert "resonance_wavelength" in target_types
        assert "fwhm_extraction" in target_types
        assert "T2_extraction" in target_types

    def test_task_type(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_SWEEP)
        assert spec.task.task_type.value in ("simulation", "data_analysis")

    def test_materials(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_SWEEP)
        ms = spec.geometry_material.material_system.value
        assert isinstance(ms, MaterialSystem)
        names = [m.name for m in ms.materials]
        assert "Au" in names


class TestChineseInput02:
    """非对称金纳米十字"""

    def test_cross_structure(self, rule_parser):
        spec = rule_parser.parse(TEXT_ASYM_CROSS)
        assert spec.physics.structure_type.value == "cross_structure"

    def test_solver_software(self, rule_parser):
        spec = rule_parser.parse(TEXT_ASYM_CROSS)
        assert spec.simulation.solver_method.value == "fdtd"
        assert spec.simulation.software_tool.value == "lumerical"

    def test_polarization(self, rule_parser):
        spec = rule_parser.parse(TEXT_ASYM_CROSS)
        assert spec.simulation.polarization.value == "linear_x"

    def test_sweep_wavelength(self, rule_parser):
        spec = rule_parser.parse(TEXT_ASYM_CROSS)
        sweep = spec.simulation.sweep_plan.value
        assert isinstance(sweep, SweepPlan)
        assert sweep.range_start == 500.0
        assert sweep.range_end == 1200.0

    def test_substrate(self, rule_parser):
        spec = rule_parser.parse(TEXT_ASYM_CROSS)
        sub = spec.geometry_material.substrate_or_film_info.value
        assert sub is not None


class TestChineseInput03:
    """COMSOL 波导"""

    def test_task_type(self, rule_parser):
        spec = rule_parser.parse(TEXT_COMSOL_WAVEGUIDE)
        assert spec.task.task_type.value == "simulation"

    def test_solver_fem(self, rule_parser):
        spec = rule_parser.parse(TEXT_COMSOL_WAVEGUIDE)
        assert spec.simulation.solver_method.value == "fem"

    def test_software_comsol(self, rule_parser):
        spec = rule_parser.parse(TEXT_COMSOL_WAVEGUIDE)
        assert spec.simulation.software_tool.value == "comsol"

    def test_waveguide_system(self, rule_parser):
        spec = rule_parser.parse(TEXT_COMSOL_WAVEGUIDE)
        assert spec.physics.physical_system.value == "waveguide"

    def test_mode_profile_observable(self, rule_parser):
        spec = rule_parser.parse(TEXT_COMSOL_WAVEGUIDE)
        obs = spec.output.output_observables.value
        assert "mode_profile" in obs


class TestChineseInput04:
    """Lorentzian 拟合"""

    def test_task_type_fitting(self, rule_parser):
        spec = rule_parser.parse(TEXT_LORENTZIAN_FIT)
        assert spec.task.task_type.value == "fitting"

    def test_software_python(self, rule_parser):
        spec = rule_parser.parse(TEXT_LORENTZIAN_FIT)
        assert spec.simulation.software_tool.value == "python"

    def test_postprocess_has_fwhm_t2(self, rule_parser):
        spec = rule_parser.parse(TEXT_LORENTZIAN_FIT)
        pp = spec.output.postprocess_target.value
        target_types = [p["target_type"] for p in pp]
        assert "fwhm_extraction" in target_types
        assert "T2_extraction" in target_types


class TestChineseInput05:
    """Gap plasmon 纳米立方"""

    def test_nanoparticle_on_film(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_CUBIC)
        assert spec.physics.physical_system.value == "nanoparticle_on_film"

    def test_cube_geometry(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_CUBIC)
        geom = spec.geometry_material.geometry_definition.value
        assert isinstance(geom, GeometryDefinition)
        assert geom.geometry_type == "cube"

    def test_tfsf_source(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_CUBIC)
        assert spec.simulation.excitation_source.value == "tfsf"

    def test_sweep_plan(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_CUBIC)
        sweep = spec.simulation.sweep_plan.value
        assert isinstance(sweep, SweepPlan)
        assert sweep.range_start == 2.0
        assert sweep.range_end == 20.0
        assert sweep.step == 2.0

    def test_mechanism_plasmon(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_CUBIC)
        assert spec.physics.physical_mechanism.value in ("gap_plasmon", "plasmon")


class TestChineseInput06:
    """超表面"""

    def test_metasurface_system(self, rule_parser):
        spec = rule_parser.parse(TEXT_METASURFACE)
        assert spec.physics.physical_system.value == "metasurface"

    def test_rcwa_solver(self, rule_parser):
        spec = rule_parser.parse(TEXT_METASURFACE)
        assert spec.simulation.solver_method.value == "rcwa"


# ═══════════════════════════════════════════════════════════════════════════
# English inputs (2+)
# ═══════════════════════════════════════════════════════════════════════════

TEXT_EN_GAP_PLASMON = (
    "Simulate a gold nanosphere-on-film gap plasmon system using Meep FDTD. "
    "Gap varies from 3 to 15 nm, calculate scattering spectrum and field enhancement, "
    "extract resonance wavelength and FWHM."
)

TEXT_EN_WAVEGUIDE = (
    "COMSOL FEM mode analysis of a silicon ridge waveguide, "
    "width 500nm, height 220nm, SiO2 BOX, air top cladding. "
    "Calculate effective index and mode profile at 1550nm."
)


class TestEnglishInput01:
    """English gap plasmon"""

    def test_physical_system(self, rule_parser):
        spec = rule_parser.parse(TEXT_EN_GAP_PLASMON)
        assert spec.physics.physical_system.value == "nanoparticle_on_film"

    def test_solver_software(self, rule_parser):
        spec = rule_parser.parse(TEXT_EN_GAP_PLASMON)
        assert spec.simulation.solver_method.value == "fdtd"
        assert spec.simulation.software_tool.value == "meep"

    def test_sweep_variable(self, rule_parser):
        spec = rule_parser.parse(TEXT_EN_GAP_PLASMON)
        sweep = spec.simulation.sweep_plan.value
        assert isinstance(sweep, SweepPlan)
        assert sweep.variable == "gap_nm"

    def test_output_observables(self, rule_parser):
        spec = rule_parser.parse(TEXT_EN_GAP_PLASMON)
        obs = spec.output.output_observables.value
        assert "scattering_spectrum" in obs
        assert "field_enhancement" in obs

    def test_postprocess(self, rule_parser):
        spec = rule_parser.parse(TEXT_EN_GAP_PLASMON)
        pp = spec.output.postprocess_target.value
        target_types = [p["target_type"] for p in pp]
        assert "resonance_wavelength" in target_types
        assert "fwhm_extraction" in target_types


class TestEnglishInput02:
    """English waveguide"""

    def test_waveguide_system(self, rule_parser):
        spec = rule_parser.parse(TEXT_EN_WAVEGUIDE)
        assert spec.physics.physical_system.value == "waveguide"

    def test_fem_comsol(self, rule_parser):
        spec = rule_parser.parse(TEXT_EN_WAVEGUIDE)
        assert spec.simulation.solver_method.value == "fem"
        assert spec.simulation.software_tool.value == "comsol"

    def test_mode_output(self, rule_parser):
        spec = rule_parser.parse(TEXT_EN_WAVEGUIDE)
        obs = spec.output.output_observables.value
        assert "mode_profile" in obs


# ═══════════════════════════════════════════════════════════════════════════
# Inference rules
# ═══════════════════════════════════════════════════════════════════════════

class TestInferenceRules:
    """Test post-hoc inference chain."""

    def test_gap_plasmon_infers_fdtd(self, rule_parser):
        text = "研究 gap plasmon 体系，金纳米球直径100nm"
        spec = rule_parser.parse(text)
        # If no solver specified, should infer fdtd for gap plasmon
        assert spec.simulation.solver_method.value == "fdtd"
        assert spec.simulation.solver_method.status == "inferred"

    def test_fwhm_infers_lorentzian(self, rule_parser):
        text = "提取散射谱的FWHM和T2"
        spec = rule_parser.parse(text)
        if spec.output.postprocess_target.status != "missing":
            pp = spec.output.postprocess_target.value
            target_types = [p["target_type"] for p in pp]
            assert "lorentzian_fit" in target_types

    def test_nanoparticle_on_film_infers_3d(self, rule_parser):
        text = "金纳米球放在金膜上，gap=5nm，计算散射"
        spec = rule_parser.parse(text)
        assert spec.physics.model_dimension.value == "3d"

    def test_scattering_spectrum_refinement(self, rule_parser):
        """Generic 'spectrum' should be refined to 'scattering_spectrum'."""
        text = "计算散射谱，波长400-800nm"
        spec = rule_parser.parse(text)
        obs = spec.output.output_observables.value
        assert "scattering_spectrum" in obs
        assert "spectrum" not in obs

    def test_inferred_fields_recorded(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_SWEEP)
        assert len(spec.inferred_fields) > 0
        assert len(spec.assumption_log) > 0


# ═══════════════════════════════════════════════════════════════════════════
# General
# ═══════════════════════════════════════════════════════════════════════════

class TestGeneral:
    def test_empty_text(self, rule_parser):
        spec = rule_parser.parse("")
        assert len(spec.missing_fields) > 0

    def test_confirmed_fields_populated(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_SWEEP)
        assert len(spec.confirmed_fields) > 0

    def test_missing_fields_populated(self, rule_parser):
        spec = rule_parser.parse(TEXT_GAP_PLASMON_SWEEP)
        assert len(spec.missing_fields) > 0

    def test_spec_has_task_id(self, rule_parser):
        spec = rule_parser.parse("FDTD仿真金纳米球散射")
        assert spec.task.task_id != ""


class TestMockLLMParser:
    def test_placeholder_returns_spec(self, llm_parser):
        spec = llm_parser.parse("test text")
        assert spec.task.task_id
        assert len(spec.assumption_log) > 0
