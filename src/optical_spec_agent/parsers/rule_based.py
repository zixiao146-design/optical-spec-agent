"""Rule-based parser — keyword / regex / inference heuristics for v0.3.

This is the baseline parser. It uses keyword tables, regex patterns, and
simple post-hoc inference rules to populate an OpticalSpec from natural
language (Chinese or English).
"""

from __future__ import annotations

import re
import uuid
from typing import Any

from optical_spec_agent.models.base import (
    BoundaryConditionSetting,
    GeometryDefinition,
    MaterialEntry,
    MaterialSystem,
    MeshSetting,
    MonitorSetting,
    ParticleInfo,
    PostprocessTargetSpec,
    SourceSetting,
    StabilitySetting,
    SubstrateOrFilmInfo,
    SweepPlan,
    SymmetrySetting,
    StatusField,
    confirmed,
    inferred,
    missing,
)
from optical_spec_agent.models.spec import (
    GeometryMaterialSection,
    OpticalSpec,
    OutputSection,
    PhysicsSection,
    SimulationSection,
    TaskSection,
)

from optical_spec_agent.parsers.base import BaseParser


# ═══════════════════════════════════════════════════════════════════════════
# Keyword mapping tables
# ═══════════════════════════════════════════════════════════════════════════

_TASK_KEYWORDS: dict[str, list[str]] = {
    "simulation": ["仿真", "simulation", "FDTD", "FEM", "RCWA", "模拟", "计算"],
    "modeling": ["建模", "modeling", "建立模型", "构建"],
    "fitting": ["拟合", "fitting", "fit", "Lorentzian", "洛伦兹", "曲线拟合"],
    "data_analysis": ["分析", "analysis", "数据处理", "提取", "研究"],
    "plotting": ["画图", "plotting", "绘图", "可视化"],
    "writing": ["撰写", "writing", "报告", "论文"],
}

_SOLVER_KEYWORDS: dict[str, list[str]] = {
    "fdtd": ["FDTD", "fdtd", "时域有限差分"],
    "fem": ["FEM", "fem", "有限元", "COMSOL"],
    "rcwa": ["RCWA", "rcwa", "严格耦合波"],
    "analytical": ["解析", "analytical", "解析解", "Mie"],
    "coupled_oscillator": ["耦合振子", "coupled oscillator", "coupled_oscillator", "耦合振子模型"],
}

_SOFTWARE_KEYWORDS: dict[str, list[str]] = {
    "meep": ["Meep", "meep", "MEEP"],
    "lumerical": ["Lumerical", "lumerical", "LUMERICAL"],
    "comsol": ["COMSOL", "comsol"],
    "matlab": ["MATLAB", "matlab"],
    "python": ["Python", "python", "scipy", "numpy"],
}

_MECHANISM_KEYWORDS: dict[str, list[str]] = {
    "gap_plasmon": [
        "gap plasmon", "间隙等离激元", "gap plasmonic",
    ],
    "plasmon": [
        "等离激元", "plasmon", "plasmonic", "表面等离激元", "SPP", "LSPR",
    ],
    "mode_hybridization": [
        "模式杂化", "mode hybridization", "mode coupling", "模式耦合",
    ],
    "interference": ["干涉", "interference", "Fabry-Perot", "FP"],
    "coupling": ["耦合", "coupling"],
    "photonic_crystal": ["光子晶体", "photonic crystal", "PhC"],
    "metamaterial": ["超材料", "metamaterial", "超表面", "metasurface"],
    "dielectric": ["介质", "dielectric", "电介质"],
    "diffraction": ["衍射", "diffraction", "光栅"],
    "scattering": ["散射", "scattering", "Mie"],
    "waveguide": ["波导", "waveguide"],
    "resonance": ["共振", "谐振", "resonance", "resonant"],
}

_PHYSICAL_SYSTEM_KEYWORDS: dict[str, list[str]] = {
    "nanoparticle_on_film": [
        "gap plasmon", "纳米.*膜", "颗粒.*膜", "nanoparticle.*film",
        "sphere.*film", "球.*膜", "立方体.*膜", "rod.*film", "棒.*膜",
        "-金膜", "-膜", "on.*film",
    ],
    "single_particle": ["单颗粒", "single particle", "纳米球", "纳米棒"],
    "particle_array": ["阵列", "array", "周期阵列"],
    "thin_film": ["薄膜", "thin film", "单层膜"],
    "multilayer": ["多层", "multilayer", "叠层"],
    "waveguide": ["波导", "waveguide", "脊波导"],
    "grating": ["光栅", "grating"],
    "metasurface": ["超表面", "metasurface"],
    "coupled_system": ["耦合体系", "coupled system"],
}

