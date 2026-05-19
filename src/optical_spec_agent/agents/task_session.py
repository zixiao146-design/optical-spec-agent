"""Deterministic local Agent Task Session builder."""

from __future__ import annotations

import hashlib
from typing import Any, Literal

from pydantic import BaseModel, Field

from optical_spec_agent.examples.registry import (
    ExampleRegistryError,
    build_example_agent_trace,
    get_optical_design_example,
)
from optical_spec_agent.examples.requirements import (
    RequirementMatchResult,
    match_goal_to_template,
)
from optical_spec_agent.materials.catalog import suggest_materials_for_application
from optical_spec_agent.optical_language import (
    AdapterSourceMonitorMapping,
    ObservableDiagnostic,
    OpticalLanguageDiagnostics,
    OpticalMonitorModel,
    OpticalSourceModel,
    diagnose_observable,
    generate_disambiguation_questions,
    infer_source_monitor_from_goal,
    map_source_monitor_to_adapter,
)
from optical_spec_agent.optics import (
    analyze_two_lens_relay,
    calculate_thin_film_spectrum,
    design_quarter_wave_ar_coating,
    focus_gaussian_beam_thin_lens,
    propagate_gaussian_beam_series,
    slab_waveguide_sweep,
    suggest_single_mode_thickness_range,
    summarize_paraxial_system,
    summarize_thin_film_result,
)

from .models import AgentTrace
from .orchestrator import build_agent_trace


PlanStatus = Literal["pending", "completed", "warning", "blocked"]
GateStatus = Literal["allowed", "blocked", "requires_explicit_approval"]
RiskLevel = Literal["low", "medium", "high"]
ToolKind = Literal[
    "internal_python",
    "api_endpoint",
    "adapter_preview",
    "external_solver",
    "external_llm",
    "publication",
    "release",
]
ToolCallStatus = Literal["executed", "skipped", "blocked", "requires_explicit_approval"]
ArtifactType = Literal[
    "spec",
    "workflow_plan",
    "adapter_preview",
    "agent_trace",
    "calculator_result",
    "material_suggestions",
    "evidence",
]


class AgentPlanStep(BaseModel):
    step_index: int
    title: str
    title_zh: str
    description: str
    description_zh: str
    agent_name: str
    status: PlanStatus = "completed"
    endpoint_or_tool: str
    expected_output: str
    safety_note: str


class AgentArtifact(BaseModel):
    artifact_id: str
    label: str
    label_zh: str
    artifact_type: ArtifactType
    summary: str
    preview_content: str | None = None
    source_endpoint: str
    generated_by_agent: str
    production_grade: bool = False


class PermissionGate(BaseModel):
    gate_id: str
    label: str
    label_zh: str
    status: GateStatus
    reason: str
    risk_level: RiskLevel
    default_allowed: bool


class ToolCallRecord(BaseModel):
    call_id: str
    tool_name: str
    tool_kind: ToolKind
    called_by_agent: str
    executed: bool
    default_allowed: bool
    status: ToolCallStatus
    input_summary: str
    output_summary: str
    reason: str
    safety_note: str


class AgentTaskSession(BaseModel):
    session_id: str
    user_goal: str
    requirement_template_id: str | None = None
    optical_intent_summary: str
    optical_language_summary: dict[str, str] = Field(default_factory=dict)
    source_model: OpticalSourceModel | None = None
    monitor_model: OpticalMonitorModel | None = None
    optical_language_diagnostics: OpticalLanguageDiagnostics = Field(
        default_factory=OpticalLanguageDiagnostics
    )
    observable_diagnostics: list[ObservableDiagnostic] = Field(default_factory=list)
    adapter_source_monitor_mapping: AdapterSourceMonitorMapping | None = None
    match_confidence: str = "low"
    candidate_templates: list[str] = Field(default_factory=list)
    recommended_questions: list[str] = Field(default_factory=list)
    selected_example_id: str | None = None
    design_case_summary: str
    missing_required_inputs: list[str] = Field(default_factory=list)
    missing_critical_inputs: list[str] = Field(default_factory=list)
    missing_optional_inputs: list[str] = Field(default_factory=list)
    default_assumptions_applied: list[str] = Field(default_factory=list)
    plan_steps: list[AgentPlanStep] = Field(default_factory=list)
    agent_trace: AgentTrace
    artifacts: list[AgentArtifact] = Field(default_factory=list)
    permission_gates: list[PermissionGate] = Field(default_factory=list)
    tool_call_ledger: list[ToolCallRecord] = Field(default_factory=list)
    final_recommendation: str
    recommended_next_actions: list[str] = Field(default_factory=list)
    status: str = "ok"
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


EXAMPLE_BY_INTENT = {
    "nanoparticle plasmonics / scattering preview": "nanoparticle_plasmonics",
    "waveguide mode preview": "waveguide_mode",
    "thin film coating preview": "thin_film_coating",
    "photonic crystal band preview": "photonic_crystal_band",
    "dielectric metasurface preview": "dielectric_metasurface_preview",
    "lens ray tracing preview": "lens_raytrace_preview",
}


