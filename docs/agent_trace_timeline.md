# Agent Trace Timeline

The Agent Trace Timeline makes local sub-agent collaboration visible in Agent Studio.

API:
- `POST /api/agent-trace`
- `POST /api/examples/{example_id}/agent-trace`

Timeline roles:
- SpecAgent: interprets intent and missing fields.
- MaterialAgent: suggests preview materials from the local material catalog.
- GeometryAgent: identifies geometry family and required geometry fields.
- AdapterAgent: recommends an open-source-first adapter path.
- WorkflowAgent: proposes a local no-execute workflow.
- EvidenceAgent: attaches validation evidence and maturity notes.
- SafetyAgent: checks no overclaim, no solver, no LLM, no upload, no tag, and no release actions.
- RecommendationAgent: proposes next actions.

Each timeline step exposes:
- step_index
- stage
- input_summary
- output_summary
- diagnostics
- evidence_refs
- recommended_next_actions
- safety_notes

The timeline is a deterministic local preview. No external LLM is called by default, no solver is executed by default, and the timeline does not claim production-grade physical validation or formal convergence proof.

Agent Command Center builds on this trace through `POST /api/agent-session`.
The command-center session adds natural language goal handling, optical intent
summary, selected design case, task plan steps, artifacts, permission gates,
and next actions around the same sub-agent collaboration timeline.
