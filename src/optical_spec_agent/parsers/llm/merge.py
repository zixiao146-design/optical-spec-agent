"""Conservative merge helpers for hybrid parsing."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

from pydantic import BaseModel

from optical_spec_agent.models.base import MaterialEntry, MaterialSystem, StatusField
from optical_spec_agent.models.spec import OpticalSpec
from optical_spec_agent.parsers.llm.config import ParserReport


def merge_specs_conservatively(
    rule_spec: OpticalSpec,
    llm_spec: OpticalSpec,
    report: ParserReport,
) -> OpticalSpec:
    """Merge LLM candidate into rule baseline without overriding confirmed rules."""

    merged = deepcopy(rule_spec)
    for section_name in merged._SECTION_NAMES:
        section = getattr(merged, section_name)
        rule_section = getattr(rule_spec, section_name)
        llm_section = getattr(llm_spec, section_name)
        for field_name in type(section).model_fields:
            if field_name == "task_id":
                continue
            path = f"{section_name}.{field_name}"
            rule_field = getattr(rule_section, field_name)
            llm_field = getattr(llm_section, field_name)
            if not isinstance(rule_field, StatusField) or not isinstance(llm_field, StatusField):
                continue
            if llm_field.status == "missing" or llm_field.value in (None, "", [], {}):
                continue

            if rule_field.status == "missing" or rule_field.value in (None, "", [], {}):
                setattr(section, field_name, _llm_field_for_merge(llm_field))
                report.merged_fields.append(path)
                continue

            if path in {"output.output_observables", "output.postprocess_target"}:
                merged_value = _merge_lists(rule_field.value, llm_field.value)
                if merged_value != rule_field.value:
                    setattr(
                        section,
                        field_name,
                        StatusField(
                            value=merged_value,
                            status=rule_field.status,
                            note=f"{rule_field.note}; merged conservative LLM additions".strip("; "),
                        ),
                    )
                    report.merged_fields.append(path)
                continue

            if path == "geometry_material.material_system":
                merged_materials = _merge_material_system(rule_field.value, llm_field.value)
                if merged_materials is not None and _dump_value(merged_materials) != _dump_value(rule_field.value):
                    setattr(
                        section,
                        field_name,
                        StatusField(
                            value=merged_materials,
                            status=rule_field.status,
                            note=f"{rule_field.note}; merged conservative LLM material additions".strip("; "),
                        ),
                    )
                    report.merged_fields.append(path)
                continue

            if _dump_value(rule_field.value) != _dump_value(llm_field.value):
                conflict = {
                    "path": path,
                    "kept": _dump_value(rule_field.value),
                    "discarded_llm": _dump_value(llm_field.value),
                    "reason": "rule-based non-missing field wins by default",
                }
                report.conflicts.append(conflict)
                merged.assumption_log.append(
                    f"[conflict_preserved_rule] {path}: kept rule-based value over LLM candidate"
                )

    merged.assumption_log.append(
        f"[parser] hybrid merge completed with {len(report.conflicts)} conflict(s)"
    )
    merged.collect_all()
    return merged


def summarize_spec(spec: OpticalSpec) -> dict[str, Any]:
    """Small summary used in parser reports."""

    spec.collect_all()
    return {
        "confirmed_count": len(spec.confirmed_fields),
        "inferred_count": len(spec.inferred_fields),
        "missing_count": len(spec.missing_fields),
        "solver_method": _status_value(spec.simulation.solver_method),
        "software_tool": _status_value(spec.simulation.software_tool),
        "physical_system": _status_value(spec.physics.physical_system),
        "observables": _status_value(spec.output.output_observables),
    }


def _llm_field_for_merge(field: StatusField) -> StatusField:
    status = "confirmed" if field.status == "confirmed" else "inferred"
    note = field.note or "LLM parser supplied this field"
    if status == "confirmed":
        note = f"confirmed_llm_text_match: {note}"
    else:
        note = f"inferred_llm: {note}"
    return StatusField(value=field.value, status=status, note=note)


def _merge_lists(left: Any, right: Any) -> Any:
    if not isinstance(left, list) or not isinstance(right, list):
        return left
    merged = list(left)
    seen = {_stable_key(item) for item in merged}
    for item in right:
        key = _stable_key(item)
        if key not in seen:
            merged.append(item)
            seen.add(key)
    return merged


def _merge_material_system(left: Any, right: Any) -> Any | None:
    left_model = _as_material_system(left)
    right_model = _as_material_system(right)
    if left_model is None or right_model is None:
        return None
    materials = list(left_model.materials)
    seen = {item.name for item in materials}
    for material in right_model.materials:
        if material.name not in seen:
            materials.append(material)
            seen.add(material.name)
    return MaterialSystem(materials=materials, description=left_model.description or right_model.description)


def _as_material_system(value: Any) -> MaterialSystem | None:
    if isinstance(value, MaterialSystem):
        return value
    if isinstance(value, dict):
        try:
            return MaterialSystem.model_validate(value)
        except Exception:
            return None
    if isinstance(value, list):
        try:
            return MaterialSystem(materials=[MaterialEntry.model_validate(item) for item in value])
        except Exception:
            return None
    return None


def _dump_value(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump()
    if isinstance(value, list):
        return [_dump_value(item) for item in value]
    if isinstance(value, dict):
        return {key: _dump_value(val) for key, val in value.items()}
    return value


def _stable_key(value: Any) -> str:
    return str(_dump_value(value))


def _status_value(field: Any) -> Any:
    if isinstance(field, StatusField):
        return field.value
    return None