def build_agent_task_session(user_goal: str, example_id: str | None = None) -> AgentTaskSession:
    """Build a local, deterministic task session for Agent Studio.

    The builder never calls an external LLM, never executes a solver, and never
    touches network/upload/release workflows. It composes the existing local
    material catalog, example registry, and sub-agent trace into one task-level
    view for the frontend command center.
    """

    goal = user_goal.strip()
    if not goal:
        raise ValueError("Agent task session requires a non-empty goal.")

    requirement_match = match_goal_to_template(goal)
    matched_template = requirement_match.matched_template
    source_monitor = infer_source_monitor_from_goal(
        goal,
        template_id=requirement_match.matched_template_id,
    )
    optical_intent = (
        matched_template.optical_intent
        if matched_template is not None
        else _detect_optical_intent(goal)
    )
    selected_example_id = example_id or (
        matched_template.design_case_id if matched_template is not None else EXAMPLE_BY_INTENT.get(optical_intent)
    )
    example_detail = None
    if selected_example_id:
        try:
            example_detail = get_optical_design_example(selected_example_id)
        except ExampleRegistryError:
            if example_id:
                raise
            selected_example_id = None

    if selected_example_id:
        trace = build_example_agent_trace(selected_example_id)
        trace.design_goal = goal
    else:
        trace = build_agent_trace({"text": goal, "design_goal": goal})

    application = _application_for_intent(optical_intent)
    material_suggestions = [item.material_id for item in suggest_materials_for_application(application)]
    if material_suggestions:
        trace.material_suggestions = material_suggestions

    adapter_recommendation = trace.adapter_recommendation or _adapter_for_intent(optical_intent)
    trace.adapter_recommendation = adapter_recommendation
    observable_diagnostics = diagnose_observable(
        source_monitor.source_model,
        source_monitor.monitor_model,
        template_id=requirement_match.matched_template_id,
    )
    adapter_mapping = map_source_monitor_to_adapter(
        adapter_recommendation,
        source_monitor.source_model,
        source_monitor.monitor_model,
        observable_diagnostics,
    )
    session_hash = hashlib.sha1(f"{goal}|{selected_example_id or ''}".encode("utf-8")).hexdigest()[:10]
    design_case_summary = _design_case_summary(
        optical_intent,
        selected_example_id,
        requirement_match,
    )
    missing_critical_inputs = sorted(
        set(requirement_match.missing_disambiguation_inputs)
        | set(source_monitor.diagnostics.missing_critical_inputs)
    )
    missing_optional_inputs = sorted(set(source_monitor.diagnostics.missing_optional_inputs))
    recommended_questions = _session_questions(
        requirement_match,
        source_monitor.diagnostics,
    )

    return AgentTaskSession(
        session_id=f"session-{session_hash}",
        user_goal=goal,
        requirement_template_id=requirement_match.matched_template_id,
        optical_intent_summary=optical_intent,
        optical_language_summary=requirement_match.optical_language_summary,
        source_model=source_monitor.source_model,
        monitor_model=source_monitor.monitor_model,
        optical_language_diagnostics=source_monitor.diagnostics,
        observable_diagnostics=observable_diagnostics,
        adapter_source_monitor_mapping=adapter_mapping,
        match_confidence=requirement_match.confidence,
        candidate_templates=requirement_match.candidate_templates,
        recommended_questions=recommended_questions,
        selected_example_id=selected_example_id,
        design_case_summary=design_case_summary,
        missing_required_inputs=sorted(
            set(requirement_match.missing_required_inputs)
            | set(source_monitor.diagnostics.missing_required_inputs)
            | set(missing_critical_inputs)
        ),
        missing_critical_inputs=missing_critical_inputs,
        missing_optional_inputs=missing_optional_inputs,
        default_assumptions_applied=[
            *requirement_match.default_assumptions,
            *source_monitor.diagnostics.default_assumptions_applied,
        ],
        plan_steps=_plan_steps(optical_intent, selected_example_id, adapter_recommendation),
        agent_trace=trace,
        artifacts=_artifacts(
            selected_example_id=selected_example_id,
            optical_intent=optical_intent,
            materials=trace.material_suggestions,
            adapter_recommendation=adapter_recommendation,
            source_model=source_monitor.source_model,
            monitor_model=source_monitor.monitor_model,
            observable_diagnostics=observable_diagnostics,
            adapter_mapping=adapter_mapping,
        ),
        permission_gates=_permission_gates(),
        tool_call_ledger=_tool_call_ledger(
            optical_intent=optical_intent,
            selected_example_id=selected_example_id,
            adapter_recommendation=adapter_recommendation,
            requirement_match=requirement_match,
            source_monitor=source_monitor,
            observable_diagnostics=observable_diagnostics,
            adapter_mapping=adapter_mapping,
        ),
        final_recommendation=(
            f"Use the local {design_case_summary} path, inspect material candidates "
            f"{', '.join(trace.material_suggestions) or 'from the material catalog'}, "
            f"then review any calculator preview, workflow plan, and adapter preview via "
            f"{adapter_recommendation}. Observable previews supported by the adapter mapping: "
            f"{', '.join(adapter_mapping.supported_observables) or 'review required'}. "
            "Real solver monitor results require explicit solver execution when applicable."
        ),
        recommended_next_actions=[
            "Review the optical intent and selected design case.",
            "Answer recommended questions for any low-confidence or under-specified goal.",
            "Inspect permission gates before any optional external action.",
            "Inspect observable diagnostics and adapter-native source/monitor mapping.",
            "Open the Agent Trace Timeline to review sub-agent contributions.",
            "Generate local workflow and adapter-preview artifacts only.",
        ],
        status="ok" if example_detail or selected_example_id is None else "needs_review",
    )


