"""Abstract adapter interface — all solver adapters implement this."""

from __future__ import annotations

from abc import ABC, abstractmethod

from pydantic import BaseModel, Field

from optical_spec_agent.models.spec import OpticalSpec


class AdapterMetadata(BaseModel):
    """Human- and machine-readable adapter capabilities."""

    tool_name: str = Field(description="Short tool key, e.g. 'meep' or 'gmsh'")
    display_name: str = Field(description="Human-readable adapter name")
    solver_family: str = Field(description="Solver family, e.g. FDTD, FEM, ray tracing")
    output_language: str = Field(description="Generated input language")
    output_extension: str = Field(description="Recommended output extension")
    supported_solver_methods: list[str] = Field(default_factory=list)
    supported_physical_systems: list[str] = Field(default_factory=list)
    current_status: str = Field(default="mvp", description="mvp, preview, or unsupported")
    limitations: list[str] = Field(default_factory=list)
    consumed_fields: list[str] = Field(default_factory=list)


class AdapterReadiness(BaseModel):
    """Adapter-level readiness check, distinct from general spec validation."""

    adapter_ready: bool = False
    errors: list[str] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    missing_required: list[str] = Field(default_factory=list)
    defaults_applied: list[str] = Field(default_factory=list)


class AdapterResult(BaseModel):
    """Output from a solver adapter: the generated solver input."""

    schema_version: str = Field(default="adapter_result.v0.1")
    tool: str = Field(description="Tool name, e.g. 'meep', 'mpb', 'elmer'")
    content: str = Field(description="Generated script or config file text")
    language: str = Field(
        description="Content language, e.g. 'python', 'scheme', 'sif'"
    )
    missing_required: list[str] = Field(
        default_factory=list,
        description="Spec fields this adapter needed but were missing",
    )
    metadata: dict = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    generated_files: dict[str, str] = Field(default_factory=dict)
    defaults_applied: list[str] = Field(default_factory=list)
    limitations: list[str] = Field(default_factory=list)


class BaseAdapter(ABC):
    """Pluggable solver adapter interface.

    An adapter takes a validated OpticalSpec and produces tool-native input
    (Python script, .sif file, .pro file, etc.).
    """

    tool_name: str = ""
    display_name: str = ""
    solver_family: str = ""
    output_language: str = ""
    output_extension: str = ""
    supported_solver_methods: list[str] = []
    supported_physical_systems: list[str] = []
    current_status: str = "mvp"
    limitations: list[str] = []
    _consumes: list[str] = []
    """Dotted paths in OpticalSpec this adapter primarily reads."""

    def metadata(self) -> AdapterMetadata:
        """Return static capability metadata for this adapter."""
        return AdapterMetadata(
            tool_name=self.tool_name,
            display_name=self.display_name or self.tool_name,
            solver_family=self.solver_family or "unknown",
            output_language=self.output_language or "text",
            output_extension=self.output_extension or ".txt",
            supported_solver_methods=list(self.supported_solver_methods),
            supported_physical_systems=list(self.supported_physical_systems),
            current_status=self.current_status,
            limitations=list(self.limitations),
            consumed_fields=list(self._consumes),
        )

    def validate_ready(self, spec: OpticalSpec, **kwargs) -> AdapterReadiness:
        """Default readiness: adapter can handle the spec with no additional checks."""
        if self.can_handle(spec):
            return AdapterReadiness(adapter_ready=True)
        return AdapterReadiness(
            adapter_ready=False,
            errors=[f"{self.tool_name} adapter cannot handle this spec"],
        )

    @abstractmethod
    def can_handle(self, spec: OpticalSpec) -> bool:
        """Return True if this adapter can process the given spec."""
        ...

    @abstractmethod
    def generate(self, spec: OpticalSpec) -> AdapterResult:
        """Convert spec into solver-native input. Must not run the solver."""
        ...
