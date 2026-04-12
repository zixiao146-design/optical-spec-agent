"""Placeholder LLM parser — returns a minimal spec with a TODO note.

This demonstrates the pluggable interface.  Replace the body with an actual
LLM call (e.g. Claude / GPT) when ready.
"""

from __future__ import annotations

from optical_spec_agent.models.base import StatusField, missing
from optical_spec_agent.models.spec import OpticalSpec

from optical_spec_agent.parsers.base import BaseParser


class LLMParser(BaseParser):
    """Stub LLM-based parser.  Always returns an empty spec with a warning."""

    def __init__(self, model_name: str = "placeholder") -> None:
        self.model_name = model_name

    def parse(self, text: str, *, task_id: str = "") -> OpticalSpec:
        import uuid
        if not task_id:
            task_id = uuid.uuid4().hex[:8]

        spec = OpticalSpec()
        spec.task.task_id = task_id
        spec.task.research_goal = StatusField(
            value=text[:200],
            status="confirmed",
            note="(LLM placeholder) 原文转发，未解析",
        )
        spec.assumption_log.append(
            f"LLM parser ({self.model_name}) not implemented — "
            "returning raw text as research_goal. "
            "Integrate a real LLM to populate the full spec."
        )
        spec.collect_missing_fields()
        return spec