def _detect_optical_intent(goal: str) -> str:
    lowered = goal.lower()
    if any(token in lowered for token in ("nanoparticle", "plasmon", "scattering", "纳米", "散射")):
        return "nanoparticle plasmonics / scattering preview"
    if any(token in lowered for token in ("gaussian", "beam waist", "rayleigh", "高斯光束", "光腰")):
        return "gaussian beam propagation preview"
    if any(token in lowered for token in ("waveguide", "mode", "波导", "模式")):
        return "waveguide mode preview"
    if any(token in lowered for token in ("thin film", "coating", "膜", "镀膜")):
        return "thin film coating preview"
    if any(token in lowered for token in ("photonic crystal", "band", "光子晶体", "能带")):
        return "photonic crystal band preview"
    if any(token in lowered for token in ("metasurface", "metalens", "超表面", "超透镜")):
        return "dielectric metasurface preview"
    if any(token in lowered for token in ("lens", "ray", "透镜", "光线")):
        return "lens ray tracing preview"
    return "general optical design preview"


def _application_for_intent(intent: str) -> str:
    if "nanoparticle" in intent:
        return "nanoparticle plasmonics"
    if "waveguide" in intent:
        return "waveguide"
    if "thin film" in intent:
        return "thin film coating"
    if "photonic crystal" in intent:
        return "photonic crystal band"
    if "metasurface" in intent:
        return "dielectric metasurface"
    if "lens" in intent:
        return "lens/ray optics"
    if "gaussian" in intent:
        return "gaussian beam"
    return "general optical preview"


def _adapter_for_intent(intent: str) -> str:
    if "photonic crystal" in intent:
        return "mpb"
    if "lens" in intent:
        return "optiland"
    if "waveguide" in intent:
        return "mpb or elmer preview"
    if "thin film" in intent:
        return "preview-only; future TMM adapter candidate"
    if "nanoparticle" in intent or "metasurface" in intent:
        return "meep with gmsh geometry preview"
    return "adapter auto-selection preview"


def _design_case_summary(
    intent: str,
    selected_example_id: str | None,
    requirement_match: RequirementMatchResult,
) -> str:
    if requirement_match.matched_template is not None:
        template = requirement_match.matched_template
        case = selected_example_id or "template-only case"
        return f"{template.template_id} requirement template -> {case} -> {intent}"
    if selected_example_id:
        return f"{selected_example_id} example-backed {intent}"
    return f"generic {intent}"


def _session_questions(
    requirement_match: RequirementMatchResult,
    diagnostics: OpticalLanguageDiagnostics,
) -> list[str]:
    questions = [
        *requirement_match.recommended_questions,
        *diagnostics.blocking_questions,
        *generate_disambiguation_questions(
            template_id=requirement_match.matched_template_id,
            missing_critical_inputs=diagnostics.missing_critical_inputs,
            missing_optional_inputs=diagnostics.missing_optional_inputs,
            candidate_templates=requirement_match.candidate_templates,
        ),
    ]
    unique: list[str] = []
    seen: set[str] = set()
    for question in questions:
        if question and question not in seen:
            unique.append(question)
            seen.add(question)
    return unique


