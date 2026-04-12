"""Abstract parser interface — all parsers implement this."""

from __future__ import annotations

from abc import ABC, abstractmethod

from optical_spec_agent.models.spec import OpticalSpec


class BaseParser(ABC):
    """Pluggable parser interface.

    A parser takes raw natural language text and returns a partially (or fully)
    populated OpticalSpec.  The rule-based parser ships as the default; an
    LLM-based parser can be swapped in later.
    """

    @abstractmethod
    def parse(self, text: str, *, task_id: str = "") -> OpticalSpec:
        """Parse natural language *text* into an OpticalSpec."""
        ...