_STRUCTURE_KEYWORDS: dict[str, list[str]] = {
    "sphere_on_film": [
        "球.*膜", "球-.*膜", "纳米球.*膜", "sphere.*on.*film",
        "金纳米球.*膜", "球.*金膜",
    ],
    "rod_on_film": [
        "棒.*膜", "纳米棒.*膜", "rod.*on.*film",
    ],
    "cube_on_film": [
        "立方体.*膜", "纳米立方.*膜", "cube.*on.*film",
    ],
    "cross_structure": [
        "十字", "cross", "十字结构", "非对称.*十字",
    ],
    "single_particle": [
        "纳米颗粒", "nanoparticle", "单粒子", "particle",
        "纳米球", "nanosphere", "纳米棒", "nanorod",
    ],
    "array": ["阵列", "array", "周期", "periodic", "晶格", "lattice"],
    "film": ["薄膜", "film"],
    "multilayer": ["多层", "multilayer"],
    "gratings": ["光栅", "grating"],
    "waveguide": ["波导", "waveguide", "脊波导"],
    "metasurface": ["超表面", "metasurface"],
}

_DIMENSION_KEYWORDS: dict[str, list[str]] = {
    "3d": ["3D", "3维", "三维", "立体"],
    "2d": ["2D", "2维", "二维", "截面", "cross-section"],
    "axisymmetric": ["轴对称", "axisymmetric", "旋转对称"],
}

_UNIT_TO_NM = {
    "nm": 1.0,
    "um": 1000.0,
    "μm": 1000.0,
    "mm": 1_000_000.0,
}

_MATERIAL_PATTERNS: list[tuple[str, list[str]]] = [
    ("Si3N4", [r"(?<![A-Za-z0-9])Si3N4(?![A-Za-z0-9])", r"\bsilicon\s+nitride\b", r"氮化硅"]),
    ("SiO2", [r"(?<![A-Za-z0-9])SiO2(?![A-Za-z0-9])", r"\bsilicon\s+dioxide\b", r"二氧化硅", r"石英", r"\bsilica\b", r"\bquartz\b"]),
    ("Al2O3", [r"(?<![A-Za-z0-9])Al2O3(?![A-Za-z0-9])", r"氧化铝", r"\balumina\b"]),
    ("TiO2", [r"(?<![A-Za-z0-9])TiO2(?![A-Za-z0-9])", r"二氧化钛", r"\btitania\b"]),
    ("Au", [r"(?<![A-Za-z0-9])Au(?![A-Za-z0-9])", r"\bgold\b", r"金"]),
    ("Ag", [r"(?<![A-Za-z0-9])Ag(?![A-Za-z0-9])", r"\bsilver\b", r"银"]),
    ("Glass", [r"\bglass\b", r"玻璃"]),
    ("Water", [r"\bwater\b", r"水"]),
    ("Air", [r"\bair\b", r"空气"]),
    ("Si", [r"(?<![A-Za-z0-9])Si(?![A-Za-z0-9])", r"\bsilicon\b(?!\s*(?:dioxide|nitride))", r"(?<!二氧化)(?<!氮化)硅"]),
]

_GAP_RELEVANT_MATERIALS = ("SiO2", "Si3N4", "Al2O3", "TiO2", "Glass", "Water", "Air", "Si")

_POLARIZATION_KEYWORDS: dict[str, list[str]] = {
    "linear_x": ["x偏振", "x-linear", "x偏光"],
    "linear_y": ["y偏振", "y-linear", "y偏光"],
    "TM": ["TM", "tm", "TM偏振", "p偏振"],
    "TE": ["TE", "te", "TE偏振", "s偏振"],
    "unpolarized": ["非偏振", "unpolarized"],
    "linear": ["线偏振", "linear polarization", "偏振"],
    "circular_left": ["左旋", "LCP"],
    "circular_right": ["右旋", "RCP"],
}

_OUTPUT_KEYWORDS: dict[str, list[str]] = {
    "scattering_spectrum": [
        "散射谱", "scattering spectrum", "散射光谱",
    ],
    "absorption_spectrum": [
        "吸收谱", "absorption spectrum", "吸收光谱", "吸收截面",
    ],
    "transmission_spectrum": ["透射谱", "transmission spectrum"],
    "reflection_spectrum": ["反射谱", "reflection spectrum"],
    "field_distribution": ["场分布", "field distribution", "场图"],
    "field_enhancement": ["场增强", "field enhancement", "|E|"],
    "cross_section": ["截面", "cross section", "消光截面"],
    "Q_factor": ["Q因子", "Q factor", "品质因子"],
    "mode_profile": ["模式分布", "mode profile", "模场", "模场分布"],
    "near_field": ["近场", "near field"],
    "far_field": ["远场", "far field"],
    "FWHM": ["FWHM", "半高全宽", "线宽"],
    "decay_rate": ["衰减", "decay rate", "弛豫"],
    "spectrum": ["光谱", "spectrum", "谱"],
}