def _plan_steps(
    intent: str,
    selected_example_id: str | None,
    adapter_recommendation: str,
) -> list[AgentPlanStep]:
    example_note = selected_example_id or "no bundled example selected"
    return [
        AgentPlanStep(
            step_index=1,
            title="Natural language -> optical language",
            title_zh="自然语言 -> 光学语言",
            description=f"Translate the natural language goal into optical intent: {intent}.",
            description_zh=f"将自然语言目标转换为光学意图：{intent}。",
            agent_name="SpecAgent",
            endpoint_or_tool="requirements.match_template and requirements.extract_optical_intent",
            expected_output="optical_intent_summary and optical_language_summary",
            safety_note="No external LLM is called by default.",
        ),
        AgentPlanStep(
            step_index=2,
            title="Optical language -> design case",
            title_zh="光学语言 -> 设计案例",
            description=f"Match the goal to {example_note}.",
            description_zh=f"将目标匹配到 {example_note}。",
            agent_name="SpecAgent",
            endpoint_or_tool="/api/design-requirements and /api/examples",
            expected_output="requirement_template_id, selected_example_id, and design_case_summary",
            safety_note="Examples are local preview cases only.",
        ),
        AgentPlanStep(
            step_index=3,
            title="Infer source and monitor",
            title_zh="推断光源和监测器",
            description="Infer preview source, monitor, observable, and default assumptions.",
            description_zh="推断预览光源、监测器、观测量和默认假设。",
            agent_name="SpecAgent",
            endpoint_or_tool="optical_language.infer_source_monitor",
            expected_output="source_model, monitor_model, and optical_language_diagnostics",
            safety_note="Monitor definitions are preview metadata; no external solver monitor was executed.",
        ),
        AgentPlanStep(
            step_index=4,
            title="Check missing source/monitor inputs",
            title_zh="检查缺失的光源/监测器输入",
            description="Report missing inputs, ambiguity notes, and blocking questions before solver use.",
            description_zh="在任何求解器使用前报告缺失输入、歧义说明和阻断问题。",
            agent_name="SafetyAgent",
            endpoint_or_tool="optical_language.diagnose_missing_inputs",
            expected_output="missing_required_inputs and safe_to_run_solver=false",
            safety_note="safe_to_preview can be true while safe_to_run_solver remains false.",
        ),
        AgentPlanStep(
            step_index=5,
            title="Suggest materials",
            title_zh="推荐材料",
            description="Use the local preview material catalog for candidate materials.",
            description_zh="使用本地预览材料库生成候选材料。",
            agent_name="MaterialAgent",
            endpoint_or_tool="/api/materials/suggest",
            expected_output="material_suggestions",
            safety_note="Material data is preview/design-assist, not production-grade optical constants.",
        ),
        AgentPlanStep(
            step_index=6,
            title="Review geometry",
            title_zh="审阅几何",
            description="Identify the geometry family and missing geometry fields.",
            description_zh="识别几何类型并标出缺失几何字段。",
            agent_name="GeometryAgent",
            endpoint_or_tool="local geometry review",
            expected_output="geometry checklist",
            safety_note="Geometry remains a scaffold until reviewed.",
        ),
        AgentPlanStep(
            step_index=7,
            title="Recommend adapter",
            title_zh="推荐适配器",
            description=f"Choose an open-source-first adapter path: {adapter_recommendation}.",
            description_zh=f"选择开源优先的适配器路径：{adapter_recommendation}。",
            agent_name="AdapterAgent",
            endpoint_or_tool="/api/adapters",
            expected_output="adapter_recommendation",
            safety_note="No proprietary solver is required by default.",
        ),
        AgentPlanStep(
            step_index=8,
            title="Diagnose observables",
            title_zh="诊断观测量",
            description="Classify requested observables and mark preview-vs-real-result boundaries.",
            description_zh="分类请求的观测量，并标记预览与真实结果的边界。",
            agent_name="EvidenceAgent",
            endpoint_or_tool="optical_language.diagnose_observable",
            expected_output="observable_diagnostics",
            safety_note="Observable diagnostics are metadata; no solver result is claimed.",
        ),
        AgentPlanStep(
            step_index=9,
            title="Map source/monitor to adapter preview",
            title_zh="映射光源/监测器到适配器预览",
            description="Translate source, monitor, and observable intent into adapter-native preview terms.",
            description_zh="将光源、监测器和观测量意图转换为适配器原生预览语义。",
            agent_name="AdapterAgent",
            endpoint_or_tool="optical_language.map_source_monitor_to_adapter",
            expected_output="adapter_source_monitor_mapping",
            safety_note="Mapping is preview/design-assist metadata, not a solver monitor result.",
        ),
        AgentPlanStep(
            step_index=10,
            title="Plan local tool calls",
            title_zh="规划本地工具调用",
            description="Plan parse, validate, preview, evidence, and human review steps.",
            description_zh="规划解析、验证、预览、证据和人工审阅步骤。",
            agent_name="WorkflowAgent",
            endpoint_or_tool="/api/workflow-plan and local optical calculators when applicable",
            expected_output="workflow_plan artifact and tool_call_ledger",
            safety_note="No solver is executed by default.",
        ),
        AgentPlanStep(
            step_index=11,
            title="Preview artifacts and evidence",
            title_zh="预览产物和证据",
            description="Prepare preview artifacts and validation evidence references.",
            description_zh="准备预览产物和验证证据引用。",
            agent_name="EvidenceAgent",
            endpoint_or_tool="/api/adapter-preview and /api/validation-evidence",
            expected_output="adapter_preview and evidence artifacts",
            safety_note="No production-grade physical validation is claimed.",
        ),
        AgentPlanStep(
            step_index=12,
            title="Check permission gates",
            title_zh="检查权限门控",
            description="Block solver, LLM, upload, publish, tag, and release actions by default.",
            description_zh="默认阻断求解器、LLM、上传、发布、tag 和 release 动作。",
            agent_name="SafetyAgent",
            endpoint_or_tool="local permission gate policy",
            expected_output="permission_gates",
            safety_note="Formal convergence proof is not claimed.",
        ),
    ]


