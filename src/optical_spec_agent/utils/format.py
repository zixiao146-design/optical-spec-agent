"""Formatting helpers for human-readable output."""

from __future__ import annotations

import json
from typing import Any

from pydantic import BaseModel

from optical_spec_agent.models.spec import OpticalSpec


def spec_to_json(spec: OpticalSpec, *, indent: int = 2) -> str:
    """Serialize spec to a stable, pretty-printed JSON string."""
    return json.dumps(spec.to_flat_dict(), indent=indent, ensure_ascii=False, default=str)


def spec_to_summary(spec: OpticalSpec) -> str:
    """Build a human-readable summary string."""
    lines: list[str] = []
    lines.append("=" * 60)
    lines.append("  Optical Spec Agent — Summary")
    lines.append("=" * 60)

    # Task
    lines.append(f"\n  Task ID:    {spec.task.task_id}")
    lines.append(f"   Task Name:  {_v(spec.task.task_name)}")
    lines.append(f"   Task Type:  {_v(spec.task.task_type)}")
    lines.append(f"   Goal:       {_v(spec.task.research_goal, max_len=100)}")

    # Physics
    lines.append(f"\n  Physical System:  {_v(spec.physics.physical_system)}")
    lines.append(f"   Mechanism:        {_v(spec.physics.physical_mechanism)}")
    lines.append(f"   Dimension:        {_v(spec.physics.model_dimension)}")
    lines.append(f"   Structure:        {_v(spec.physics.structure_type)}")

    # Geometry & Material
    lines.append(f"\n  Geometry:         {_v(spec.geometry_material.geometry_definition, max_len=80)}")
    lines.append(f"   Materials:        {_v(spec.geometry_material.material_system, max_len=80)}")
    lines.append(f"   Material Model:   {_v(spec.geometry_material.material_model)}")
    lines.append(f"   Substrate/Film:   {_v(spec.geometry_material.substrate_or_film_info, max_len=60)}")
    lines.append(f"   Particle:         {_v(spec.geometry_material.particle_info, max_len=60)}")
    lines.append(f"   Gap Medium:       {_v(spec.geometry_material.gap_medium)}")
    lines.append(f"   Key Params:       {_v(spec.geometry_material.key_parameters)}")

    # Simulation
    lines.append(f"\n  Solver:           {_v(spec.simulation.solver_method)}")
    lines.append(f"   Software:         {_v(spec.simulation.software_tool)}")
    lines.append(f"   Sweep:            {_v(spec.simulation.sweep_plan, max_len=60)}")
    lines.append(f"   Source:           {_v(spec.simulation.excitation_source)}")
    lines.append(f"   Source Setting:   {_v(spec.simulation.source_setting, max_len=60)}")
    lines.append(f"   Polarization:     {_v(spec.simulation.polarization)}")
    lines.append(f"   Direction:        {_v(spec.simulation.incident_direction)}")
    lines.append(f"   Boundary:         {_v(spec.simulation.boundary_condition, max_len=60)}")
    lines.append(f"   Symmetry:         {_v(spec.simulation.symmetry_setting)}")
    lines.append(f"   Mesh:             {_v(spec.simulation.mesh_setting)}")
    lines.append(f"   Stability:        {_v(spec.simulation.stability_setting)}")
    lines.append(f"   Monitor:          {_v(spec.simulation.monitor_setting)}")

    # Output
    lines.append(f"\n  Observables:      {_v(spec.output.output_observables)}")
    lines.append(f"   Post-process:     {_v(spec.output.postprocess_target)}")

    # Confirmed / Inferred
    lines.append(f"\n  Confirmed ({len(spec.confirmed_fields)}):")
    for path, val in list(spec.confirmed_fields.items())[:8]:
        lines.append(f"     {path} = {_truncate(_val_str(val), 50)}")
    if len(spec.confirmed_fields) > 8:
        lines.append(f"     ... +{len(spec.confirmed_fields) - 8} more")

    lines.append(f"\n  Inferred ({len(spec.inferred_fields)}):")
    for path, info in list(spec.inferred_fields.items())[:8]:
        lines.append(f"     {path} = {_truncate(_val_str(info.get('value')), 50)}")
    if len(spec.inferred_fields) > 8:
        lines.append(f"     ... +{len(spec.inferred_fields) - 8} more")

    # System
    vs = spec.validation_status
    status_icon = "OK" if vs.is_executable else "NOT EXECUTABLE"
    lines.append(f"\n  [{status_icon}] Executable: {vs.is_executable}")
    if vs.errors:
        lines.append("   Errors:")
        for e in vs.errors:
            lines.append(f"     - {e}")
    if vs.warnings:
        lines.append("   Warnings:")
        for w in vs.warnings:
            lines.append(f"     - {w}")

    if spec.missing_fields:
        lines.append(f"\n  Missing Fields ({len(spec.missing_fields)}):")
        for mf in spec.missing_fields[:12]:
            lines.append(f"     - {mf}")
        if len(spec.missing_fields) > 12:
            lines.append(f"     ... +{len(spec.missing_fields) - 12} more")

    if spec.assumption_log:
        lines.append(f"\n  Assumptions ({len(spec.assumption_log)}):")
        for a in spec.assumption_log[:8]:
            lines.append(f"     - {a}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _v(sf: Any, max_len: int = 60) -> str:
    """Format a StatusField value for display."""
    from optical_spec_agent.models.base import StatusField

    if not isinstance(sf, StatusField):
        return str(sf)

    if sf.status == "missing":
        return "---"

    val = sf.value
    tag = {"confirmed": "[C]", "inferred": "[~]"}.get(sf.status, "[?]")
    text = _val_str(val)
    return f"{tag} {_truncate(text, max_len)}"


def _val_str(val: Any) -> str:
    """Convert any value to a short display string."""
    if val is None:
        return "None"
    if isinstance(val, BaseModel):
        # Show a compact version of Pydantic models
        d = val.model_dump()
        # Remove empty/default fields for brevity
        parts = []
        for k, v in d.items():
            if v and v != "" and v != [] and v != {} and v is not None:
                parts.append(f"{k}={_truncate(repr(v), 30)}")
        return ", ".join(parts) if parts else str(val)
    if isinstance(val, (list, dict)):
        text = json.dumps(val, ensure_ascii=False, default=str)
    else:
        text = str(val)
    return text


def _truncate(text: str, max_len: int) -> str:
    if text and len(text) > max_len:
        return text[: max_len - 3] + "..."
    return text