_POSTPROCESS_KEYWORDS: dict[str, list[str]] = {
    "resonance_wavelength": [
        "共振波长", "resonance wavelength", "谐振波长", "主峰波长", "峰位",
        "共振频率", "resonant wavelength",
    ],
    "fwhm_extraction": [
        "FWHM", "半高全宽", "线宽", "line width",
    ],
    "T2_extraction": [
        "T2", "退相干时间", "dephasing time", "退相位时间", "dephasing",
    ],
    "Q_factor_calc": ["Q因子", "Q factor", "品质因子"],
    "lorentzian_fit": ["Lorentzian", "洛伦兹拟合", "洛伦兹"],
    "peak_finding": ["找峰", "peak finding"],
    "band_diagram": ["能带", "band diagram", "色散"],
    "S_parameter": ["S参数", "S parameter", "S11", "S21"],
}

_BOUNDARY_KEYWORDS: dict[str, list[str]] = {
    "PML": ["PML", "pml", "完美匹配层"],
    "periodic": ["周期边界", "periodic"],
    "Bloch": ["Bloch", "bloch", "布洛赫"],
}

_GEOMETRY_TYPE_KEYWORDS: dict[str, list[str]] = {
    "sphere": ["球", "sphere", "nanosphere", "纳米球"],
    "cube": ["立方体", "cube", "nanocube", "纳米立方"],
    "rod": ["棒", "rod", "nanorod", "纳米棒"],
    "cross": ["十字", "cross"],
    "cylinder": ["圆柱", "cylinder"],
    "film": ["膜", "film", "薄膜"],
    "waveguide": ["波导", "waveguide", "脊波导"],
    "ring": ["环", "ring"],
}

# Generic "X 从 A 到 B unit" pattern  (Chinese)
_GENERIC_SWEEP_CN = re.compile(
    r"(gap|间隙(?:厚度)?|间距|直径|厚度|周期|width|diameter|thickness|period)"
    r"\s*从\s*([\d.]+)\s*(?:nm|μm|um|mm)?\s*(?:到|至)\s*([\d.]+)\s*(nm|μm|um|mm)",
    re.IGNORECASE,
)

# English "X from A to B unit"
_GENERIC_SWEEP_EN = re.compile(
    r"(gap|diameter|thickness|period|width)"
    r"\s+(?:varies?\s+)?(?:from\s+)?([\d.]+)\s*(?:to|[-–~])\s*([\d.]+)\s*(nm|μm|um|mm)",
    re.IGNORECASE,
)

# Wavelength range pattern
_WL_RANGE = re.compile(r"([\d.]+)\s*[-–到至~]\s*([\d.]+)\s*(nm|μm|um)", re.IGNORECASE)


# ═══════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════

def _match_keywords(text: str, table: dict[Any, list[str]]) -> list[str]:
    """Return all keys whose keywords appear in *text*.

    For entries whose keyword contains `.*`, use regex search instead of `in`.
    """
    hits: list[str] = []
    text_lower = text.lower()
    for key, keywords in table.items():
        for kw in keywords:
            if ".*" in kw:
                if re.search(kw, text, re.IGNORECASE):
                    hits.append(key)
                    break
            else:
                if kw.lower() in text_lower:
                    hits.append(key)
                    break
    return hits


def _extract_first(text: str, pattern: str) -> str | None:
    m = re.search(pattern, text, re.IGNORECASE)
    return m.group(0).strip() if m else None


def _match_materials(text: str) -> list[str]:
    """Match materials with regex boundaries and long-token priority."""
    hits: list[str] = []
    for name, patterns in _MATERIAL_PATTERNS:
        if any(re.search(pattern, text, re.IGNORECASE) for pattern in patterns):
            hits.append(name)
    return hits


def _format_number(value: float) -> str:
    return str(int(value)) if float(value).is_integer() else f"{value:g}"


def _normalize_unit(unit: str) -> str:
    unit_l = unit.lower()
    if unit_l == "um":
        return "μm"
    return unit


def _format_length(value: float, unit: str) -> str:
    return f"{_format_number(value)} {_normalize_unit(unit)}"


def _length_to_nm(value: float, unit: str) -> float:
    return value * _UNIT_TO_NM[unit.lower()]


def _extract_length(text: str, patterns: list[str]) -> tuple[float, str] | None:
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE)
        if m:
            return float(m.group(1)), m.group(2)
    return None


def _build_dimension_pair(native_key: str, nm_key: str, value: float, unit: str) -> dict[str, str]:
    return {
        native_key: _format_length(value, unit),
        nm_key: _format_number(_length_to_nm(value, unit)),
    }