def _artifacts(
    *,
    selected_example_id: str | None,
    optical_intent: str,
    materials: list[str],
    adapter_recommendation: str,
    source_model: OpticalSourceModel | None,
    monitor_model: OpticalMonitorModel | None,
    observable_diagnostics: list[ObservableDiagnostic],
    adapter_mapping: AdapterSourceMonitorMapping,
) -> list[AgentArtifact]:
    example_path = (
        f"examples/optical_design/{selected_example_id}/spec.json"
        if selected_example_id
        else "generated local preview spec summary"
    )
    artifacts = [
        AgentArtifact(
            artifact_id="spec-preview",
            label="Spec preview",
            label_zh="规格预览",
            artifact_type="spec",
            summary=f"Design intent mapped to {optical_intent}; source: {example_path}.",
            preview_content=example_path,
            source_endpoint="/api/agent-session",
            generated_by_agent="SpecAgent",
        ),
        AgentArtifact(
            artifact_id="material-suggestions",
            label="Material suggestions",
            label_zh="材料建议",
            artifact_type="material_suggestions",
            summary=", ".join(materials) if materials else "Review local material catalog.",
            source_endpoint="/api/materials/suggest",
            generated_by_agent="MaterialAgent",
        ),
        AgentArtifact(
            artifact_id="agent-trace",
            label="Sub-agent trace",
            label_zh="子智能体轨迹",
            artifact_type="agent_trace",
            summary="Eight-agent deterministic collaboration trace.",
            source_endpoint="/api/agent-session",
            generated_by_agent="RecommendationAgent",
        ),
        AgentArtifact(
            artifact_id="workflow-plan",
            label="Workflow plan",
            label_zh="工作流计划",
            artifact_type="workflow_plan",
            summary=f"Local parse -> validate -> preview workflow for {adapter_recommendation}.",
            source_endpoint="/api/workflow-plan",
            generated_by_agent="WorkflowAgent",
        ),
        AgentArtifact(
            artifact_id="source-monitor-metadata",
            label="Source and monitor metadata",
            label_zh="光源和监测器元数据",
            artifact_type="spec",
            summary=(
                f"Source={source_model.source_type if source_model else 'unknown'}; "
                f"monitor={monitor_model.monitor_type if monitor_model else 'unknown'}; "
                "preview metadata only."
            ),
            preview_content=(
                f"source={source_model.model_dump(mode='json') if source_model else {}}; "
                f"monitor={monitor_model.model_dump(mode='json') if monitor_model else {}}"
            ),
            source_endpoint="/api/optical-language/infer",
            generated_by_agent="SpecAgent",
        ),
        AgentArtifact(
            artifact_id="adapter-preview",
            label="Adapter preview",
            label_zh="适配器预览",
            artifact_type="adapter_preview",
            summary="Preview-only solver-native scaffold; no solver execution.",
            source_endpoint="/api/adapter-preview",
            generated_by_agent="AdapterAgent",
        ),
        AgentArtifact(
            artifact_id="observable-diagnostics",
            label="Observable diagnostics",
            label_zh="观测量诊断",
            artifact_type="evidence",
            summary=(
                ", ".join(item.observable_kind for item in observable_diagnostics)
                if observable_diagnostics
                else "No observable diagnostics produced."
            ),
            preview_content=str([item.model_dump(mode="json") for item in observable_diagnostics]),
            source_endpoint="/api/optical-language/observables/diagnose",
            generated_by_agent="EvidenceAgent",
        ),
        AgentArtifact(
            artifact_id="adapter-native-source-monitor-preview",
            label="Adapter-native source/monitor preview",
            label_zh="适配器原生光源/监测器预览",
            artifact_type="adapter_preview",
            summary=(
                f"{adapter_mapping.adapter_name}: "
                f"{', '.join(adapter_mapping.supported_observables) or 'review observables'}; "
                "preview metadata only."
            ),
            preview_content=str(adapter_mapping.model_dump(mode="json")),
            source_endpoint="/api/optical-language/adapter-mapping",
            generated_by_agent="AdapterAgent",
        ),
        AgentArtifact(
            artifact_id="validation-evidence",
            label="Validation evidence",
            label_zh="验证证据",
            artifact_type="evidence",
            summary="Adapter maturity and validation evidence references.",
            source_endpoint="/api/validation-evidence",
            generated_by_agent="EvidenceAgent",
        ),
    ]
    calculator_summary = _calculator_artifact_summary(optical_intent)
    if calculator_summary is not None:
        artifacts.append(
            AgentArtifact(
                artifact_id="calculator-preview",
                label="Calculator preview",
                label_zh="计算器预览",
                artifact_type="calculator_result",
                summary=calculator_summary["summary"],
                preview_content=str(calculator_summary),
                source_endpoint=calculator_summary["source_endpoint"],
                generated_by_agent="WorkflowAgent",
            )
        )
    return artifacts


def _calculator_artifact_summary(optical_intent: str) -> dict[str, str] | None:
    if "thin film" in optical_intent:
        spectrum = calculate_thin_film_spectrum(
            [{"n": 1.38, "thickness_nm": 100.0}],
            450.0,
            700.0,
            6,
            incident_n=1.0,
            substrate_n=1.5,
        )
        ar = design_quarter_wave_ar_coating(substrate_n=1.5, target_wavelength_nm=550.0)
        return {
            "summary": (
                f"{summarize_thin_film_result(spectrum)['summary']} "
                f"{summarize_thin_film_result(ar)['summary']}"
            ),
            "source_endpoint": "/api/optics/thin-film-spectrum and /api/optics/quarter-wave-ar",
        }
    if "lens" in optical_intent:
        relay = analyze_two_lens_relay(
            f1_mm=50.0,
            f2_mm=100.0,
            separation_mm=150.0,
            object_distance_mm=100.0,
        )
        return {
            "summary": str(summarize_paraxial_system(relay)["summary"]),
            "source_endpoint": "/api/optics/two-lens-relay",
        }
    if "waveguide" in optical_intent:
        sweep = slab_waveguide_sweep(
            core_n=2.0,
            cladding_n=1.44,
            wavelength_nm=1550.0,
            thickness_start_um=0.1,
            thickness_stop_um=0.6,
            points=6,
        )
        single_mode = suggest_single_mode_thickness_range(
            core_n=2.0,
            cladding_n=1.44,
            wavelength_nm=1550.0,
        )
        return {
            "summary": f"{sweep.result['summary']} {single_mode.result['summary']}",
            "source_endpoint": "/api/optics/waveguide-sweep and /api/optics/waveguide-single-mode-range",
        }
    if "gaussian" in optical_intent.lower():
        series = propagate_gaussian_beam_series(
            wavelength_nm=1064.0,
            waist_um=10.0,
            z_start_mm=0.0,
            z_stop_mm=10.0,
            points=5,
        )
        focus = focus_gaussian_beam_thin_lens(
            wavelength_nm=1064.0,
            input_waist_um=1000.0,
            focal_length_mm=50.0,
        )
        return {
            "summary": f"{series.result['summary']} {focus.result['summary']}",
            "source_endpoint": "/api/optics/gaussian-beam-series and /api/optics/gaussian-beam-focus",
        }
    return None


