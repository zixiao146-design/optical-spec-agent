"""Models for local optical design examples."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ExampleSafety(BaseModel):
    external_solver_executed: bool = False
    external_llm_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False


class OpticalDesignExampleSummary(BaseModel):
    example_id: str
    title: str
    title_zh: str
    design_goal: str
    design_goal_zh: str
    category: str
    suggested_materials: list[str] = Field(default_factory=list)
    suggested_adapter: str
    physical_system: str
    workflow_focus: list[str] = Field(default_factory=list)
    maturity_note: str
    spec_path: str
    has_agent_trace: bool = True
    safety: ExampleSafety = Field(default_factory=ExampleSafety)


class OpticalDesignExampleDetail(BaseModel):
    summary: OpticalDesignExampleSummary
    spec: dict[str, Any]
    expected_agent_trace: dict[str, Any]
    recommended_next_actions: list[str] = Field(default_factory=list)
    safety_boundaries: list[str] = Field(default_factory=list)
