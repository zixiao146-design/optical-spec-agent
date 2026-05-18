"""Preview sub-agent collaboration trace for Agent Studio."""

from __future__ import annotations

import importlib

from .models import AgentStep, AgentTrace
from .orchestrator import build_agent_trace
from .roles import AGENT_ROLES

_LAZY_EXPORTS = {
    "AgentArtifact": "optical_spec_agent.agents.task_session",
    "AgentPlanStep": "optical_spec_agent.agents.task_session",
    "AgentTaskSession": "optical_spec_agent.agents.task_session",
    "PermissionGate": "optical_spec_agent.agents.task_session",
    "ToolCallRecord": "optical_spec_agent.agents.task_session",
    "build_agent_task_session": "optical_spec_agent.agents.task_session",
    "BackendCapabilityReport": "optical_spec_agent.agents.capability_report",
    "generate_backend_capability_report": "optical_spec_agent.agents.capability_report",
}


def __getattr__(name: str):
    """Lazily expose session/report helpers without import cycles."""

    module_name = _LAZY_EXPORTS.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    module = importlib.import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value

__all__ = [
    "AGENT_ROLES",
    "AgentArtifact",
    "AgentPlanStep",
    "AgentStep",
    "AgentTaskSession",
    "AgentTrace",
    "BackendCapabilityReport",
    "PermissionGate",
    "ToolCallRecord",
    "build_agent_task_session",
    "build_agent_trace",
    "generate_backend_capability_report",
]