def _tool_call_ledger(
    *,
    optical_intent: str,
    selected_example_id: str | None,
    adapter_recommendation: str,
    requirement_match: RequirementMatchResult,
    source_monitor: Any,
    observable_diagnostics: list[ObservableDiagnostic],
    adapter_mapping: AdapterSourceMonitorMapping,
) -> list[ToolCallRecord]:
    ledger = [
        ToolCallRecord(
            call_id="requirements-match-template",
            tool_name="requirements.match_template",
            tool_kind="internal_python",
            called_by_agent="SpecAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary="Natural-language goal.",
            output_summary=(
                f"Matched {requirement_match.matched_template_id} with "
                f"{requirement_match.confidence} confidence."
                if requirement_match.matched_template_id
                else "No template matched; returned generic safe preview guidance."
            ),
            reason="The command center starts from deterministic requirement-template matching.",
            safety_note="No external LLM is called by default.",
        ),
        ToolCallRecord(
            call_id="requirements-extract-optical-intent",
            tool_name="requirements.extract_optical_intent",
            tool_kind="internal_python",
            called_by_agent="SpecAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary=requirement_match.matched_template_id or optical_intent,
            output_summary=(
                requirement_match.optical_language_summary.get(
                    "calculator_or_tool_path",
                    "Generic optical language summary produced.",
                )
            ),
            reason="The backend exposes the natural language -> optical language step explicitly.",
            safety_note="Optical language extraction is local heuristic logic, not an external model.",
        ),
        ToolCallRecord(
            call_id="requirements-match-ambiguity-check",
            tool_name="requirements.match_ambiguity_check",
            tool_kind="internal_python",
            called_by_agent="SpecAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary="Template scores and candidate template set.",
            output_summary=(
                f"confidence={requirement_match.confidence}; "
                f"candidates={', '.join(requirement_match.candidate_templates) or 'none'}"
            ),
            reason="Ambiguous or under-specified goals should produce questions rather than unsafe actions.",
            safety_note="No external LLM was used for disambiguation.",
        ),
        ToolCallRecord(
            call_id="optical-language-generate-disambiguation-questions",
            tool_name="optical_language.generate_disambiguation_questions",
            tool_kind="internal_python",
            called_by_agent="SafetyAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary="Matched template, candidate templates, and missing inputs.",
            output_summary=(
                f"critical={len(source_monitor.diagnostics.missing_critical_inputs)}; "
                f"optional={len(source_monitor.diagnostics.missing_optional_inputs)}"
            ),
            reason="The session should expose follow-up questions for ambiguous or incomplete requirements.",
            safety_note="Questions are deterministic local diagnostics; no solver or LLM was invoked.",
        ),
        ToolCallRecord(
            call_id="optical-language-infer-source-monitor",
            tool_name="optical_language.infer_source_monitor",
            tool_kind="internal_python",
            called_by_agent="SpecAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary=requirement_match.matched_template_id or optical_intent,
            output_summary=(
                f"source={source_monitor.source_model.source_type}; "
                f"monitor={source_monitor.monitor_model.monitor_type}"
            ),
            reason="Source, monitor, and observable assumptions must be visible before preview artifacts.",
            safety_note="No external solver monitor was executed.",
        ),
        ToolCallRecord(
            call_id="optical-language-diagnose-missing-inputs",
            tool_name="optical_language.diagnose_missing_inputs",
            tool_kind="internal_python",
            called_by_agent="SafetyAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary="Goal, requirement template, source model, and monitor model.",
            output_summary=(
                f"missing={len(source_monitor.diagnostics.missing_required_inputs)}; "
                f"safe_to_preview={source_monitor.diagnostics.safe_to_preview}; "
                f"safe_to_run_solver={source_monitor.diagnostics.safe_to_run_solver}"
            ),
            reason="Missing source/monitor inputs and defaults must be explicit.",
            safety_note="safe_to_run_solver is false by default.",
        ),
        ToolCallRecord(
            call_id="optical-language-diagnose-observable",
            tool_name="optical_language.diagnose_observable",
            tool_kind="internal_python",
            called_by_agent="EvidenceAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary=source_monitor.monitor_model.observable,
            output_summary=(
                f"observables={', '.join(item.observable_kind for item in observable_diagnostics)}"
                if observable_diagnostics
                else "No observable diagnostics produced."
            ),
            reason="Requested observables must be classified before adapter-native mapping.",
            safety_note="Observable diagnostics are preview metadata; no solver result was computed.",
        ),
        ToolCallRecord(
            call_id="optical-language-map-source-monitor-to-adapter",
            tool_name="optical_language.map_source_monitor_to_adapter",
            tool_kind="internal_python",
            called_by_agent="AdapterAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary=f"adapter={adapter_recommendation}; monitor={source_monitor.monitor_model.monitor_type}",
            output_summary=(
                f"{adapter_mapping.adapter_name}: "
                f"supported={', '.join(adapter_mapping.supported_observables) or 'none'}; "
                f"unsupported={', '.join(adapter_mapping.unsupported_observables) or 'none'}"
            ),
            reason="Adapter preview needs native source/monitor semantics.",
            safety_note="Adapter mapping is preview/design-assist metadata; no adapter solver was executed.",
        ),
        ToolCallRecord(
            call_id="material-catalog-suggest",
            tool_name="material_catalog.suggest",
            tool_kind="internal_python",
            called_by_agent="MaterialAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary=f"Application inferred from {optical_intent}.",
            output_summary="Returned local preview material candidates.",
            reason="Material suggestions are needed before adapter/workflow planning.",
            safety_note="Local preview catalog only; not production-grade optical constants.",
        ),
        ToolCallRecord(
            call_id="example-registry-load",
            tool_name="example_registry.load",
            tool_kind="internal_python",
            called_by_agent="SpecAgent",
            executed=selected_example_id is not None,
            default_allowed=True,
            status="executed" if selected_example_id is not None else "skipped",
            input_summary=selected_example_id or "No bundled example matched or requested.",
            output_summary=(
                f"Loaded {selected_example_id} from examples/optical_design."
                if selected_example_id
                else "No local example file was loaded."
            ),
            reason="Use local examples when the user goal matches a known optical design case.",
            safety_note="Example loading is repo-local and does not access the network.",
        ),
        ToolCallRecord(
            call_id="agent-trace-build",
            tool_name="agent_trace.build",
            tool_kind="internal_python",
            called_by_agent="RecommendationAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary="Optical intent, materials, adapter recommendation, and example context.",
            output_summary="Built deterministic eight-role sub-agent trace.",
            reason="The command center needs visible collaboration trace data.",
            safety_note="Trace is deterministic local Python; no external LLM is called.",
        ),
        ToolCallRecord(
            call_id="workflow-plan-preview",
            tool_name="workflow_plan.preview",
            tool_kind="api_endpoint",
            called_by_agent="WorkflowAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary=f"Adapter path: {adapter_recommendation}.",
            output_summary="Prepared local workflow-plan preview steps.",
            reason="Workflow planning is a local preview operation.",
            safety_note="No solver execution is part of workflow planning by default.",
        ),
        ToolCallRecord(
            call_id="adapter-preview-generate",
            tool_name="adapter_preview.generate",
            tool_kind="adapter_preview",
            called_by_agent="AdapterAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary=f"Preview adapter path: {adapter_recommendation}.",
            output_summary="Prepared preview scaffold metadata; solver process not launched.",
            reason="Adapter preview makes artifacts inspectable without running a solver.",
            safety_note="Preview generation is not production-grade physical validation.",
        ),
    ]
    calculator_record = _calculator_tool_call(optical_intent)
    if calculator_record is not None:
        ledger.append(calculator_record)
    ledger.extend(_blocked_tool_calls())
    return ledger


