"""Deterministic local sub-agent trace builder."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from optical_spec_agent.materials.catalog import suggest_materials_for_application

from .models import AgentStep, AgentTrace


def _stringify_request(request: Any) -> str:
    if isinstance(request, str):
        return request
    try:
        return json.dumps(request, ensure_ascii=False, sort_keys=True)
    except TypeError:
        return str(request)


def _detect_application(text: str) -> str:
    lowered = text.lower()
    if any(word in lowered for word in ("nanoparticle", "plasmon", "散射", "纳米")):
        return "nanoparticle plasmonics"
    if any(word in lowered for word in ("thin film", "coating", "薄膜")):
        return "thin film coating"
    if any(word in lowered for word in ("waveguide", "mode", "波导")):
        return "waveguide mode"
    if any(word in lowered for word in ("photonic crystal", "band", "光子晶体")):
        return "photonic crystal band"
    if any(word in lowered for word in ("lens", "ray", "透镜")):
        return "lens/ray optics"
    if any(word in lowered for word in ("metasurface", "metalens", "超表面")):
        return "dielectric metasurface"
    return "general optical preview"


def _adapter_for_application(application: str) -> str:
    if application == "photonic crystal band":
        return "mpb"
    if application == "lens/ray optics":
        return "optiland"
    if application == "thin film coating":
        return "preview-only; future TMM adapter candidate"
    if application == "waveguide mode":
        return "mpb or elmer preview"
    if application in {"nanoparticle plasmonics", "dielectric metasurface"}:
        return "meep with gmsh geometry preview"
    return "adapter auto-selection preview"


def _design_goal_from_request(request: Any, application: str) -> str:
    if isinstance(request, dict):
        for key in ("design_goal", "text", "example_id"):
            value = request.get(key)
            if isinstance(value, str) and value.strip():
                return value
        spec = request.get("spec")
        if isinstance(spec, dict):
            value = spec.get("design_goal") or spec.get("application")
            if isinstance(value, str) and value.strip():
                return value
    return f"Local preview workflow for {application}."


def build_agent_trace(spec_or_request: Any) -> AgentTrace:
    """Build a deterministic local collaboration trace.

    This function intentionally does not call an external LLM, does not run a
    solver, and does not access the network. It is a preview trace for making
    Agent Studio collaboration visible.
    """

    text = _stringify_request(spec_or_request)
    application = _detect_application(text)
    material_suggestions = suggest_materials_for_application(application)
    material_names = ", ".join(item.material_id for item in material_suggestions)
    adapter = _adapter_for_application(application)
    design_goal = _design_goal_from_request(spec_or_request, application)
    example_id = spec_or_request.get("example_id") if isinstance(spec_or_request, dict) else None
    trace_hash = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]

    agents = [
        AgentStep(
            step_index=1,
            agent_name="SpecAgent",
            role="Interprets user intent / spec and identifies missing fields.",
            stage="spec_intake",
            input_summary=f"Request classified as {application}.",
            output_summary="Prepared a local preview intent summary for downstream agents.",
            diagnostics=["Spec interpretation is deterministic and local."],
            recommended_next_actions=["Review required wavelength, geometry, material, and output fields."],
            confidence="candidate",
            safety_notes=["No external LLM was called for this preview trace."],
        ),
        AgentStep(
            step_index=2,
            agent_name="MaterialAgent",
            role="Suggests materials from the local preview material catalog.",
            stage="material_selection",
            input_summary=f"Application: {application}.",
            output_summary=f"Suggested preview materials: {material_names}.",
            diagnostics=["Material constants are preview/design-assist values only."],
            recommended_next_actions=["Verify optical constants before physical conclusions."],
            confidence="preview",
            safety_notes=["Material suggestions are not production-grade optical constants."],
            evidence_refs=["docs/material_library.md"],
        ),
        AgentStep(
            step_index=3,
            agent_name="GeometryAgent",
            role="Identifies geometry family and required geometry fields.",
            stage="geometry_review",
            input_summary=f"Application: {application}.",
            output_summary="Mapped the request to a preview geometry family and noted missing dimensions if any.",
            diagnostics=["Geometry output is a scaffold until reviewed by the user."],
            recommended_next_actions=["Confirm geometry dimensions, units, and boundary conditions."],
            confidence="candidate",
            safety_notes=["Geometry remains a local preview scaffold."],
        ),
        AgentStep(
            step_index=4,
            agent_name="AdapterAgent",
            role="Recommends adapter/tool and explains maturity / limitations.",
            stage="adapter_recommendation",
            input_summary=f"Application and material hints: {application}; {material_names}.",
            output_summary=f"Recommended adapter path: {adapter}.",
            diagnostics=["Open-source-solver-first recommendation; no proprietary solver dependency."],
            recommended_next_actions=["Use adapter preview before any optional solver execution."],
            confidence="candidate",
            safety_notes=["No proprietary solver is required by default."],
            evidence_refs=["docs/adapter_support_matrix.md"],
        ),
        AgentStep(
            step_index=5,
            agent_name="WorkflowAgent",
            role="Creates local preview workflow plan and ensures no solver by default.",
            stage="workflow_planning",
            input_summary=f"Adapter path: {adapter}.",
            output_summary="Proposed parse -> validate -> adapter preview -> human review workflow.",
            diagnostics=["No solver execution is part of this trace."],
            recommended_next_actions=["Inspect workflow plan and preview artifact before any manual execution."],
            confidence="preview",
            safety_notes=["No solver is executed by default."],
        ),
        AgentStep(
            step_index=6,
            agent_name="EvidenceAgent",
            role="Attaches validation evidence / maturity and explains verified boundaries.",
            stage="evidence_review",
            input_summary=f"Adapter path: {adapter}.",
            output_summary="Attached adapter maturity and validation-evidence references where available.",
            diagnostics=["Evidence does not imply production-grade physical validation."],
            recommended_next_actions=["Review validation reports and scope limitations."],
            confidence="preview",
            safety_notes=["No production-grade physical validation is claimed."],
            evidence_refs=["docs/validation_evidence_manifest.md"],
        ),
        AgentStep(
            step_index=7,
            agent_name="SafetyAgent",
            role="Checks no overclaim and no default solver/LLM/publish/release actions.",
            stage="safety_review",
            input_summary="Collaboration trace safety boundary review.",
            output_summary="Safety flags remain false; no solver, LLM, upload, tag, or release action.",
            diagnostics=["Production-grade physical validation and formal convergence proof are not claimed."],
            recommended_next_actions=["Keep preview and validation boundaries visible in the UI."],
            confidence="validated",
            safety_notes=[
                "No PyPI/TestPyPI upload control.",
                "No GitHub tag/release control.",
                "Formal convergence proof is not claimed.",
            ],
            evidence_refs=["docs/frontend_safety_policy.md"],
        ),
        AgentStep(
            step_index=8,
            agent_name="RecommendationAgent",
            role="Proposes next actions.",
            stage="next_actions",
            input_summary=f"Trace for {application}.",
            output_summary="Next step: load the example, validate spec fields, inspect materials, and preview the adapter artifact.",
            diagnostics=["Recommendations are local workflow guidance only."],
            recommended_next_actions=[
                "Review material suggestions.",
                "Generate a workflow plan.",
                "Create an adapter preview without executing a solver.",
            ],
            confidence="preview",
            safety_notes=["Recommended next actions stay local and preview-first."],
        ),
    ]

    return AgentTrace(
        trace_id=f"trace-{trace_hash}",
        example_id=example_id if isinstance(example_id, str) else None,
        design_goal=design_goal,
        timeline_summary=(
            "Example Gallery -> Load example -> Material suggestions -> Adapter recommendation -> "
            "Agent trace timeline -> Workflow plan -> Artifact preview -> Evidence -> Next action"
        ),
        agents=agents,
        final_recommendation=(
            f"Use {material_names} as preview material candidates and follow {adapter}; "
            "verify material constants and validation evidence before physical conclusions."
        ),
        recommended_next_actions=[
            "Review material library warnings.",
            "Open Agent Collaboration in the frontend.",
            "Use /api/adapter-preview for local scaffold output.",
        ],
        material_suggestions=[item.material_id for item in material_suggestions],
        adapter_recommendation=adapter,
    )
