from __future__ import annotations

from optical_spec_agent.agents.orchestrator import build_agent_trace


def test_agent_trace_timeline_fields_and_recommendations():
    trace = build_agent_trace({"example_id": "nanoparticle_plasmonics"})
    assert trace.timeline_summary
    assert trace.final_recommendation
    assert trace.material_suggestions
    assert trace.adapter_recommendation

    agents = trace.agents
    assert [agent.step_index for agent in agents] == list(range(1, 9))
    names = [agent.agent_name for agent in agents]
    assert names == [
        "SpecAgent",
        "MaterialAgent",
        "GeometryAgent",
        "AdapterAgent",
        "WorkflowAgent",
        "EvidenceAgent",
        "SafetyAgent",
        "RecommendationAgent",
    ]
    for agent in agents:
        assert agent.stage
        assert agent.input_summary
        assert agent.output_summary
        assert agent.recommended_next_actions
        assert agent.safety_notes
    assert trace.external_solver_executed is False
    assert trace.external_llm_required is False
    assert trace.production_grade_validation_claimed is False
    assert trace.formal_convergence_proof_claimed is False
