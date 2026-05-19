"""Deterministic optical design requirement templates.

These templates translate first-run natural-language goals into local,
preview/design-assist optical language. They do not call external LLMs,
execute solvers, or query online material databases.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from optical_spec_agent.optical_language import (
    OpticalMonitorModel,
    OpticalSourceModel,
    template_source_monitor_defaults,
)


MatchConfidence = Literal["high", "medium", "low", "none"]


class RequirementSafetyFlags(BaseModel):
    no_solver_by_default: bool = True
    no_external_llm: bool = True
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class OpticalDesignRequirementTemplate(BaseModel):
    template_id: str
    title: str
    title_zh: str
    natural_language_goal_en: str
    natural_language_goal_zh: str
    optical_intent: str
    physical_system: str
    required_inputs: list[str] = Field(default_factory=list)
    default_assumptions: list[str] = Field(default_factory=list)
    source_model: OpticalSourceModel | None = None
    monitor_model: OpticalMonitorModel | None = None
    required_source_inputs: list[str] = Field(default_factory=list)
    required_monitor_inputs: list[str] = Field(default_factory=list)
    default_source_assumptions: list[str] = Field(default_factory=list)
    default_monitor_assumptions: list[str] = Field(default_factory=list)
    suggested_materials: list[str] = Field(default_factory=list)
    suggested_adapter: str
    expected_calculators: list[str] = Field(default_factory=list)
    expected_tool_calls: list[str] = Field(default_factory=list)
    expected_artifacts: list[str] = Field(default_factory=list)
    evidence_boundary: str
    next_actions: list[str] = Field(default_factory=list)
    design_case_id: str | None = None
    optical_language_summary: dict[str, str] = Field(default_factory=dict)
    safety: RequirementSafetyFlags = Field(default_factory=RequirementSafetyFlags)


class RequirementMatchResult(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    matched_template: OpticalDesignRequirementTemplate | None = None
    matched_template_id: str | None = None
    optical_language_summary: dict[str, str] = Field(default_factory=dict)
    confidence: MatchConfidence = "low"
    candidate_templates: list[str] = Field(default_factory=list)
    ambiguity_notes: list[str] = Field(default_factory=list)
    missing_disambiguation_inputs: list[str] = Field(default_factory=list)
    recommended_questions: list[str] = Field(default_factory=list)
    safe_default_template: str | None = None
    no_external_llm_used: bool = True
    missing_required_inputs: list[str] = Field(default_factory=list)
    default_assumptions: list[str] = Field(default_factory=list)
    recommended_next_actions: list[str] = Field(default_factory=list)
    diagnostics: list[str] = Field(default_factory=list)
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class DesignRequirementsResponse(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    templates: list[OpticalDesignRequirementTemplate] = Field(default_factory=list)
    template_count: int = 0
    catalog_status: str = "local_preview_requirement_templates"
    recommended_next_actions: list[str] = Field(default_factory=list)
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class DesignRequirementDetailResponse(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    template: OpticalDesignRequirementTemplate
    recommended_next_actions: list[str] = Field(default_factory=list)
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


TEMPLATE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "nanoparticle_plasmonics": (
        "nanoparticle",
        "plasmon",
        "scattering",
        "sphere",
        "纳米颗粒",
        "纳米粒子",
        "等离激元",
        "散射",
    ),
    "thin_film_ar_coating": (
        "anti-reflection",
        "antireflection",
        "ar coating",
        "coating",
        "thin film",
        "增透",
        "减反",
        "镀膜",
        "薄膜",
        "薄膜镀膜",
    ),
    "gaussian_beam_focus": (
        "gaussian",
        "beam waist",
        "waist",
        "rayleigh",
        "focus",
        "聚焦",
        "光腰",
        "高斯光束",
        "瑞利",
    ),
    "slab_waveguide_single_mode": (
        "waveguide",
        "single mode",
        "single-mode",
        "mode confinement",
        "波导",
        "单模",
        "模式",
    ),
    "paraxial_lens_imaging": (
        "lens",
        "imaging",
        "relay",
        "focal length",
        "ray trace",
        "透镜",
        "成像",
        "焦距",
        "光线",
    ),
    "photonic_crystal_band_preview": (
        "photonic crystal",
        "band diagram",
        "band structure",
        "lattice",
        "光子晶体",
        "能带",
        "晶格",
    ),
    "dielectric_metasurface_preview": (
        "metasurface",
        "metalens",
        "meta atom",
        "phase profile",
        "超表面",
        "超透镜",
        "相位",
    ),
}


def list_requirement_templates() -> list[OpticalDesignRequirementTemplate]:
    """Return local deterministic requirement templates."""

    return [TEMPLATES[template_id] for template_id in TEMPLATE_ORDER]


def get_requirement_template(template_id: str) -> OpticalDesignRequirementTemplate:
    """Return one requirement template by id."""

    try:
        return TEMPLATES[template_id]
    except KeyError as exc:
        raise ValueError(f"Unknown design requirement template: {template_id}") from exc


def match_goal_to_template(goal: str) -> RequirementMatchResult:
    """Match a natural-language goal to a local optical requirement template."""

    text = goal.strip()
    if not text:
        return RequirementMatchResult(
            status="needs_review",
            confidence="none",
            ambiguity_notes=["No goal text was supplied."],
            missing_disambiguation_inputs=["optical_application", "target_observable"],
            recommended_questions=[
                "What optical system are you trying to design?",
                "Which observable should be inspected first?",
            ],
            diagnostics=["Goal is empty; no requirement template can be matched."],
            recommended_next_actions=["Provide a natural-language optical design goal."],
        )
    lowered = text.lower()
    scores: list[tuple[int, int, str]] = []
    for priority, template_id in enumerate(TEMPLATE_ORDER):
        keywords = TEMPLATE_KEYWORDS[template_id]
        score = sum(1 for keyword in keywords if keyword.lower() in lowered)
        if score:
            scores.append((score, -priority, template_id))
    if not scores:
        return RequirementMatchResult(
            status="needs_review",
            confidence="none",
            optical_language_summary=_generic_optical_language_summary(text),
            candidate_templates=[],
            ambiguity_notes=[
                "No deterministic requirement template matched this goal.",
                "The backend will not guess a solver path from an unknown application.",
            ],
            missing_disambiguation_inputs=[
                "optical_application",
                "physical_system",
                "materials",
                "geometry",
                "target_output",
            ],
            recommended_questions=[
                "Is this a coating, beam, waveguide, lens, photonic crystal, metasurface, or nanoparticle case?",
                "What source and monitored observable should define the preview?",
                "Which material system and geometry scale should be assumed?",
            ],
            diagnostics=["No deterministic requirement template matched this goal."],
            missing_required_inputs=["physical_system", "materials", "geometry", "target_output"],
            default_assumptions=[
                "Use local preview workflow only.",
                "Do not execute external solvers or call external LLMs.",
            ],
            recommended_next_actions=[
                "Clarify whether this is a coating, beam, waveguide, lens, photonic crystal, metasurface, or nanoparticle case.",
                "Use /api/design-requirements to inspect supported templates.",
            ],
        )

    scores_sorted = sorted(scores, reverse=True)
    top_score = scores_sorted[0][0]
    top_template_ids = [template_id for score, _, template_id in scores_sorted if score == top_score]
    candidate_templates = [template_id for _, _, template_id in scores_sorted]
    _, _, template_id = scores_sorted[0]
    template = TEMPLATES[template_id]
    mixed_application = len(candidate_templates) > 1
    confidence: MatchConfidence
    if top_score >= 2 and len(top_template_ids) == 1 and not _looks_underconstrained(text):
        confidence = "high"
    elif len(top_template_ids) > 1 or mixed_application:
        confidence = "low"
    else:
        confidence = "medium"
    ambiguity_notes = _ambiguity_notes(
        text=text,
        confidence=confidence,
        candidate_templates=candidate_templates,
        top_template_ids=top_template_ids,
    )
    missing_disambiguation_inputs = _missing_disambiguation_inputs(template.template_id, text)
    recommended_questions = _recommended_questions(
        template.template_id,
        candidate_templates=candidate_templates,
        missing_inputs=missing_disambiguation_inputs,
    )
    return RequirementMatchResult(
        status="needs_review" if confidence in {"low", "none"} else "ok",
        matched_template=template,
        matched_template_id=template.template_id,
        optical_language_summary=template.optical_language_summary,
        confidence=confidence,
        candidate_templates=candidate_templates,
        ambiguity_notes=ambiguity_notes,
        missing_disambiguation_inputs=missing_disambiguation_inputs,
        recommended_questions=recommended_questions,
        safe_default_template=template.template_id if confidence == "medium" else None,
        missing_required_inputs=template.required_inputs,
        default_assumptions=template.default_assumptions,
        recommended_next_actions=template.next_actions,
        diagnostics=[
            "Matched with deterministic keyword heuristics; no external LLM was called.",
            "Template outputs are preview/design-assist and require human review.",
        ],
    )


def _looks_underconstrained(text: str) -> bool:
    lowered = text.lower()
    underconstrained_tokens = (
        "design an optical system",
        "optical system",
        "optimize",
        "优化",
        "光学系统",
        "设计一个光学系统",
        "帮我优化",
    )
    return any(token in lowered for token in underconstrained_tokens)


def _ambiguity_notes(
    *,
    text: str,
    confidence: MatchConfidence,
    candidate_templates: list[str],
    top_template_ids: list[str],
) -> list[str]:
    notes = [
        "Requirement matching is deterministic keyword logic; no external LLM was used.",
    ]
    if confidence == "high":
        notes.append("The goal contains a clear template-specific keyword pattern.")
    if confidence == "medium":
        notes.append("A safe default template is available, but design inputs remain under-specified.")
    if confidence == "low":
        if len(top_template_ids) > 1:
            notes.append("Multiple templates tied for the strongest deterministic match.")
        elif len(candidate_templates) > 1:
            notes.append("The goal mixes multiple optical application families.")
        if _looks_underconstrained(text):
            notes.append("The goal is underconstrained and needs more design intent before solver use.")
    if confidence == "none":
        notes.append("No supported local design template matched the goal.")
    return notes


def _missing_disambiguation_inputs(template_id: str, text: str) -> list[str]:
    lowered = text.lower()
    missing_by_template = {
        "nanoparticle_plasmonics": [
            ("particle_radius_or_diameter", ("radius", "diameter", "半径", "直径")),
            ("particle_material", ("silver", "gold", "ag", "au", "材料")),
            ("film_thickness", ("film thickness", "薄膜厚度", "thickness")),
            ("wavelength_band", ("wavelength", "band", "波长")),
        ],
        "thin_film_ar_coating": [
            ("target_wavelength", ("wavelength", "550", "波长")),
            ("substrate_material", ("substrate", "glass", "基底")),
            ("incidence_angle", ("angle", "入射角")),
        ],
        "gaussian_beam_focus": [
            ("wavelength", ("wavelength", "波长")),
            ("input_waist", ("waist", "光腰")),
            ("focal_length", ("focal", "焦距")),
        ],
        "slab_waveguide_single_mode": [
            ("core_index_or_material", ("core", "芯层", "材料")),
            ("cladding_index_or_material", ("cladding", "包层")),
            ("core_thickness", ("thickness", "厚度")),
            ("wavelength", ("wavelength", "波长")),
        ],
        "paraxial_lens_imaging": [
            ("focal_length", ("focal", "焦距")),
            ("aperture", ("aperture", "孔径")),
            ("field_of_view", ("field", "视场")),
            ("object_distance", ("object distance", "物距")),
        ],
        "photonic_crystal_band_preview": [
            ("lattice_constant", ("lattice", "period", "晶格", "周期")),
            ("unit_cell_geometry", ("unit cell", "孔", "柱", "单胞")),
            ("k_point_path", ("k-point", "k point", "能带路径")),
        ],
        "dielectric_metasurface_preview": [
            ("period", ("period", "周期")),
            ("target_phase_profile", ("phase", "相位")),
            ("polarization", ("polarization", "偏振")),
            ("wavelength", ("wavelength", "波长")),
        ],
    }
    missing = [
        field
        for field, tokens in missing_by_template.get(template_id, [])
        if not any(token.lower() in lowered for token in tokens)
    ]
    return missing


def _recommended_questions(
    template_id: str,
    *,
    candidate_templates: list[str],
    missing_inputs: list[str],
) -> list[str]:
    questions: list[str] = []
    if len(candidate_templates) > 1:
        questions.append(
            "Which design family should take priority: "
            + ", ".join(candidate_templates[:4])
            + "?"
        )
    if template_id == "paraxial_lens_imaging":
        questions.append("What focal length, aperture, field of view, and object distance should be assumed?")
    elif template_id == "nanoparticle_plasmonics":
        questions.append("What particle size, material, film thickness, wavelength band, and polarization should be assumed?")
    elif template_id == "thin_film_ar_coating":
        questions.append("What target wavelength, substrate material, incidence angle, and polarization define the coating?")
    elif template_id == "slab_waveguide_single_mode":
        questions.append("What core/cladding materials, core thickness, and wavelength should define the waveguide?")
    elif template_id == "gaussian_beam_focus":
        questions.append("What wavelength, input waist, and focal length should define the Gaussian beam preview?")
    elif template_id == "photonic_crystal_band_preview":
        questions.append("What lattice constant, unit cell geometry, and k-point path should define the band preview?")
    elif template_id == "dielectric_metasurface_preview":
        questions.append("What wavelength, polarization, period, and target phase profile should define the metasurface?")
    if missing_inputs:
        questions.append("Please provide or confirm: " + ", ".join(missing_inputs) + ".")
    questions.append("Should the backend keep using local preview-only tools without external solver execution?")
    return questions


def _template(
    *,
    template_id: str,
    title: str,
    title_zh: str,
    natural_language_goal_en: str,
    natural_language_goal_zh: str,
    optical_intent: str,
    physical_system: str,
    required_inputs: list[str],
    default_assumptions: list[str],
    suggested_materials: list[str],
    suggested_adapter: str,
    expected_calculators: list[str],
    expected_tool_calls: list[str],
    expected_artifacts: list[str],
    evidence_boundary: str,
    next_actions: list[str],
    design_case_id: str | None,
    material_system: str,
    geometry_model: str,
    solver_or_adapter_family: str,
    calculator_or_tool_path: str,
) -> OpticalDesignRequirementTemplate:
    (
        source_model,
        monitor_model,
        required_source_inputs,
        required_monitor_inputs,
        default_source_assumptions,
        default_monitor_assumptions,
    ) = template_source_monitor_defaults(template_id)
    return OpticalDesignRequirementTemplate(
        template_id=template_id,
        title=title,
        title_zh=title_zh,
        natural_language_goal_en=natural_language_goal_en,
        natural_language_goal_zh=natural_language_goal_zh,
        optical_intent=optical_intent,
        physical_system=physical_system,
        required_inputs=required_inputs,
        default_assumptions=default_assumptions,
        source_model=source_model,
        monitor_model=monitor_model,
        required_source_inputs=required_source_inputs,
        required_monitor_inputs=required_monitor_inputs,
        default_source_assumptions=default_source_assumptions,
        default_monitor_assumptions=default_monitor_assumptions,
        suggested_materials=suggested_materials,
        suggested_adapter=suggested_adapter,
        expected_calculators=expected_calculators,
        expected_tool_calls=expected_tool_calls,
        expected_artifacts=expected_artifacts,
        evidence_boundary=evidence_boundary,
        next_actions=next_actions,
        design_case_id=design_case_id,
        optical_language_summary={
            "physical_system": physical_system,
            "material_system": material_system,
            "geometry_model": geometry_model,
            "solver_or_adapter_family": solver_or_adapter_family,
            "calculator_or_tool_path": calculator_or_tool_path,
            "evidence_boundary": evidence_boundary,
        },
    )


def _generic_optical_language_summary(goal: str) -> dict[str, str]:
    return {
        "physical_system": "unknown_or_mixed_optical_system",
        "material_system": "not_enough_information",
        "geometry_model": "not_enough_information",
        "solver_or_adapter_family": "needs_human_selection",
        "calculator_or_tool_path": "no calculator selected",
        "evidence_boundary": "Preview/design-assist only; clarify the case before using outputs.",
        "source_goal": goal,
    }


COMMON_LOCAL_TOOL_CALLS = [
    "requirements.match_template",
    "requirements.extract_optical_intent",
    "optical_language.infer_source_monitor",
    "optical_language.diagnose_missing_inputs",
    "material_catalog.suggest",
    "example_registry.load",
    "agent_trace.build",
    "workflow_plan.preview",
    "adapter_preview.generate",
]

TEMPLATES: dict[str, OpticalDesignRequirementTemplate] = {
    "thin_film_ar_coating": _template(
        template_id="thin_film_ar_coating",
        title="Thin-film anti-reflection coating",
        title_zh="薄膜增透镀膜",
        natural_language_goal_en=(
            "Design a local preview for a single-layer anti-reflection coating on glass at 550 nm, "
            "estimate the quarter-wave thickness, and inspect a wavelength sweep without running solvers."
        ),
        natural_language_goal_zh=(
            "为玻璃基底上的单层增透薄膜做本地预览设计，目标波长 550 nm，估算四分之一波厚度，"
            "并查看反射率随波长变化，不运行外部求解器。"
        ),
        optical_intent="thin film coating preview",
        physical_system="thin_film_stack",
        required_inputs=[
            "incident_n",
            "substrate_n",
            "target_wavelength_nm",
            "coating_n or material choice",
            "wavelength_range_nm",
        ],
        default_assumptions=[
            "Normal incidence.",
            "Lossless constant-index preview.",
            "Single-layer quarter-wave helper before any validated stack model.",
        ],
        suggested_materials=["sio2", "tio2", "al2o3", "glass_fused_silica_preview"],
        suggested_adapter="preview-only; future TMM adapter candidate",
        expected_calculators=["optics.thin_film.spectrum"],
        expected_tool_calls=COMMON_LOCAL_TOOL_CALLS + ["optics.thin_film.spectrum"],
        expected_artifacts=["requirement_match", "thin_film_spectrum", "quarter_wave_ar", "workflow_plan"],
        evidence_boundary="Sanity-checked preview formulas only; verify material constants and stack physics before conclusions.",
        next_actions=[
            "Confirm coating material/index and substrate index.",
            "Inspect spectrum and quarter-wave helper output.",
            "Use validated thin-film tooling later if physical conclusions are needed.",
        ],
        design_case_id="thin_film_coating",
        material_system="SiO2/TiO2/Al2O3 preview coating candidates on glass",
        geometry_model="one-dimensional layer stack",
        solver_or_adapter_family="local thin-film calculator; future TMM adapter candidate",
        calculator_or_tool_path="/api/optics/thin-film-spectrum and /api/optics/quarter-wave-ar",
    ),
    "gaussian_beam_focus": _template(
        template_id="gaussian_beam_focus",
        title="Gaussian beam focus preview",
        title_zh="高斯光束聚焦预览",
        natural_language_goal_en=(
            "Preview Gaussian beam propagation and thin-lens focusing for a 1064 nm beam, "
            "including waist, Rayleigh range, and focused spot estimate without calling external tools."
        ),
        natural_language_goal_zh=(
            "预览 1064 nm 高斯光束的传播和薄透镜聚焦，给出光腰、瑞利长度和焦斑估计，"
            "不调用外部工具。"
        ),
        optical_intent="gaussian beam propagation preview",
        physical_system="gaussian_beam",
        required_inputs=["wavelength_nm", "input_waist_um", "propagation_range_mm", "focal_length_mm"],
        default_assumptions=[
            "Fundamental paraxial Gaussian beam.",
            "Ideal thin lens.",
            "No aberration, clipping, or vector-field effects.",
        ],
        suggested_materials=["air", "glass_bk7_preview", "glass_fused_silica_preview"],
        suggested_adapter="local Gaussian beam calculator; no solver adapter required",
        expected_calculators=["optics.gaussian_beam.series"],
        expected_tool_calls=COMMON_LOCAL_TOOL_CALLS + ["optics.gaussian_beam.series"],
        expected_artifacts=["requirement_match", "gaussian_beam_series", "gaussian_focus", "workflow_plan"],
        evidence_boundary="Paraxial Gaussian formulas only; not a vector diffraction or full lens validation.",
        next_actions=[
            "Confirm beam waist, wavelength, and focal length.",
            "Inspect Rayleigh range and focused waist estimates.",
            "Use a diffraction or ray-trace solver later if aperture/aberration effects matter.",
        ],
        design_case_id=None,
        material_system="air/glass preview propagation path",
        geometry_model="paraxial Gaussian beam plus ideal thin lens",
        solver_or_adapter_family="local Gaussian beam calculator",
        calculator_or_tool_path="/api/optics/gaussian-beam-series and /api/optics/gaussian-beam-focus",
    ),
    "slab_waveguide_single_mode": _template(
        template_id="slab_waveguide_single_mode",
        title="Slab waveguide single-mode estimate",
        title_zh="平板波导单模估计",
        natural_language_goal_en=(
            "Estimate whether a SiN slab waveguide is likely single-mode near 1550 nm, "
            "sweep core thickness, and keep the result as a local design-assist preview."
        ),
        natural_language_goal_zh=(
            "估算 1550 nm 附近 SiN 平板波导是否可能单模，扫描芯层厚度，并保持为本地设计辅助预览。"
        ),
        optical_intent="waveguide mode preview",
        physical_system="slab_waveguide",
        required_inputs=["core_n", "cladding_n", "core_thickness_um", "wavelength_nm"],
        default_assumptions=[
            "Symmetric slab-waveguide scalar V-number preview.",
            "Uses approximate single-mode threshold only.",
            "Does not solve ridge/asymmetric vector modes.",
        ],
        suggested_materials=["si3n4", "sio2", "si", "air"],
        suggested_adapter="mpb or elmer preview",
        expected_calculators=["optics.waveguide.sweep"],
        expected_tool_calls=COMMON_LOCAL_TOOL_CALLS + ["optics.waveguide.sweep"],
        expected_artifacts=["requirement_match", "waveguide_v_number_sweep", "single_mode_range", "workflow_plan"],
        evidence_boundary="Scalar V-number orientation only; not a mode-solver result.",
        next_actions=[
            "Confirm refractive indices and core thickness range.",
            "Inspect V-number sweep before adapter preview.",
            "Use MPB/Elmer validation only after explicit solver approval.",
        ],
        design_case_id="waveguide_mode",
        material_system="Si3N4/SiO2/air preview waveguide candidates",
        geometry_model="symmetric slab-waveguide approximation",
        solver_or_adapter_family="MPB or Elmer preview path",
        calculator_or_tool_path="/api/optics/waveguide-sweep and /api/optics/waveguide-single-mode-range",
    ),
    "paraxial_lens_imaging": _template(
        template_id="paraxial_lens_imaging",
        title="Paraxial lens imaging preview",
        title_zh="近轴透镜成像预览",
        natural_language_goal_en=(
            "Preview a simple lens imaging or two-lens relay design using ABCD matrices, "
            "then produce a local ray-optics workflow without running Optiland."
        ),
        natural_language_goal_zh=(
            "使用 ABCD 矩阵预览简单透镜成像或双透镜中继设计，然后生成本地光线光学工作流，不运行 Optiland。"
        ),
        optical_intent="lens ray tracing preview",
        physical_system="paraxial_lens_system",
        required_inputs=["focal_length_mm", "object_distance_mm", "lens_separation_mm optional", "wavelength optional"],
        default_assumptions=[
            "Ideal thin lenses.",
            "First-order paraxial model.",
            "No aberration, aperture stop, or material dispersion model.",
        ],
        suggested_materials=["glass_bk7_preview", "glass_fused_silica_preview", "air"],
        suggested_adapter="optiland",
        expected_calculators=["optics.paraxial.two_lens_relay"],
        expected_tool_calls=COMMON_LOCAL_TOOL_CALLS + ["optics.paraxial.two_lens_relay"],
        expected_artifacts=["requirement_match", "paraxial_system", "two_lens_relay", "adapter_preview"],
        evidence_boundary="First-order paraxial preview only; not ray-trace validation.",
        next_actions=[
            "Confirm focal length, object distance, and lens sequence.",
            "Inspect paraxial image distance/magnification before adapter preview.",
            "Use validated ray tracing later if aberrations or tolerances matter.",
        ],
        design_case_id="lens_raytrace_preview",
        material_system="preview glass candidates plus air",
        geometry_model="ideal thin-lens / ABCD system",
        solver_or_adapter_family="Optiland preview path",
        calculator_or_tool_path="/api/optics/paraxial-lens and /api/optics/two-lens-relay",
    ),
    "photonic_crystal_band_preview": _template(
        template_id="photonic_crystal_band_preview",
        title="Photonic crystal band preview",
        title_zh="光子晶体能带预览",
        natural_language_goal_en=(
            "Prepare a local photonic crystal band-structure preview workflow for MPB, "
            "including lattice/material assumptions and no solver execution."
        ),
        natural_language_goal_zh=(
            "为 MPB 准备本地光子晶体能带预览工作流，包含晶格和材料假设，不执行求解器。"
        ),
        optical_intent="photonic crystal band preview",
        physical_system="photonic_crystal",
        required_inputs=["lattice_type", "period", "material_indices", "num_bands", "k_path"],
        default_assumptions=[
            "Schematic periodic lattice until geometry is reviewed.",
            "MPB adapter preview only.",
            "No convergence proof or solver run.",
        ],
        suggested_materials=["si", "gaas", "sio2", "air"],
        suggested_adapter="mpb",
        expected_calculators=[],
        expected_tool_calls=COMMON_LOCAL_TOOL_CALLS,
        expected_artifacts=["requirement_match", "mpb_adapter_preview", "workflow_plan", "agent_trace"],
        evidence_boundary="Adapter preview only; no band solver execution or formal convergence proof.",
        next_actions=[
            "Confirm lattice, material contrast, and k-path.",
            "Inspect MPB preview input before any optional solver execution.",
            "Add convergence criteria before physical interpretation.",
        ],
        design_case_id="photonic_crystal_band",
        material_system="Si/GaAs/SiO2/air preview candidates",
        geometry_model="periodic lattice scaffold",
        solver_or_adapter_family="MPB preview path",
        calculator_or_tool_path="/api/adapter-preview and /api/workflow-plan",
    ),
    "dielectric_metasurface_preview": _template(
        template_id="dielectric_metasurface_preview",
        title="Dielectric metasurface preview",
        title_zh="介质超表面预览",
        natural_language_goal_en=(
            "Create a local preview workflow for a dielectric metasurface unit-cell array, "
            "suggest materials and adapters, and keep all outputs preview-only."
        ),
        natural_language_goal_zh=(
            "为介质超表面单元阵列创建本地预览工作流，推荐材料和适配器，并保持所有输出为预览。"
        ),
        optical_intent="dielectric metasurface preview",
        physical_system="metasurface",
        required_inputs=["target_wavelength_nm", "phase_profile", "period", "meta_atom_geometry", "substrate_material"],
        default_assumptions=[
            "Unit-cell/array geometry remains schematic.",
            "Material indices are preview values.",
            "No FDTD solver execution by default.",
        ],
        suggested_materials=["tio2", "si3n4", "si", "sio2"],
        suggested_adapter="meep with gmsh geometry preview",
        expected_calculators=[],
        expected_tool_calls=COMMON_LOCAL_TOOL_CALLS,
        expected_artifacts=["requirement_match", "material_suggestions", "meep_gmsh_preview", "agent_trace"],
        evidence_boundary="Geometry/material preview only; no metasurface efficiency validation.",
        next_actions=[
            "Confirm phase target, period, and meta-atom geometry.",
            "Inspect material suggestions and adapter preview.",
            "Add solver validation later only with explicit approval.",
        ],
        design_case_id="dielectric_metasurface_preview",
        material_system="TiO2/Si3N4/Si/SiO2 preview candidates",
        geometry_model="periodic meta-atom array scaffold",
        solver_or_adapter_family="Meep with Gmsh geometry preview",
        calculator_or_tool_path="/api/adapter-preview and /api/agent-trace",
    ),
    "nanoparticle_plasmonics": _template(
        template_id="nanoparticle_plasmonics",
        title="Nanoparticle plasmonics scattering preview",
        title_zh="纳米颗粒等离激元散射预览",
        natural_language_goal_en=(
            "Generate a local preview workflow for silver or gold nanoparticle scattering on a thin film, "
            "suggest materials and an open-source adapter path, and do not run external solvers."
        ),
        natural_language_goal_zh=(
            "为银或金纳米颗粒位于薄膜上的散射问题生成本地预览工作流，推荐材料和开源适配器路径，"
            "不运行外部求解器。"
        ),
        optical_intent="nanoparticle plasmonics / scattering preview",
        physical_system="nanoparticle_on_film",
        required_inputs=["particle_material", "particle_size_nm", "film_material", "gap_nm", "wavelength_range_nm"],
        default_assumptions=[
            "Open-source-first Meep/Gmsh preview path.",
            "Material constants must be verified before conclusions.",
            "No FDTD solver execution by default.",
        ],
        suggested_materials=["ag", "au", "sio2", "water", "air"],
        suggested_adapter="meep with gmsh geometry preview",
        expected_calculators=[],
        expected_tool_calls=COMMON_LOCAL_TOOL_CALLS,
        expected_artifacts=["requirement_match", "material_suggestions", "agent_trace", "adapter_preview"],
        evidence_boundary="Adapter/material preview only; no scattering spectrum solver result.",
        next_actions=[
            "Confirm particle size, gap, film, and wavelength range.",
            "Review Meep/Gmsh preview artifacts.",
            "Verify metal optical constants before any physical conclusions.",
        ],
        design_case_id="nanoparticle_plasmonics",
        material_system="Ag/Au nanoparticle with SiO2/water/air environment preview",
        geometry_model="sphere-on-film or nanoparticle-on-film scaffold",
        solver_or_adapter_family="Meep with optional Gmsh geometry preview",
        calculator_or_tool_path="/api/adapter-preview and /api/agent-trace",
    ),
}

TEMPLATE_ORDER = [
    "nanoparticle_plasmonics",
    "thin_film_ar_coating",
    "gaussian_beam_focus",
    "slab_waveguide_single_mode",
    "paraxial_lens_imaging",
    "photonic_crystal_band_preview",
    "dielectric_metasurface_preview",
]
