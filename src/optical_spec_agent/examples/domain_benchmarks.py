"""Application-domain benchmark scenarios for local optical design previews.

The benchmark suite evaluates deterministic backend behavior for positive,
ambiguous, underconstrained, and unsupported optical-design goals. It reuses
the application-domain registry, requirement-template matching, and Agent Task
Session ledger. It never executes external solvers, calls external LLMs,
uploads artifacts, creates tags, or creates releases.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

from optical_spec_agent.examples.application_domains import (
    get_application_domain,
    match_goal_to_application_domains,
)
from optical_spec_agent.examples.requirements import match_goal_to_template


ScenarioType = Literal[
    "positive",
    "ambiguous",
    "underconstrained",
    "unsupported",
    "unsafe_or_blocked",
]
ScenarioStatus = Literal["pass", "warn", "fail"]


class ApplicationDomainScenario(BaseModel):
    scenario_id: str
    domain_id: str | None = None
    scenario_type: ScenarioType
    goal_en: str
    goal_zh: str
    expected_primary_domain: str | None = None
    expected_candidate_domains: list[str] = Field(default_factory=list)
    expected_confidence: str
    expected_requirement_template: str | None = None
    expected_materials: list[str] = Field(default_factory=list)
    expected_calculators: list[str] = Field(default_factory=list)
    expected_adapters: list[str] = Field(default_factory=list)
    expected_missing_critical_inputs: list[str] = Field(default_factory=list)
    expected_missing_optional_inputs: list[str] = Field(default_factory=list)
    expected_recommended_questions: list[str] = Field(default_factory=list)
    expected_blocked_actions: list[str] = Field(default_factory=list)
    preview_only: bool = True
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class ApplicationDomainScenarioResult(BaseModel):
    api_contract_version: str = "0.1"
    scenario_id: str
    status: ScenarioStatus
    actual_domain: str | None = None
    actual_candidates: list[str] = Field(default_factory=list)
    actual_confidence: str = "none"
    actual_template: str | None = None
    actual_tool_calls: list[str] = Field(default_factory=list)
    actual_missing_inputs: list[str] = Field(default_factory=list)
    actual_questions: list[str] = Field(default_factory=list)
    diagnostics: list[str] = Field(default_factory=list)
    safety_flags: dict[str, bool] = Field(default_factory=dict)
    actual_materials: list[str] = Field(default_factory=list)
    actual_adapter: str | None = None
    blocked_actions: list[str] = Field(default_factory=list)
    preview_only: bool = True
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class ApplicationDomainBenchmarkResponse(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    scenarios: list[ApplicationDomainScenario] = Field(default_factory=list)
    scenario_count: int = 0
    scenario_type_counts: dict[str, int] = Field(default_factory=dict)
    preview_only: bool = True
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class ApplicationDomainBenchmarkResultResponse(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    results: list[ApplicationDomainScenarioResult] = Field(default_factory=list)
    summary: dict[str, int] = Field(default_factory=dict)
    preview_only: bool = True
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class ApplicationDomainScenarioResponse(BaseModel):
    api_contract_version: str = "0.1"
    status: str = "ok"
    scenario: ApplicationDomainScenario
    preview_only: bool = True
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


def _scenario(
    scenario_id: str,
    scenario_type: ScenarioType,
    goal_en: str,
    goal_zh: str,
    *,
    domain_id: str | None = None,
    expected_primary_domain: str | None = None,
    expected_candidate_domains: list[str] | None = None,
    expected_confidence: str = "high",
    expected_requirement_template: str | None = None,
    expected_materials: list[str] | None = None,
    expected_calculators: list[str] | None = None,
    expected_adapters: list[str] | None = None,
    expected_missing_critical_inputs: list[str] | None = None,
    expected_missing_optional_inputs: list[str] | None = None,
    expected_recommended_questions: list[str] | None = None,
    expected_blocked_actions: list[str] | None = None,
) -> ApplicationDomainScenario:
    return ApplicationDomainScenario(
        scenario_id=scenario_id,
        domain_id=domain_id,
        scenario_type=scenario_type,
        goal_en=goal_en,
        goal_zh=goal_zh,
        expected_primary_domain=expected_primary_domain or domain_id,
        expected_candidate_domains=expected_candidate_domains or [],
        expected_confidence=expected_confidence,
        expected_requirement_template=expected_requirement_template,
        expected_materials=expected_materials or [],
        expected_calculators=expected_calculators or [],
        expected_adapters=expected_adapters or [],
        expected_missing_critical_inputs=expected_missing_critical_inputs or [],
        expected_missing_optional_inputs=expected_missing_optional_inputs or [],
        expected_recommended_questions=expected_recommended_questions or [],
        expected_blocked_actions=expected_blocked_actions or [],
    )


SCENARIOS: dict[str, ApplicationDomainScenario] = {
    "nanoparticle_plasmonics_positive": _scenario(
        "nanoparticle_plasmonics_positive",
        "positive",
        "Create a local preview for a silver nanoparticle plasmonic scattering spectrum from 400 to 900 nm.",
        "请为银纳米颗粒等离激元散射谱生成 400 到 900 nm 的本地预览。",
        domain_id="nanoparticle_plasmonics",
        expected_requirement_template="nanoparticle_plasmonics",
        expected_materials=["ag", "au", "sio2"],
        expected_adapters=["meep", "gmsh"],
    ),
    "thin_film_coating_positive": _scenario(
        "thin_film_coating_positive",
        "positive",
        "Design a thin film anti-reflection coating on glass at 550 nm using local preview calculators.",
        "请为玻璃基底在 550 nm 设计薄膜增透镀膜，并只使用本地预览计算器。",
        domain_id="thin_film_coating",
        expected_requirement_template="thin_film_ar_coating",
        expected_materials=["sio2", "tio2", "al2o3"],
        expected_calculators=["optics.thin_film.spectrum"],
    ),
    "slab_waveguide_positive": _scenario(
        "slab_waveguide_positive",
        "positive",
        "Design a single mode slab waveguide preview at 1550 nm with SiN core and SiO2 cladding.",
        "请设计 1550 nm 的单模平板波导预览，芯层为氮化硅，包层为二氧化硅。",
        domain_id="slab_waveguide",
        expected_requirement_template="slab_waveguide_single_mode",
        expected_materials=["si3n4", "sio2"],
        expected_calculators=["optics.waveguide.sweep"],
        expected_adapters=["mpb", "elmer"],
    ),
    "photonic_crystal_positive": _scenario(
        "photonic_crystal_positive",
        "positive",
        "Create a photonic crystal band structure preview with an MPB adapter path.",
        "请生成光子晶体能带结构的 MPB adapter 本地预览。",
        domain_id="photonic_crystal",
        expected_requirement_template="photonic_crystal_band_preview",
        expected_materials=["si", "sio2", "air"],
        expected_adapters=["mpb"],
    ),
    "dielectric_metasurface_positive": _scenario(
        "dielectric_metasurface_positive",
        "positive",
        "Plan a dielectric metasurface phase profile preview for a TiO2 periodic meta atom.",
        "请为 TiO2 周期性超表面单元结构规划介质超表面相位预览。",
        domain_id="dielectric_metasurface",
        expected_requirement_template="dielectric_metasurface_preview",
        expected_materials=["tio2", "sio2"],
        expected_adapters=["meep", "gmsh"],
    ),
    "lens_ray_optics_positive": _scenario(
        "lens_ray_optics_positive",
        "positive",
        "Create a paraxial lens ray trace preview with focal length and aperture estimates.",
        "请创建包含焦距和孔径估计的近轴透镜光线预览。",
        domain_id="lens_ray_optics",
        expected_requirement_template="paraxial_lens_imaging",
        expected_materials=["glass_bk7_preview", "glass_fused_silica_preview"],
        expected_calculators=["optics.paraxial.two_lens_relay"],
        expected_adapters=["optiland"],
    ),
    "gaussian_beam_focusing_positive": _scenario(
        "gaussian_beam_focusing_positive",
        "positive",
        "Preview Gaussian beam focusing with waist, Rayleigh range, and focal spot estimates.",
        "请预览高斯光束聚焦，包含光腰、瑞利长度和焦斑估计。",
        domain_id="gaussian_beam_focusing",
        expected_requirement_template="gaussian_beam_focus",
        expected_materials=["air"],
        expected_calculators=["optics.gaussian_beam.series"],
    ),
    "imaging_system_preview_positive": _scenario(
        "imaging_system_preview_positive",
        "positive",
        "Plan an imaging system preview with magnification, image plane, and aperture questions.",
        "请规划成像系统预览，包含放大率、像面和孔径问题。",
        domain_id="imaging_system_preview",
        expected_requirement_template="paraxial_lens_imaging",
        expected_materials=["glass_bk7_preview", "glass_fused_silica_preview"],
        expected_calculators=["optics.paraxial.two_lens_relay"],
        expected_adapters=["optiland"],
    ),
    "fiber_coupling_preview_positive": _scenario(
        "fiber_coupling_preview_positive",
        "positive",
        "Preview fiber coupling with mode overlap and Gaussian beam assumptions.",
        "请预览光纤耦合，包含模式重叠和高斯光束假设。",
        domain_id="fiber_coupling_preview",
        expected_requirement_template="gaussian_beam_focus",
        expected_materials=["glass_fused_silica_preview", "sio2", "si3n4"],
        expected_calculators=["optics.gaussian_beam.series"],
        expected_adapters=["mpb", "optiland"],
    ),
    "polarization_optics_preview_positive": _scenario(
        "polarization_optics_preview_positive",
        "positive",
        "Create a polarization waveplate preview with input polarization and retardance questions.",
        "请创建偏振波片预览，包含输入偏振和延迟量问题。",
        domain_id="polarization_optics_preview",
        expected_materials=["tio2", "si3n4", "sio2"],
    ),
    "waveguide_or_coating_ambiguous": _scenario(
        "waveguide_or_coating_ambiguous",
        "ambiguous",
        "Design a waveguide and thin-film coating preview for an integrated photonics stack.",
        "请为集成光子堆栈设计一个波导和薄膜镀膜预览。",
        expected_candidate_domains=["slab_waveguide", "thin_film_coating"],
        expected_confidence="low",
        expected_recommended_questions=["Is the primary artifact a waveguide mode estimate or a coating spectrum?"],
    ),
    "lens_or_gaussian_focus_ambiguous": _scenario(
        "lens_or_gaussian_focus_ambiguous",
        "ambiguous",
        "Focus a Gaussian beam with a lens, but decide whether this is a beam or ray-optics task.",
        "请用透镜聚焦高斯光束，但需要判断这是光束任务还是光线光学任务。",
        expected_candidate_domains=["gaussian_beam_focusing", "lens_ray_optics"],
        expected_confidence="low",
        expected_recommended_questions=["Should the first result be a Gaussian waist estimate or a paraxial lens image?"],
    ),
    "generic_optical_system_ambiguous": _scenario(
        "generic_optical_system_ambiguous",
        "ambiguous",
        "Design an optical system.",
        "设计一个光学系统。",
        expected_candidate_domains=[
            "thin_film_coating",
            "slab_waveguide",
            "lens_ray_optics",
            "gaussian_beam_focusing",
            "nanoparticle_plasmonics",
        ],
        expected_confidence="low",
    ),
    "lens_missing_focal_length": _scenario(
        "lens_missing_focal_length",
        "underconstrained",
        "Optimize a lens preview for imaging.",
        "请优化一个成像透镜预览。",
        domain_id="lens_ray_optics",
        expected_confidence="medium",
        expected_requirement_template="paraxial_lens_imaging",
        expected_missing_critical_inputs=["focal_length_mm", "aperture", "field_of_view"],
    ),
    "nanoparticle_missing_radius_material": _scenario(
        "nanoparticle_missing_radius_material",
        "underconstrained",
        "Plan a nanoparticle scattering preview.",
        "请规划一个纳米颗粒散射预览。",
        domain_id="nanoparticle_plasmonics",
        expected_requirement_template="nanoparticle_plasmonics",
        expected_missing_critical_inputs=["particle_radius", "particle_material", "gap_medium"],
    ),
    "waveguide_missing_core_thickness": _scenario(
        "waveguide_missing_core_thickness",
        "underconstrained",
        "Plan a single mode slab waveguide preview.",
        "请规划一个单模平板波导预览。",
        domain_id="slab_waveguide",
        expected_requirement_template="slab_waveguide_single_mode",
        expected_missing_critical_inputs=["core_thickness_um", "cladding_material", "wavelength_nm"],
    ),
    "full_zemax_optimization_request": _scenario(
        "full_zemax_optimization_request",
        "unsupported",
        "Run a full Zemax lens optimization and return production-ready prescription files.",
        "请运行完整 Zemax 透镜优化并返回生产可用的处方文件。",
        expected_confidence="none",
        expected_blocked_actions=["proprietary_solver", "external_solver", "production_ready_export"],
    ),
    "full_lumerical_fdtd_request": _scenario(
        "full_lumerical_fdtd_request",
        "unsupported",
        "Run a full Lumerical FDTD metasurface optimization with real monitor results.",
        "请运行完整 Lumerical FDTD 超表面优化并返回真实 monitor 结果。",
        expected_confidence="none",
        expected_blocked_actions=["proprietary_solver", "external_solver", "real_solver_monitor_result"],
    ),
    "production_grade_validation_request": _scenario(
        "production_grade_validation_request",
        "unsafe_or_blocked",
        "Provide production-grade physical validation and a convergence proof for this optical design.",
        "请为这个光学设计提供生产级物理验证和收敛证明。",
        expected_confidence="none",
        expected_blocked_actions=["production_grade_validation", "formal_convergence_claim", "external_solver"],
    ),
}


def list_domain_scenarios() -> list[ApplicationDomainScenario]:
    """Return stable application-domain benchmark scenarios."""

    return [SCENARIOS[scenario_id] for scenario_id in SCENARIOS]


def get_domain_scenario(scenario_id: str) -> ApplicationDomainScenario:
    """Return one benchmark scenario."""

    try:
        return SCENARIOS[scenario_id]
    except KeyError as exc:
        raise ValueError(f"Unknown application domain benchmark scenario: {scenario_id}") from exc


def evaluate_domain_scenario(scenario_id: str) -> ApplicationDomainScenarioResult:
    """Evaluate one scenario against local deterministic backend behavior."""

    scenario = get_domain_scenario(scenario_id)
    domain_match = match_goal_to_application_domains(scenario.goal_en)
    requirement_match = match_goal_to_template(scenario.goal_en)
    blocked_actions = _detect_blocked_actions(scenario.goal_en, scenario.goal_zh)
    session = None
    if scenario.scenario_type not in {"ambiguous", "unsupported", "unsafe_or_blocked"}:
        from optical_spec_agent.agents.task_session import build_agent_task_session

        session = build_agent_task_session(scenario.goal_en)

    actual_domain = (
        session.application_domain_id
        if session is not None and session.application_domain_id
        else (domain_match.matched_domains[0] if domain_match.matched_domains else None)
    )
    actual_candidates = _unique_strings(
        [
            *domain_match.candidate_domains,
            *(session.application_domain_candidates if session is not None else []),
        ]
    )
    actual_tool_calls = (
        sorted({entry.tool_name for entry in session.tool_call_ledger if entry.executed})
        if session is not None
        else []
    )
    actual_missing_inputs = _unique_strings(
        [
            *(session.missing_critical_inputs if session is not None else []),
            *(session.missing_optional_inputs if session is not None else []),
            *(session.missing_required_inputs if session is not None else []),
            *_domain_missing_inputs(actual_domain),
        ]
    )
    actual_questions = _unique_strings(
        [
            *domain_match.recommended_questions,
            *requirement_match.recommended_questions,
            *(session.recommended_questions if session is not None else []),
            *_domain_questions(actual_domain),
        ]
    )
    actual_adapter = (
        session.adapter_source_monitor_mapping.adapter_name
        if session is not None and session.adapter_source_monitor_mapping is not None
        else None
    )
    actual_materials = _domain_materials(actual_domain)
    diagnostics = _diagnose_result(
        scenario,
        actual_domain=actual_domain,
        actual_candidates=actual_candidates,
        actual_template=requirement_match.matched_template_id,
        actual_tool_calls=actual_tool_calls,
        actual_missing_inputs=actual_missing_inputs,
        actual_questions=actual_questions,
        actual_materials=actual_materials,
        actual_adapter=actual_adapter,
        blocked_actions=blocked_actions,
    )
    status = _status_from_diagnostics(scenario, diagnostics)
    safety_flags = {
        "external_solver_executed": False,
        "external_llm_required": False,
        "proprietary_solver_required": False,
        "production_grade_validation_claimed": False,
        "formal_convergence_proof_claimed": False,
        "upload_performed": False,
        "tag_created": False,
        "release_created": False,
    }
    return ApplicationDomainScenarioResult(
        scenario_id=scenario.scenario_id,
        status=status,
        actual_domain=actual_domain,
        actual_candidates=actual_candidates,
        actual_confidence=domain_match.confidence,
        actual_template=requirement_match.matched_template_id,
        actual_tool_calls=actual_tool_calls,
        actual_missing_inputs=actual_missing_inputs,
        actual_questions=actual_questions,
        diagnostics=diagnostics or ["Scenario matched expected local preview behavior."],
        safety_flags=safety_flags,
        actual_materials=actual_materials,
        actual_adapter=actual_adapter,
        blocked_actions=blocked_actions,
    )


def evaluate_all_domain_scenarios() -> ApplicationDomainBenchmarkResultResponse:
    """Evaluate all benchmark scenarios."""

    results = [evaluate_domain_scenario(scenario.scenario_id) for scenario in list_domain_scenarios()]
    summary = {
        "total": len(results),
        "pass": sum(1 for result in results if result.status == "pass"),
        "warn": sum(1 for result in results if result.status == "warn"),
        "fail": sum(1 for result in results if result.status == "fail"),
        "positive": sum(1 for scenario in SCENARIOS.values() if scenario.scenario_type == "positive"),
        "ambiguous": sum(1 for scenario in SCENARIOS.values() if scenario.scenario_type == "ambiguous"),
        "underconstrained": sum(1 for scenario in SCENARIOS.values() if scenario.scenario_type == "underconstrained"),
        "unsupported": sum(
            1
            for scenario in SCENARIOS.values()
            if scenario.scenario_type in {"unsupported", "unsafe_or_blocked"}
        ),
        "unsafe_or_blocked": sum(
            1 for scenario in SCENARIOS.values() if scenario.scenario_type == "unsafe_or_blocked"
        ),
        "preview_only": len(results),
    }
    return ApplicationDomainBenchmarkResultResponse(
        status="needs_review" if summary["fail"] else "ok",
        results=results,
        summary=summary,
    )


def application_domain_benchmark_response() -> ApplicationDomainBenchmarkResponse:
    """Return the benchmark scenario catalog response."""

    scenarios = list_domain_scenarios()
    return ApplicationDomainBenchmarkResponse(
        scenarios=scenarios,
        scenario_count=len(scenarios),
        scenario_type_counts={
            "positive": sum(1 for scenario in scenarios if scenario.scenario_type == "positive"),
            "ambiguous": sum(1 for scenario in scenarios if scenario.scenario_type == "ambiguous"),
            "underconstrained": sum(
                1 for scenario in scenarios if scenario.scenario_type == "underconstrained"
            ),
            "unsupported": sum(
                1
                for scenario in scenarios
                if scenario.scenario_type in {"unsupported", "unsafe_or_blocked"}
            ),
            "unsafe_or_blocked": sum(
                1 for scenario in scenarios if scenario.scenario_type == "unsafe_or_blocked"
            ),
        },
    )


def _diagnose_result(
    scenario: ApplicationDomainScenario,
    *,
    actual_domain: str | None,
    actual_candidates: list[str],
    actual_template: str | None,
    actual_tool_calls: list[str],
    actual_missing_inputs: list[str],
    actual_questions: list[str],
    actual_materials: list[str],
    actual_adapter: str | None,
    blocked_actions: list[str],
) -> list[str]:
    diagnostics: list[str] = []
    if scenario.scenario_type in {"unsupported", "unsafe_or_blocked"}:
        missing_blocks = [
            action for action in scenario.expected_blocked_actions if action not in blocked_actions
        ]
        if missing_blocks:
            diagnostics.append(f"Missing expected blocked actions: {', '.join(missing_blocks)}.")
        if actual_tool_calls:
            diagnostics.append("Unsupported scenario unexpectedly built an executable task session.")
        return diagnostics

    if scenario.scenario_type == "ambiguous":
        if scenario.expected_confidence == "low" and actual_candidates and len(actual_candidates) < 2:
            diagnostics.append("Ambiguous scenario did not preserve multiple candidate domains.")
        if scenario.expected_candidate_domains:
            missing_candidates = [
                item for item in scenario.expected_candidate_domains if item not in actual_candidates
            ]
            if missing_candidates:
                diagnostics.append(f"Missing expected candidate domains: {', '.join(missing_candidates)}.")
        if actual_domain and scenario.expected_primary_domain is None:
            diagnostics.append("Ambiguous scenario hard-matched a primary domain.")
        if not actual_questions:
            diagnostics.append("Ambiguous scenario did not produce follow-up questions.")
        return diagnostics

    if scenario.expected_primary_domain and scenario.expected_primary_domain != actual_domain:
        diagnostics.append(
            f"Expected domain {scenario.expected_primary_domain}, got {actual_domain or 'none'}."
        )
    if scenario.expected_requirement_template and scenario.expected_requirement_template != actual_template:
        diagnostics.append(
            f"Expected template {scenario.expected_requirement_template}, got {actual_template or 'none'}."
        )
    missing_materials = [
        material for material in scenario.expected_materials if material not in actual_materials
    ]
    if missing_materials:
        diagnostics.append(f"Missing expected domain materials: {', '.join(missing_materials)}.")
    missing_tools = [
        tool for tool in scenario.expected_calculators if tool not in actual_tool_calls
    ]
    if missing_tools:
        diagnostics.append(f"Missing expected calculator tool calls: {', '.join(missing_tools)}.")
    if scenario.expected_adapters and actual_adapter not in scenario.expected_adapters:
        diagnostics.append(
            f"Expected adapter in {', '.join(scenario.expected_adapters)}, got {actual_adapter or 'none'}."
        )
    missing_inputs = [
        item for item in scenario.expected_missing_critical_inputs if item not in actual_missing_inputs
    ]
    if scenario.scenario_type == "underconstrained" and missing_inputs:
        diagnostics.append(f"Missing expected underconstrained inputs: {', '.join(missing_inputs)}.")
    if scenario.scenario_type == "underconstrained" and not actual_questions:
        diagnostics.append("Underconstrained scenario did not produce recommended questions.")
    return diagnostics


def _status_from_diagnostics(
    scenario: ApplicationDomainScenario,
    diagnostics: list[str],
) -> ScenarioStatus:
    if not diagnostics:
        if scenario.domain_id in {"fiber_coupling_preview", "polarization_optics_preview"}:
            return "warn"
        return "pass"
    if scenario.scenario_type in {"unsupported", "unsafe_or_blocked"}:
        return "fail"
    if scenario.scenario_type in {"ambiguous", "underconstrained"}:
        return "warn"
    if scenario.domain_id in {"fiber_coupling_preview", "polarization_optics_preview"}:
        return "warn"
    return "fail"


def _detect_blocked_actions(goal_en: str, goal_zh: str) -> list[str]:
    text = f"{goal_en} {goal_zh}".lower()
    actions: list[str] = []
    if any(term in text for term in ("zemax", "lumerical", "comsol", "ansys")):
        actions.extend(["proprietary_solver", "external_solver"])
    if any(term in text for term in ("production-ready", "生产可用")):
        actions.append("production_ready_export")
    if any(term in text for term in ("real monitor result", "真实 monitor")):
        actions.append("real_solver_monitor_result")
    if any(term in text for term in ("production-grade physical validation", "生产级物理验证")):
        actions.append("production_grade_validation")
    if any(term in text for term in ("convergence proof", "收敛证明")):
        actions.append("formal_convergence_claim")
    if "external_solver" not in actions and actions:
        actions.append("external_solver")
    return _unique_strings(actions)


def _domain_materials(domain_id: str | None) -> list[str]:
    if not domain_id:
        return []
    try:
        return get_application_domain(domain_id).suggested_materials
    except ValueError:
        return []


def _domain_missing_inputs(domain_id: str | None) -> list[str]:
    if not domain_id:
        return []
    try:
        domain = get_application_domain(domain_id)
    except ValueError:
        return []
    return [*domain.common_missing_inputs, *domain.required_inputs]


def _domain_questions(domain_id: str | None) -> list[str]:
    if not domain_id:
        return []
    try:
        return get_application_domain(domain_id).recommended_questions
    except ValueError:
        return []


def _unique_strings(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value and value not in seen:
            result.append(value)
            seen.add(value)
    return result
