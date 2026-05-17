# Sub-agent Architecture

Agent Studio now exposes a deterministic local sub-agent collaboration trace.
The trace makes the agent workflow visible without introducing autonomous
external agents, external LLM calls, solver execution, uploads, tags, or
releases.

Current roles:
- SpecAgent: interprets user intent or an OpticalSpec and identifies missing fields.
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
- Each step includes diagnostics, recommended next actions, confidence, and evidence refs.

Safety:
- No external LLM is called by default.
- No external solver is executed by default.
- No network access is required.
- No production-grade physical validation is claimed.
- Formal convergence proof is not claimed.

Frontend visualization:
- Agent Studio exposes an Agent Collaboration page.
- The page renders each sub-agent as a card/timeline item.
- The page keeps preview and validation boundaries visible.
