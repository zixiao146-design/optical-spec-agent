"""Models for local preview sub-agent collaboration traces."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AgentStep(BaseModel):
    agent_name: str
    role: str
    input_summary: str
    output_summary: str
    diagnostics: list[str] = Field(default_factory=list)
    recommended_next_actions: list[str] = Field(default_factory=list)
    confidence: str = "preview"
    evidence_refs: list[str] = Field(default_factory=list)


class AgentTrace(BaseModel):
    trace_id: str
    status: str = "ok"
    agents: list[AgentStep] = Field(default_factory=list)
    final_recommendation: str
    recommended_next_actions: list[str] = Field(default_factory=list)
    external_solver_executed: bool = False
    external_llm_required: bool = False
    proprietary_solver_required: bool = False
    production_grade_validation_claimed: bool = False
    formal_convergence_proof_claimed: bool = False
