"""Abstract adapter interface — all solver adapters implement this."""

from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from optical_spec_agent.models.spec import OpticalSpec


class AdapterResult(BaseModel):
    """Output from a solver adapter: the generated solver input."""

    tool: str = Field(description="Tool name, e.g. 'meep', 'mpb', 'elmer'")
    content: str = Field(description="Generated script or config file text")
    language: str = Field(
        description="Content language, e.g. 'python', 'scheme', 'sif'"
    )
    missing_required: list[str] = Field(
        default_factory=list,
        description="Spec fields this adapter needed but were missing",
    )


class BaseAdapter(ABC):
    """Pluggable solver adapter interface.

    An adapter takes a validated OpticalSpec and produces tool-native input
    (Python script, .sif file, .pro file, etc.).
    """

    tool_name: str = ""
    _consumes: list[str] = []
    """Dotted paths in OpticalSpec this adapter primarily reads."""

    @abstractmethod
    def can_handle(self, spec: OpticalSpec) -> bool:
        """Return True if this adapter can process the given spec."""
        ...

    @abstractmethod
    def generate(self, spec: OpticalSpec) -> AdapterResult:
        """Convert spec into solver-native input. Must not run the solver."""
        ...
