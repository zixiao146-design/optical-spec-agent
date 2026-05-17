"""Local registry for optical design examples."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from optical_spec_agent.agents.models import AgentTrace
from optical_spec_agent.agents.orchestrator import build_agent_trace

from .models import OpticalDesignExampleDetail, OpticalDesignExampleSummary


REPO_ROOT = Path(__file__).resolve().parents[3]
EXAMPLES_ROOT = REPO_ROOT / "examples" / "optical_design"

EXAMPLE_METADATA: dict[str, dict[str, Any]] = {
    "nanoparticle_plasmonics": {
        "title": "Nanoparticle Plasmonics Preview",
        "title_zh": "纳米颗粒等离激元预览",
        "design_goal_zh": "预览一个本地纳米颗粒散射工作流。",
        "category": "plasmonics",
        "physical_system": "nanoparticle_on_film",
        "maturity_note": "Meep/Gmsh preview path; material constants must be verified.",
    },
    "thin_film_coating": {
        "title": "Thin Film Coating Preview",
        "title_zh": "薄膜镀膜预览",
        "design_goal_zh": "预览一个薄膜叠层设计工作流，不新增求解器依赖。",
        "category": "coating",
        "physical_system": "thin_film_stack",
        "maturity_note": "Preview-only; future TMM adapter candidate.",
    },
    "waveguide_mode": {
        "title": "Waveguide Mode Preview",
        "title_zh": "波导模式预览",
        "design_goal_zh": "预览波导模式设置和本地设计审阅流程。",
        "category": "waveguide",
        "physical_system": "waveguide",
        "maturity_note": "MPB preview path; Elmer remains Level 2 + Level-3-ready, install deferred.",
    },
    "photonic_crystal_band": {
        "title": "Photonic Crystal Band Preview",
        "title_zh": "光子晶体能带预览",
        "design_goal_zh": "预览 MPB 风格的光子晶体能带工作流。",
        "category": "photonic_crystal",
        "physical_system": "photonic_crystal",
        "maturity_note": "MPB preview path; no formal convergence proof claimed.",
    },
    "dielectric_metasurface_preview": {
        "title": "Dielectric Metasurface Preview",
        "title_zh": "介质超表面预览",
        "design_goal_zh": "预览介质超表面本地工作流。",
        "category": "metasurface",
        "physical_system": "metasurface",
        "maturity_note": "Meep/Gmsh preview path; geometry remains scaffold until reviewed.",
    },
    "lens_raytrace_preview": {
        "title": "Lens Raytrace Preview",
        "title_zh": "透镜光线追迹预览",
        "design_goal_zh": "预览 Optiland 方向的本地透镜/光线光学工作流。",
        "category": "ray_optics",
        "physical_system": "lens",
        "maturity_note": "Optiland scaffold; glass catalog data must be verified.",
    },
}

SAFETY_BOUNDARIES = [
    "No solver is executed by default.",
    "No external LLM is called by default.",
    "Preview artifacts are not production-grade physical validation.",
    "Formal convergence proof is not claimed.",
]


class ExampleRegistryError(ValueError):
    """Raised for missing or malformed local examples."""


def list_optical_design_examples() -> list[OpticalDesignExampleSummary]:
    """List local optical design examples from examples/optical_design."""

    return [
        _load_summary(example_id)
        for example_id in sorted(EXAMPLE_METADATA)
    ]


def get_optical_design_example(example_id: str) -> OpticalDesignExampleDetail:
    """Load one local optical design example."""

    summary = _load_summary(example_id)
    example_dir = _example_dir(example_id)
    spec = _load_json(example_dir / "spec.json")
    expected_agent_trace = _load_json(example_dir / "expected_agent_trace.json")
    return OpticalDesignExampleDetail(
        summary=summary,
        spec=spec,
        expected_agent_trace=expected_agent_trace,
        recommended_next_actions=[
            "Load this example into Agent Studio.",
            "Review material suggestions and adapter recommendation.",
            "Generate the agent trace timeline before workflow planning.",
            "Keep preview and validation boundaries visible.",
        ],
        safety_boundaries=SAFETY_BOUNDARIES,
    )


def build_example_agent_trace(example_id: str) -> AgentTrace:
    """Build a local deterministic agent trace for a bundled example."""

    detail = get_optical_design_example(example_id)
    trace = build_agent_trace(
        {
            "example_id": example_id,
            "spec": detail.spec,
            "design_goal": detail.summary.design_goal,
            "application": detail.spec.get("application"),
            "suggested_adapter": detail.summary.suggested_adapter,
        }
    )
    trace.example_id = example_id
    trace.design_goal = detail.summary.design_goal
    trace.timeline_summary = (
        "Example Gallery -> Material suggestions -> Adapter recommendation -> "
        "Agent trace timeline -> Workflow plan -> Artifact preview -> Evidence -> Next action"
    )
    return trace


def _load_summary(example_id: str) -> OpticalDesignExampleSummary:
    metadata = EXAMPLE_METADATA.get(example_id)
    if metadata is None:
        raise ExampleRegistryError(f"Unknown optical design example: {example_id}")
    example_dir = _example_dir(example_id)
    spec = _load_json(example_dir / "spec.json")
    _ensure_file(example_dir / "README.md")
    _ensure_file(example_dir / "expected_agent_trace.json")
    return OpticalDesignExampleSummary(
        example_id=example_id,
        title=metadata["title"],
        title_zh=metadata["title_zh"],
        design_goal=str(spec.get("design_goal", "")),
        design_goal_zh=metadata["design_goal_zh"],
        category=metadata["category"],
        suggested_materials=list(spec.get("suggested_materials", [])),
        suggested_adapter=str(spec.get("suggested_adapter", "")),
        physical_system=metadata["physical_system"],
        workflow_focus=list(spec.get("workflow_steps", [])),
        maturity_note=metadata["maturity_note"],
        spec_path=f"examples/optical_design/{example_id}/spec.json",
        has_agent_trace=(example_dir / "expected_agent_trace.json").exists(),
    )


def _example_dir(example_id: str) -> Path:
    if "/" in example_id or "\\" in example_id or ".." in example_id:
        raise ExampleRegistryError(f"Invalid example id: {example_id}")
    example_dir = EXAMPLES_ROOT / example_id
    if not example_dir.is_dir():
        raise ExampleRegistryError(f"Unknown optical design example: {example_id}")
    return example_dir


def _load_json(path: Path) -> dict[str, Any]:
    _ensure_file(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ExampleRegistryError(f"Malformed example JSON: {path}") from exc
    if not isinstance(payload, dict):
        raise ExampleRegistryError(f"Example JSON must be an object: {path}")
    return payload


def _ensure_file(path: Path) -> None:
    if not path.exists():
        raise ExampleRegistryError(f"Required example file missing: {path}")
