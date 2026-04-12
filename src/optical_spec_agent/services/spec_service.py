"""High-level service: parse -> validate -> format."""

from __future__ import annotations

from typing import Any

from optical_spec_agent.models.spec import OpticalSpec
from optical_spec_agent.parsers.base import BaseParser
from optical_spec_agent.parsers.rule_based import RuleBasedParser
from optical_spec_agent.validators.spec_validator import SpecValidator


class SpecService:
    """Orchestrates parsing and validation.

    This is the main entry-point for both CLI and API usage.
    """

    def __init__(self, parser: BaseParser | None = None) -> None:
        self.parser = parser or RuleBasedParser()
        self.validator = SpecValidator()

    def process(self, text: str, *, task_id: str = "") -> OpticalSpec:
        """Parse natural language -> validate -> return enriched spec."""
        spec = self.parser.parse(text, task_id=task_id)
        spec = self.validator.validate(spec)
        return spec

    def process_to_dict(self, text: str, *, task_id: str = "") -> dict[str, Any]:
        """Convenience: returns the flat dict representation."""
        spec = self.process(text, task_id=task_id)
        return spec.to_flat_dict()
