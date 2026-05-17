"""Deterministic local Agent Task Session builder."""

from __future__ import annotations

import hashlib
from typing import Literal

from pydantic import BaseModel, Field

from optical_spec_agent.examples.registry import (
    ExampleRegistryError,
    build_example_agent_trace,
    get_optical_design_example,
)
from optical_spec_agent.materials.catalog import suggest_materials_for_application

from .models import AgentTrace
from .orchestrator import build_agent_trace


PlanStatus = Literal["pending", "completed", "warning", "blocked"]
GateStatus = Literal["allowed", "blocked", "requires_explicit_approval"]
RiskLevel = Literal["low", "medium", "high"]
ArtifactType = Literal[
    "spec",
    "workflow_plan",
    "adapter_preview",
    "agent_trace",
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


class AgentTaskSession(BaseModel):
    session_id: str
    user_goal: str
    optical_intent_summary: str
    selected_example_id: str | None = None
    design_case_summary: str
    plan_steps: list[AgentPlanStep] = Field(default_factory=list)
    agent_trace: AgentTrace
    artifacts: list[AgentArtifact] = Field(default_factory=list)
    permission_gates: list[PermissionGate] = Field(default_factory=list)
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

    optical_intent = _detect_optical_intent(goal)
    selected_example_id = example_id or EXAMPLE_BY_INTENT.get(optical_intent)
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
    session_hash = hashlib.sha1(f"{goal}|{selected_example_id or ''}".encode("utf-8")).hexdigest()[:10]
    design_case_summary = _design_case_summary(optical_intent, selected_example_id)

    return AgentTaskSession(
        session_id=f"session-{session_hash}",
        user_goal=goal,
        optical_intent_summary=optical_intent,
        selected_example_id=selected_example_id,
        design_case_summary=design_case_summary,
        plan_steps=_plan_steps(optical_intent, selected_example_id, adapter_recommendation),
        agent_trace=trace,
        artifacts=_artifacts(
            selected_example_id=selected_example_id,
            optical_intent=optical_intent,
            materials=trace.material_suggestions,
            adapter_recommendation=adapter_recommendation,
        ),
        permission_gates=_permission_gates(),
        final_recommendation=(
            f"Use the local {design_case_summary} path, inspect material candidates "
            f"{', '.join(trace.material_suggestions) or 'from the material catalog'}, "
            f"then generate a workflow plan and adapter preview via {adapter_recommendation}."
        ),
        recommended_next_actions=[
            "Review the optical intent and selected design case.",
            "Inspect permission gates before any optional external action.",
            "Open the Agent Trace Timeline to review sub-agent contributions.",
            "Generate local workflow and adapter-preview artifacts only.",
        ],
        status="ok" if example_detail or selected_example_id is None else "needs_review",
    )


def _detect_optical_intent(goal: str) -> str:
    lowered = goal.lower()
    if any(token in lowered for token in ("nanoparticle", "plasmon", "scattering", "纳米", "散射")):
        return "nanoparticle plasmonics / scattering preview"
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


def _design_case_summary(intent: str, selected_example_id: str | None) -> str:
    if selected_example_id:
        return f"{selected_example_id} example-backed {intent}"
    return f"generic {intent}"


def _plan_steps(
    intent: str,
    selected_example_id: str | None,
    adapter_recommendation: str,
) -> list[AgentPlanStep]:
    example_note = selected_example_id or "no bundled example selected"
    return [
        AgentPlanStep(
            step_index=1,
            title="Interpret optical goal",
            title_zh="理解光学目标",
            description=f"Translate the natural language goal into {intent}.",
            description_zh=f"将自然语言目标转换为 {intent}。",
            agent_name="SpecAgent",
            endpoint_or_tool="local heuristic intent detector",
            expected_output="optical_intent_summary",
            safety_note="No external LLM is called by default.",
        ),
        AgentPlanStep(
            step_index=2,
            title="Select design case",
            title_zh="选择设计案例",
            description=f"Match the goal to {example_note}.",
            description_zh=f"将目标匹配到 {example_note}。",
            agent_name="SpecAgent",
            endpoint_or_tool="/api/examples",
            expected_output="selected_example_id and design_case_summary",
            safety_note="Examples are local preview cases only.",
        ),
        AgentPlanStep(
            step_index=3,
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
            step_index=4,
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
            step_index=5,
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
            step_index=6,
            title="Plan local workflow",
            title_zh="规划本地工作流",
            description="Plan parse, validate, preview, evidence, and human review steps.",
            description_zh="规划解析、验证、预览、证据和人工审阅步骤。",
            agent_name="WorkflowAgent",
            endpoint_or_tool="/api/workflow-plan",
            expected_output="workflow_plan artifact",
            safety_note="No solver is executed by default.",
        ),
        AgentPlanStep(
            step_index=7,
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
            step_index=8,
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
) -> list[AgentArtifact]:
    example_path = (
        f"examples/optical_design/{selected_example_id}/spec.json"
        if selected_example_id
        else "generated local preview spec summary"
    )
    return [
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
            artifact_id="adapter-preview",
            label="Adapter preview",
            label_zh="适配器预览",
            artifact_type="adapter_preview",
            summary="Preview-only solver-native scaffold; no solver execution.",
            source_endpoint="/api/adapter-preview",
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