def _calculator_tool_call(optical_intent: str) -> ToolCallRecord | None:
    if "thin film" in optical_intent:
        return ToolCallRecord(
            call_id="optics-thin-film-spectrum",
            tool_name="optics.thin_film.spectrum",
            tool_kind="internal_python",
            called_by_agent="WorkflowAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary="Thin-film/coating intent detected.",
            output_summary="Prepared wavelength-sweep and quarter-wave AR preview calculations.",
            reason="Thin-film spectrum and AR helper are deterministic local design-assist tools.",
            safety_note="Calculator output is preview/design-assist, not production validation.",
        )
    if "lens" in optical_intent:
        return ToolCallRecord(
            call_id="optics-paraxial-two-lens-relay",
            tool_name="optics.paraxial.two_lens_relay",
            tool_kind="internal_python",
            called_by_agent="WorkflowAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary="Lens/ray optics intent detected.",
            output_summary="Prepared two-lens relay and paraxial system preview estimate.",
            reason="Paraxial estimates are deterministic local design-assist tools.",
            safety_note="Paraxial preview is not full ray-trace validation.",
        )
    if "waveguide" in optical_intent:
        return ToolCallRecord(
            call_id="optics-waveguide-sweep",
            tool_name="optics.waveguide.sweep",
            tool_kind="internal_python",
            called_by_agent="WorkflowAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary="Waveguide intent detected.",
            output_summary="Prepared slab waveguide V-number sweep and single-mode range preview.",
            reason="V-number estimates provide local design orientation before solver setup.",
            safety_note="Waveguide estimate is not a mode-solver result.",
        )
    if "gaussian" in optical_intent.lower():
        return ToolCallRecord(
            call_id="optics-gaussian-beam-series",
            tool_name="optics.gaussian_beam.series",
            tool_kind="internal_python",
            called_by_agent="WorkflowAgent",
            executed=True,
            default_allowed=True,
            status="executed",
            input_summary="Gaussian beam intent detected.",
            output_summary="Prepared Gaussian beam series and thin-lens focus preview estimates.",
            reason="Gaussian beam formulas provide local design-assist calculations.",
            safety_note="Gaussian beam output is paraxial preview only.",
        )
    return None


