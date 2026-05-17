from optical_spec_agent.agents.orchestrator import build_agent_trace


def test_build_agent_trace_returns_all_sub_agents_and_safety_flags():
    trace = build_agent_trace({"text": "nanoparticle plasmonics with silver particle"})
    names = [agent.agent_name for agent in trace.agents]
    for name in [
        "SpecAgent",
        "MaterialAgent",
        "GeometryAgent",
        "AdapterAgent",
        "WorkflowAgent",
        "EvidenceAgent",
        "SafetyAgent",
        "RecommendationAgent",
    ]:
        assert name in names
    material_step = next(agent for agent in trace.agents if agent.agent_name == "MaterialAgent")
    adapter_step = next(agent for agent in trace.agents if agent.agent_name == "AdapterAgent")
    safety_step = next(agent for agent in trace.agents if agent.agent_name == "SafetyAgent")
    assert "au" in material_step.output_summary or "ag" in material_step.output_summary
    assert "meep" in adapter_step.output_summary.lower()
    assert "No solver" in safety_step.output_summary or "no solver" in safety_step.output_summary
    assert trace.external_solver_executed is False
    assert trace.external_llm_required is False
    assert trace.production_grade_validation_claimed is False
    assert trace.formal_convergence_proof_claimed is False