def _extract_particle_dimensions(text: str, particle_type: str | None) -> dict[str, str]:
    """Extract particle-specific dimensions without mixing in gap/film values."""
    dims: dict[str, str] = {}

    sphere_patterns = [
        r"直径\s*(?:=|为|是|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
        r"([\d.]+)\s*(nm|μm|um|mm)\s*(?:金|银|Au|Ag|gold|silver)?\s*(?:纳米)?球",
        r"([\d.]+)\s*(nm|μm|um|mm)\s*(?:Au|Ag|gold|silver)\s*(?:nano)?sphere\b",
        r"(?:Au|Ag|gold|silver)?\s*(?:nano)?sphere(?:\s+diameter)?\s*(?:of|=|is|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
        r"(?:Au|Ag|gold|silver)?\s*nanosphere(?:\s+diameter)?\s*(?:of|=|is|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
    ]
    cube_patterns = [
        r"边长\s*(?:=|为|是|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
        r"([\d.]+)\s*(nm|μm|um|mm)\s*(?:金|银|Au|Ag|gold|silver)?\s*(?:纳米)?立方(?:体|块)?",
        r"([\d.]+)\s*(nm|μm|um|mm)\s*(?:Au|Ag|gold|silver)\s*(?:nano)?cube\b",
        r"(?:Au|Ag|gold|silver)?\s*(?:nano)?cube(?:\s+edge(?:\s+length)?)?\s*(?:of|=|is|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
    ]
    rod_diameter_patterns = [
        r"直径\s*(?:=|为|是|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
        r"(?:Au|Ag|gold|silver|金|银)?\s*(?:nano)?rod(?:\s+diameter)?\s*(?:of|=|is|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
        r"([\d.]+)\s*(nm|μm|um|mm)\s*(?:Au|Ag|gold|silver|金|银)?\s*(?:纳米)?棒",
    ]

    if particle_type == "sphere":
        diameter = _extract_length(text, sphere_patterns)
        if diameter:
            dims.update(_build_dimension_pair("直径", "diameter_nm", *diameter))
    elif particle_type == "cube":
        edge = _extract_length(text, cube_patterns)
        if edge:
            dims.update(_build_dimension_pair("边长", "edge_length_nm", *edge))
    elif particle_type == "rod":
        rod_diameter = _extract_length(text, rod_diameter_patterns)
        if rod_diameter:
            dims.update(_build_dimension_pair("直径", "diameter_nm", *rod_diameter))

    if not dims:
        explicit_diameter = _extract_length(text, [r"直径\s*(?:=|为|是|:)?\s*([\d.]+)\s*(nm|μm|um|mm)", r"\bdiameter\s*(?:=|of|is|:)?\s*([\d.]+)\s*(nm|μm|um|mm)"])
        if explicit_diameter:
            dims.update(_build_dimension_pair("直径", "diameter_nm", *explicit_diameter))

    return dims


def _extract_film_thickness(text: str) -> tuple[float, str] | None:
    return _extract_length(
        text,
        [
            r"(?:金|Au|gold)\s*(?:膜|film)\s*(?:厚度|thickness)?\s*(?:=|为|是|:|of|is)?\s*([\d.]+)\s*(nm|μm|um|mm)",
            r"([\d.]+)\s*(nm|μm|um|mm)\s*(?:金|Au|gold)\s*(?:膜|film)(?:上)?",
            r"(?:Au|gold)\s*film\s*thickness\s*(?:=|of|is|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
        ],
    )


def _extract_gap_thickness(text: str) -> tuple[float, str] | None:
    return _extract_length(
        text,
        [
            r"(?:gap|gap thickness|间隙(?:厚度)?|间距)\s*(?:=|为|是|:|of|is)?\s*([\d.]+)\s*(nm|μm|um|mm)",
            r"间隙填充[^()（）]{0,20}[（(]\s*([\d.]+)\s*(nm|μm|um|mm)\s*[)）]",
            r"(?:中间\s*)?[^。,.，]{0,20}\bgap\b\s*(?:=|为|是|:|of|is)?\s*([\d.]+)\s*(nm|μm|um|mm)",
        ],
    )


def _extract_gap_medium(text: str, found_materials: list[str]) -> str | None:
    if not re.search(r"(gap|间隙|间距)", text, re.IGNORECASE):
        return None

    for name, patterns in _MATERIAL_PATTERNS:
        if name not in found_materials or name not in _GAP_RELEVANT_MATERIALS:
            continue
        for pattern in patterns:
            if re.search(rf"{pattern}\s*gap", text, re.IGNORECASE):
                return name
            if re.search(rf"间隙填充\s*{pattern}", text, re.IGNORECASE):
                return name
            if re.search(rf"(gap|间隙)[^。,.，]{{0,16}}{pattern}", text, re.IGNORECASE):
                return name

    for material in found_materials:
        if material not in ("Au", "Ag"):
            return material
    return None