def _blocked_tool_calls() -> list[ToolCallRecord]:
    return [
        ToolCallRecord(
            call_id="external-solver-meep",
            tool_name="external_solver.meep",
            tool_kind="external_solver",
            called_by_agent="SafetyAgent",
            executed=False,
            default_allowed=False,
            status="requires_explicit_approval",
            input_summary="Potential Meep execution request.",
            output_summary="No Meep process was launched.",
            reason="External solvers require explicit maintainer/user approval.",
            safety_note="No solver is executed by default.",
        ),
        ToolCallRecord(
            call_id="external-solver-gmsh",
            tool_name="external_solver.gmsh",
            tool_kind="external_solver",
            called_by_agent="SafetyAgent",
            executed=False,
            default_allowed=False,
            status="requires_explicit_approval",
            input_summary="Potential Gmsh execution request.",
            output_summary="No Gmsh process was launched.",
            reason="External solvers require explicit maintainer/user approval.",
            safety_note="No solver is executed by default.",
        ),
        ToolCallRecord(
            call_id="external-solver-mpb",
            tool_name="external_solver.mpb",
            tool_kind="external_solver",
            called_by_agent="SafetyAgent",
            executed=False,
            default_allowed=False,
            status="requires_explicit_approval",
            input_summary="Potential MPB execution request.",
            output_summary="No MPB process was launched.",
            reason="External solvers require explicit maintainer/user approval.",
            safety_note="No solver is executed by default.",
        ),
        ToolCallRecord(
            call_id="external-solver-elmer",
            tool_name="external_solver.elmer",
            tool_kind="external_solver",
            called_by_agent="SafetyAgent",
            executed=False,
            default_allowed=False,
            status="requires_explicit_approval",
            input_summary="Potential ElmerSolver execution request.",
            output_summary="No Elmer process was launched.",
            reason="Elmer remains install-deferred and is never run by default.",
            safety_note="Elmer is not marked Level 3.",
        ),
        ToolCallRecord(
            call_id="external-solver-optiland",
            tool_name="external_solver.optiland",
            tool_kind="external_solver",
            called_by_agent="SafetyAgent",
            executed=False,
            default_allowed=False,
            status="requires_explicit_approval",
            input_summary="Potential Optiland execution request.",
            output_summary="No Optiland process was launched.",
            reason="External solver/tool execution requires explicit approval.",
            safety_note="No solver is executed by default.",
        ),
        ToolCallRecord(
            call_id="external-llm",
            tool_name="external_llm",
            tool_kind="external_llm",
            called_by_agent="SafetyAgent",
            executed=False,
            default_allowed=False,
            status="requires_explicit_approval",
            input_summary="Potential external LLM call.",
            output_summary="No external LLM call was made.",
            reason="The backend is deterministic/local by default.",
            safety_note="No external LLM is called by default.",
        ),
        ToolCallRecord(
            call_id="testpypi-upload",
            tool_name="testpypi_upload",
            tool_kind="publication",
            called_by_agent="SafetyAgent",
            executed=False,
            default_allowed=False,
            status="blocked",
            input_summary="Potential TestPyPI upload.",
            output_summary="No upload command is exposed or executed.",
            reason="Uploads require explicit maintainer approval outside Agent Studio.",
            safety_note="NO UPLOAD PERFORMED.",
        ),
        ToolCallRecord(
            call_id="pypi-publish",
            tool_name="pypi_publish",
            tool_kind="publication",
            called_by_agent="SafetyAgent",
            executed=False,
            default_allowed=False,
            status="blocked",
            input_summary="Potential PyPI publication.",
            output_summary="No PyPI publication is exposed or executed.",
            reason="PyPI is not published and approval is not granted.",
            safety_note="NO UPLOAD PERFORMED.",
        ),
        ToolCallRecord(
            call_id="git-tag-create",
            tool_name="git_tag_create",
            tool_kind="release",
            called_by_agent="SafetyAgent",
            executed=False,
            default_allowed=False,
            status="blocked",
            input_summary="Potential git tag creation.",
            output_summary="No tag was created.",
            reason="Release actions are out of scope for backend tool-call previews.",
            safety_note="NO TAG CREATED.",
        ),
        ToolCallRecord(
            call_id="github-release-create",
            tool_name="github_release_create",
            tool_kind="release",
            called_by_agent="SafetyAgent",
            executed=False,
            default_allowed=False,
            status="blocked",
            input_summary="Potential GitHub release creation.",
            output_summary="No release was created.",
            reason="Release actions require separate explicit approval.",
            safety_note="NO RELEASE CREATED.",
        ),
    ]


def _permission_gates() -> list[PermissionGate]:
    return [
        PermissionGate(
            gate_id="parse_local_spec",
            label="Parse local spec",
            label_zh="本地解析规格",
            status="allowed",
            reason="Local deterministic parsing is part of the preview workflow.",
            risk_level="low",
            default_allowed=True,
        ),
        PermissionGate(
            gate_id="read_local_material_catalog",
            label="Read local material catalog",
            label_zh="读取本地材料库",
            status="allowed",
            reason="The catalog is bundled and preview-only.",
            risk_level="low",
            default_allowed=True,
        ),
        PermissionGate(
            gate_id="generate_workflow_plan",
            label="Generate workflow plan",
            label_zh="生成工作流计划",
            status="allowed",
            reason="Workflow planning is local and does not execute solvers.",
            risk_level="low",
            default_allowed=True,
        ),
        PermissionGate(
            gate_id="generate_adapter_preview",
            label="Generate adapter preview",
            label_zh="生成适配器预览",
            status="allowed",
            reason="Adapter preview produces scaffold content only.",
            risk_level="low",
            default_allowed=True,
        ),
        PermissionGate(
            gate_id="run_external_solver",
            label="External solver execution",
            label_zh="外部求解器执行",
            status="requires_explicit_approval",
            reason="External solvers are never executed by default.",
            risk_level="high",
            default_allowed=False,
        ),
        PermissionGate(
            gate_id="call_external_llm",
            label="External LLM call",
            label_zh="外部 LLM 调用",
            status="requires_explicit_approval",
            reason="The command center is deterministic and local by default.",
            risk_level="high",
            default_allowed=False,
        ),
        PermissionGate(
            gate_id="upload_testpypi",
            label="TestPyPI upload",
            label_zh="TestPyPI 上传",
            status="blocked",
            reason="Publishing controls are not exposed in Agent Studio.",
            risk_level="high",
            default_allowed=False,
        ),
        PermissionGate(
            gate_id="publish_pypi",
            label="PyPI publication",
            label_zh="PyPI 发布",
            status="blocked",
            reason="PyPI publication requires separate maintainer approval outside this UI.",
            risk_level="high",
            default_allowed=False,
        ),
        PermissionGate(
            gate_id="create_git_tag",
            label="Git tag creation",
            label_zh="Git tag 创建",
            status="blocked",
            reason="Release/tag operations are out of scope for the local command center.",
            risk_level="high",
            default_allowed=False,
        ),
        PermissionGate(
            gate_id="create_github_release",
            label="GitHub release creation",
            label_zh="GitHub release 创建",
            status="blocked",
            reason="GitHub release operations are not controlled from Agent Studio.",
            risk_level="high",
            default_allowed=False,
        ),
    ]
