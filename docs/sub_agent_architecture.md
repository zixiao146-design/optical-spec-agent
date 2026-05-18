# Sub-agent Architecture

Agent Studio now exposes a deterministic local sub-agent collaboration trace.
The trace makes the agent workflow visible without introducing autonomous
external agents, external LLM calls, solver execution, uploads, tags, or
releases.

Current roles:
- SpecAgent: interprets user intent or an OpticalSpec, runs
  `requirements.match_template` / `requirements.extract_optical_intent`, and
  identifies missing fields.
- MaterialAgent: suggests materials from the local preview material catalog.
- GeometryAgent: identifies geometry family and required geometry fields.
- AdapterAgent: recommends an open-source-first adapter/tool and explains limitations.
- WorkflowAgent: creates a local preview workflow plan with no solver execution by default.
- EvidenceAgent: attaches validation evidence and maturity notes.
- SafetyAgent: checks no overclaim, no default solver/LLM, and no publication controls.
- RecommendationAgent: summarizes next actions.

Input/output:
- Input may be local text, a spec-like JSON object, or a local example ID.
- Output is an AgentTrace with AgentStep entries and a final recommendation.
- Each step includes `step_index`, `stage`, input summary, output summary,
  diagnostics, recommended next actions, confidence, status, safety notes, and
  evidence refs.
- Example-specific traces are available through
  `POST /api/examples/{example_id}/agent-trace`.

Safety:
- No external LLM is called by default.
- No external solver is executed by default.
- No network access is required.
- No production-grade physical validation is claimed.
- Formal convergence proof is not claimed.

Frontend visualization:
- Agent Studio exposes an Agent Collaboration page.
- The page renders each sub-agent as an Agent Trace Timeline item.
- The Example Gallery can generate a trace for bundled optical design examples.
- The page keeps preview and validation boundaries visible.

Agent Command Center:
- `POST /api/agent-session` wraps the same sub-agent roles into a task-level
  session for a natural language goal.
- The session adds optical intent, selected design case, plan steps, local
  artifacts, permission gates, a tool-call ledger, final recommendation, and
  next actions.
- Permission gates keep external solver, external LLM, upload, PyPI
  publication, tag, and release actions blocked by default.
- `scripts/audit_sub_agents.py` reports the current reality honestly:
  sub-agents are deterministic trace roles with callable backend functions, not
  standalone importable autonomous classes.