# ═══════════════════════════════════════════════════════════════════════════
# RuleBasedParser
# ═══════════════════════════════════════════════════════════════════════════

class RuleBasedParser(BaseParser):
    """Keyword-driven heuristic parser for optical task descriptions."""

    def parse(self, text: str, *, task_id: str = "") -> OpticalSpec:
        if not task_id:
            task_id = uuid.uuid4().hex[:8]

        task = self._parse_task(text, task_id)
        physics = self._parse_physics(text)
        geom = self._parse_geometry_material(text)
        sim = self._parse_simulation(text, physics)
        out = self._parse_output(text)

        spec = OpticalSpec(
            task=task,
            physics=physics,
            geometry_material=geom,
            simulation=sim,
            output=out,
        )

        # ---- post-hoc inference chain ----
        self._apply_inference_rules(spec, text)

        spec.collect_all()
        return spec

    # ── section parsers ──────────────────────────────────────────────────

    def _parse_task(self, text: str, task_id: str) -> TaskSection:
        types = _match_keywords(text, _TASK_KEYWORDS)
        task_type_val = types[0] if types else None
        task_type = confirmed(task_type_val) if task_type_val else missing("无法识别任务类型")

        first_sentence = re.split(r"[。.!！\n]", text)[0].strip()[:80]
        task_name = confirmed(first_sentence) if first_sentence else missing()

        return TaskSection(
            task_id=task_id,
            task_name=task_name,
            task_type=task_type,
            research_goal=inferred(text[:300], "从用户描述推断"),
        )

    def _parse_physics(self, text: str) -> PhysicsSection:
        mechanisms = _match_keywords(text, _MECHANISM_KEYWORDS)
        structures = _match_keywords(text, _STRUCTURE_KEYWORDS)
        phys_systems = _match_keywords(text, _PHYSICAL_SYSTEM_KEYWORDS)
        dims = _match_keywords(text, _DIMENSION_KEYWORDS)

        # Prefer the most specific physical_system
        ps_val = None
        for preferred in ("nanoparticle_on_film", "waveguide", "metasurface", "grating"):
            if preferred in phys_systems:
                ps_val = preferred
                break
        if not ps_val and phys_systems:
            ps_val = phys_systems[0]
        if not ps_val and structures:
            # fallback: map structure → physical_system
            _struct_to_sys = {
                "sphere_on_film": "nanoparticle_on_film",
                "rod_on_film": "nanoparticle_on_film",
                "cube_on_film": "nanoparticle_on_film",
                "cross_structure": "nanoparticle_on_film",
                "waveguide": "waveguide",
                "gratings": "grating",
                "metasurface": "metasurface",
            }
            ps_val = _struct_to_sys.get(structures[0])
            if not ps_val:
                ps_val = structures[0]

        # For mechanism, prefer gap_plasmon over plasmon when both match
        mech_val = mechanisms[0] if mechanisms else None

        return PhysicsSection(
            physical_system=confirmed(ps_val) if ps_val else missing("未指定物理系统"),
            physical_mechanism=confirmed(mech_val) if mech_val else missing("未识别物理机制"),
            model_dimension=inferred(dims[0], "根据描述推断") if dims else missing("未指定维度"),
            structure_type=confirmed(structures[0]) if structures else missing("未识别结构类型"),
        )

    def _parse_geometry_material(self, text: str) -> GeometryMaterialSection:
        found_materials = _match_materials(text)
        geom_types = _match_keywords(text, _GEOMETRY_TYPE_KEYWORDS)

        # --- GeometryDefinition ---
        dim_patterns = {
            "直径": r"直径\s*(?:=|为|是|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
            "边长": r"边长\s*(?:=|为|是|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
            "长度": r"(?:长度|宽|高)\s*(?:=|为|是|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
            "gap": r"(?:gap|间隙)\s*(?:=|为|是|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
            "厚度": r"厚度\s*(?:=|为|是|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
            "宽": r"宽(?:度)?\s*(?:=|为|是|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
            "厚": r"厚(?:度)?\s*(?:=|为|是|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
            "周期": r"周期\s*(?:=|为|是|:)?\s*([\d.]+)\s*(nm|μm|um|mm)",
        }
        extracted_dims: dict[str, str] = {}
        for name, pat in dim_patterns.items():
            val = _extract_first(text, pat)
            if val:
                extracted_dims[name] = val

        particle_dims = _extract_particle_dimensions(text, geom_types[0] if geom_types else None)
        film_thickness = _extract_film_thickness(text)
        gap_thickness = _extract_gap_thickness(text)

        if "直径" in particle_dims:
            extracted_dims["直径"] = particle_dims["直径"]
        if "边长" in particle_dims:
            extracted_dims["边长"] = particle_dims["边长"]
        if film_thickness:
            extracted_dims["膜厚"] = _format_length(*film_thickness)
        if gap_thickness:
            extracted_dims["gap"] = _format_length(*gap_thickness)

        geom_def = GeometryDefinition(
            geometry_type=geom_types[0] if geom_types else None,
            description=re.split(r"[。.!！\n]", text)[0][:200],
            dimensions=extracted_dims,
        )

        # --- MaterialSystem ---
        mat_entries = [MaterialEntry(name=m) for m in found_materials]
        for entry in mat_entries:
            if entry.name in ("Au", "Ag"):
                if any(kw in text for kw in ("金膜", "膜上", "film", "-膜")):
                    entry.role = "film"
                else:
                    entry.role = "particle"
            elif entry.name in ("SiO2", "Glass", "Si"):
                if any(kw in text for kw in ("间隙", "gap", "填充")):
                    entry.role = "gap_medium"
                elif any(kw in text for kw in ("基底", "substrate", "包层")):
                    entry.role = "substrate"
                else:
                    entry.role = "substrate"
        mat_system = MaterialSystem(materials=mat_entries)

        # --- MaterialModel ---
        mat_model_val = None
        if found_materials and any(m in ("Au", "Ag") for m in found_materials):
            mat_model_val = "Johnson-Christy"

        # --- SubstrateOrFilmInfo ---
        sub_info = SubstrateOrFilmInfo()
        if any(kw in text for kw in ("基底", "substrate", "下包层")):
            sub_info.has_substrate = True
            for m in found_materials:
                if m in ("SiO2", "Glass", "Si"):
                    sub_info.substrate_material = m
        if any(kw in text for kw in ("膜", "film", "金膜")):
            sub_info.has_film = True
            if "Au" in found_materials:
                sub_info.film_material = "Au"
            elif "Ag" in found_materials:
                sub_info.film_material = "Ag"
        if film_thickness:
            sub_info.film_thickness = _format_length(*film_thickness)

        # --- ParticleInfo ---
        particle = ParticleInfo()
        if geom_types:
            particle.particle_type = geom_types[0]
            for m in found_materials:
                if m in ("Au", "Ag"):
                    particle.material = m
                    break
            particle.dimensions = particle_dims

        # --- Key parameters ---
        param_patterns = [
            r"gap\s*(?:=|为|是|:)?\s*[\d.]+\s*(?:nm|μm|um|mm)",
            r"间隙\s*(?:=|为|是|:)?\s*[\d.]+\s*(?:nm|μm|um|mm)",
            r"直径\s*(?:=|为|是|:)?\s*[\d.]+\s*(?:nm|μm|um|mm)",
            r"边长\s*(?:=|为|是|:)?\s*[\d.]+\s*(?:nm|μm|um|mm)",
            r"波长\s*(?:=|为|是|:)?\s*[\d.]+\s*(?:nm|μm|um|mm)",
            r"厚度\s*(?:=|为|是|:)?\s*[\d.]+\s*(?:nm|μm|um|mm)",
            r"周期\s*(?:=|为|是|:)?\s*[\d.]+\s*(?:nm|μm|um|mm)",
            r"[\d.]+\s*(?:nm|μm|um)\s*(?:gap|间距)",
        ]
        key_params = []
        for pat in param_patterns:
            for m in re.finditer(pat, text, re.IGNORECASE):
                key_params.append(m.group(0).strip())
        if "直径" in particle_dims:
            key_params.append(f"直径 {particle_dims['直径']}")
        if film_thickness:
            key_params.append(f"金膜厚度 {_format_length(*film_thickness)}")
        if gap_thickness:
            key_params.append(f"gap {_format_length(*gap_thickness)}")
        key_params = list(dict.fromkeys(key_params))

        # --- gap_medium ---
        gap_medium_val = _extract_gap_medium(text, found_materials)

        return GeometryMaterialSection(
            geometry_definition=confirmed(geom_def) if geom_def.description else missing(),
            material_system=confirmed(mat_system) if mat_entries else missing("未识别材料体系"),
            material_model=inferred(mat_model_val, "默认金属光学常数来源") if mat_model_val else missing(),
            substrate_or_film_info=confirmed(sub_info) if (sub_info.has_substrate or sub_info.has_film) else missing("未指定基底/薄膜"),
            particle_info=confirmed(particle) if particle.particle_type else missing(),
            gap_medium=confirmed(gap_medium_val) if gap_medium_val else missing("未指定间隙介质"),
            key_parameters=confirmed(key_params) if key_params else missing("未提取到关键参数"),
        )

    def _parse_simulation(self, text: str, physics: PhysicsSection) -> SimulationSection:
        solvers = _match_keywords(text, _SOLVER_KEYWORDS)
        softwares = _match_keywords(text, _SOFTWARE_KEYWORDS)
        pols = _match_keywords(text, _POLARIZATION_KEYWORDS)
        boundaries = _match_keywords(text, _BOUNDARY_KEYWORDS)

        # ---- SweepPlan ----
        sweep = self._extract_sweep_plan(text)

        # ---- SourceSetting ----
        source = SourceSetting()
        for kw, src_type in [
            ("总场散射场", "tfsf"), ("TFSF", "tfsf"),
            ("平面波", "plane_wave"), ("plane wave", "plane_wave"),
            ("点源", "dipole"), ("dipole", "dipole"), ("偶极子", "dipole"),
            ("mode source", "mode_source"), ("模式源", "mode_source"),
        ]:
            if kw.lower() in text.lower():
                source.source_type = src_type
                break

        wl_match = _WL_RANGE.search(text)
        if wl_match:
            source.wavelength_range = f"{wl_match.group(1)}-{wl_match.group(2)} {wl_match.group(3)}"
        if pols:
            source.polarization = pols[0]

        # ---- BoundaryConditionSetting ----
        bc = BoundaryConditionSetting()
        if boundaries:
            for side in ("x_min", "x_max", "y_min", "y_max", "z_min", "z_max"):
                setattr(bc, side, boundaries[0])
        elif physics.physical_system.status == "confirmed" and physics.physical_system.value in (
            "nanoparticle_on_film", "single_particle",
        ):
            for side in ("x_min", "x_max", "y_min", "y_max", "z_min", "z_max"):
                setattr(bc, side, "PML")

        # ---- Remaining settings ----
        symmetry = SymmetrySetting()
        mesh = MeshSetting()
        stability = StabilitySetting()
        monitor = MonitorSetting()

        # Incident direction
        direction = None
        for kw in ["正入射", "normal incidence", "normal", "垂直入射"]:
            if kw.lower() in text.lower():
                direction = kw
                break
        if direction is None and any(kw in text for kw in ["斜入射", "oblique"]):
            direction = "斜入射"

        return SimulationSection(
            solver_method=confirmed(solvers[0]) if solvers else missing("未指定求解方法"),
            software_tool=confirmed(softwares[0]) if softwares else missing("未指定软件工具"),
            sweep_plan=confirmed(sweep) if (sweep.sweep_type or sweep.variable) else missing("未指定扫描计划"),
            excitation_source=confirmed(source.source_type) if source.source_type else missing("未指定激励源"),
            source_setting=confirmed(source) if source.source_type else missing("未指定光源设置"),
            polarization=confirmed(pols[0]) if pols else missing("未指定偏振"),
            incident_direction=confirmed(direction) if direction else inferred("正入射", "默认入射方向"),
            boundary_condition=confirmed(bc) if bc.x_min else missing("未指定边界条件"),
            symmetry_setting=missing("未指定对称性设置"),
            mesh_setting=missing("未指定网格设置"),
            stability_setting=missing("未指定稳定性设置"),
            monitor_setting=missing("未指定监视器设置"),
        )

    def _parse_output(self, text: str) -> OutputSection:
        observables = _match_keywords(text, _OUTPUT_KEYWORDS)
        postprocs = _match_keywords(text, _POSTPROCESS_KEYWORDS)

        # Build PostprocessTargetSpec list
        pp_specs = [PostprocessTargetSpec(target_type=p) for p in postprocs]

        return OutputSection(
            output_observables=confirmed(observables) if observables else inferred(
                ["spectrum"], "默认输出光谱",
            ),
            postprocess_target=confirmed(
                [p.model_dump() for p in pp_specs]
            ) if pp_specs else missing("未指定后处理目标"),
        )

    # ── sweep extraction ─────────────────────────────────────────────────

    def _extract_sweep_plan(self, text: str) -> SweepPlan:
        sweep = SweepPlan()

        # --- Try Chinese generic "X 从 A 到 B unit" first (highest priority) ---
        cn = _GENERIC_SWEEP_CN.search(text)
        if cn:
            raw_var = cn.group(1).lower()
            var_map = {
                "gap": "gap_nm", "间隙": "gap_nm", "间隙厚度": "gap_nm", "间距": "gap_nm",
                "直径": "diameter_nm", "diameter": "diameter_nm",
                "厚度": "thickness_nm", "thickness": "thickness_nm",
                "周期": "period_nm", "period": "period_nm",
                "width": "width_nm",
            }
            sweep.variable = var_map.get(raw_var, raw_var + "_" + cn.group(4))
            sweep.range_start = float(cn.group(2))
            sweep.range_end = float(cn.group(3))
            sweep.unit = cn.group(4)
            sweep.sweep_type = "parameter"
            sweep.description = cn.group(0).strip()

        # --- Try English "X from A to B unit" ---
        if not sweep.variable:
            en = _GENERIC_SWEEP_EN.search(text)
            if en:
                raw_var = en.group(1).lower()
                var_map = {
                    "gap": "gap_nm", "diameter": "diameter_nm",
                    "thickness": "thickness_nm", "period": "period_nm",
                    "width": "width_nm",
                }
                sweep.variable = var_map.get(raw_var, raw_var + "_" + en.group(4))
                sweep.range_start = float(en.group(2))
                sweep.range_end = float(en.group(3))
                sweep.unit = en.group(4)
                sweep.sweep_type = "parameter"
                sweep.description = en.group(0).strip()

        # --- Step ---
        step_m = re.search(r"步长\s*([\d.]+)\s*(nm|μm|um|mm)", text, re.IGNORECASE)
        if step_m:
            sweep.step = float(step_m.group(1))
            sweep.unit = step_m.group(2)

        # --- Wavelength range (only if no parameter sweep found) ---
        if not sweep.variable:
            wl = _WL_RANGE.search(text)
            if wl:
                sweep.sweep_type = "wavelength"
                sweep.variable = "wavelength_nm"
                sweep.range_start = float(wl.group(1))
                sweep.range_end = float(wl.group(2))
                sweep.unit = wl.group(3)

        return sweep

    # ── post-hoc inference rules ─────────────────────────────────────────

    def _apply_inference_rules(self, spec: OpticalSpec, text: str) -> None:
        """Apply inference rules that depend on multiple fields."""

        # Rule 1: scattering/absorption → task_type bias
        if spec.task.task_type.status == "missing":
            if any(kw in text for kw in ("散射谱", "吸收谱", "scattering spectrum", "absorption spectrum")):
                spec.task.task_type = inferred("data_analysis", "提到光谱分析，推断为 data_analysis")
            elif any(kw in text for kw in ("散射", "吸收", "scattering", "absorption")):
                spec.task.task_type = inferred("simulation", "提到散射/吸收，推断为 simulation")

        # Rule 2: FWHM / T2 → suggest lorentzian fit_model
        if any(kw in text for kw in ("FWHM", "T2", "退相干", "线宽", "半高全宽", "dephasing", "退相位")):
            # Add lorentzian to postprocess if not already there
            if spec.output.postprocess_target.status == "missing":
                spec.output.postprocess_target = inferred(
                    [PostprocessTargetSpec(target_type="lorentzian_fit").model_dump()],
                    "FWHM/T2 提取需求推断需要 Lorentzian 拟合",
                )
            elif spec.output.postprocess_target.status == "confirmed":
                pp_list = spec.output.postprocess_target.value
                if isinstance(pp_list, list):
                    target_types = [p.get("target_type", "") for p in pp_list if isinstance(p, dict)]
                    if "lorentzian_fit" not in target_types:
                        pp_list.append(PostprocessTargetSpec(target_type="lorentzian_fit").model_dump())
                        spec.output.postprocess_target = inferred(
                            pp_list, "FWHM/T2 提取需求推断补充 Lorentzian 拟合",
                        )

        # Rule 3: gap plasmon + no solver → infer fdtd
        if (spec.simulation.solver_method.status == "missing"
                and spec.physics.physical_mechanism.status == "confirmed"
                and spec.physics.physical_mechanism.value in ("gap_plasmon", "plasmon")):
            spec.simulation.solver_method = inferred(
                "fdtd", "gap plasmon 体系通常使用 FDTD 求解",
            )

        # Rule 4: nanoparticle_on_film + no dimension → infer 3d
        if (spec.physics.model_dimension.status == "missing"
                and spec.physics.physical_system.status == "confirmed"
                and spec.physics.physical_system.value == "nanoparticle_on_film"):
            spec.physics.model_dimension = inferred(
                "3d", "nanoparticle_on_film 通常需要 3D 仿真",
            )

        # Rule 5: if output has scattering/absorption keywords but observables
        # is only generic "spectrum", refine to specific spectrum type
        if spec.output.output_observables.status == "confirmed":
            obs = spec.output.output_observables.value
            if isinstance(obs, list) and "spectrum" in obs:
                if any(kw in text for kw in ("散射", "scattering")):
                    obs = [o for o in obs if o != "spectrum"]
                    if "scattering_spectrum" not in obs:
                        obs.append("scattering_spectrum")
                    spec.output.output_observables = confirmed(obs)
                elif any(kw in text for kw in ("吸收", "absorption")):
                    obs = [o for o in obs if o != "spectrum"]
                    if "absorption_spectrum" not in obs:
                        obs.append("absorption_spectrum")
                    spec.output.output_observables = confirmed(obs)
