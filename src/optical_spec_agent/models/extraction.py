"""Extraction record schema for the optics extraction workflow.

This module defines the data model for records produced by the
"web search → optical structure extraction" pipeline.
It is NOT connected to any MCP server or web crawler yet — it only
provides the schema that the future pipeline will populate.

See docs/optics_extraction_workflow.md for the full design.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, Field


class ExtractedSpec(BaseModel):
    """Structured optical spec fields extracted from a web page."""

    physical_system: Optional[str] = Field(
        None,
        description="Maps to PhysicalSystem enum: nanoparticle_on_film, waveguide, etc.",
    )
    structure_type: Optional[str] = Field(
        None,
        description="Maps to StructureType enum: sphere_on_film, cross_structure, etc.",
    )
    materials: list[str] = Field(
        default_factory=list,
        description="Material names: Au, Ag, SiO2, Si3N4, etc.",
    )
    physical_mechanism: Optional[str] = Field(
        None,
        description="Maps to PhysicalMechanism enum: gap_plasmon, scattering, etc.",
    )
    solver_hints: list[str] = Field(
        default_factory=list,
        description="Solver methods mentioned: fdtd, fem, rcwa, etc.",
    )
    output_observables: list[str] = Field(
        default_factory=list,
        description="Output types: scattering_spectrum, field_distribution, FWHM, etc.",
    )
    postprocess_target: list[str] = Field(
        default_factory=list,
        description="Post-processing targets: lorentzian_fit, fwhm_extraction, etc.",
    )


class ExtractionRecord(BaseModel):
    """A single record from the optics extraction pipeline."""

    query: str = Field(..., description="The search query that found this page")
    source_url: str = Field(..., description="Canonical URL of the source page")
    source_title: str = Field("", description="Page title")
    extraction_timestamp: str = Field(
        default_factory=lambda: datetime.utcnow().isoformat() + "Z",
        description="ISO 8601 timestamp",
    )
    task_text: str = Field(
        ..., description="Natural-language optical task description extracted from the page"
    )
    spec: ExtractedSpec = Field(
        default_factory=ExtractedSpec,
        description="Structured spec fields",
    )
    evidence_span: str = Field(
        ..., description="Exact text from source justifying the extraction"
    )
    confidence: str = Field(
        "medium",
        description="high | medium | low — extraction quality assessment",
    )
    notes: str = Field("", description="Free-text notes about extraction quality")
