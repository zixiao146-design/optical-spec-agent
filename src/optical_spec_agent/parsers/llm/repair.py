"""JSON extraction, repair, and OpticalSpec normalization helpers."""

from __future__ import annotations

import json
import re
from typing import Any

from pydantic import ValidationError

from optical_spec_agent.models.base import StatusField, missing
from optical_spec_agent.models.spec import OpticalSpec


class LLMJSONError(ValueError):
    """Raised when an LLM response cannot be converted into OpticalSpec JSON."""


_NORMALIZE_VALUES = {
    "FDTD": "fdtd",
    "fdtd": "fdtd",
    "finite element": "fem",
    "finite_element": "fem",
    "FEM": "fem",
    "fem": "fem",
    "band diagram": "band_structure",
    "band structure": "band_structure",
    "ray tracing": "ray_trace",
    "raytracing": "ray_trace",
    "ray trace": "ray_trace",
    "mode solver": "mode_solver",
}


def repair_common_json_issues(text: str) -> str:
    """Repair common non-semantic JSON formatting issues."""

    repaired = text.strip()
    repaired = _strip_markdown_fence(repaired)
    repaired = _slice_first_json_object(repaired)
    repaired = re.sub(r",\s*([}\]])", r"\1", repaired)
    return repaired


def extract_json_object(text: str) -> dict[str, Any]:
    """Extract and parse the first JSON object from an LLM response."""

    repaired = repair_common_json_issues(text)
    try:
        parsed = json.loads(repaired)
    except json.JSONDecodeError as exc:
        raise LLMJSONError(f"Could not parse LLM JSON: {exc}") from exc
    if not isinstance(parsed, dict):
        raise LLMJSONError("LLM response must contain a JSON object")
    return parsed


def normalize_llm_spec_dict(data: dict[str, Any]) -> dict[str, Any]:
    """Normalize enum-ish strings and ensure top-level sections exist."""

    normalized = dict(data)
    for section in ("task", "physics", "geometry_material", "simulation", "output"):
        normalized.setdefault(section, {})
    _normalize_status_values(normalized)
    return normalized


def llm_dict_to_optical_spec(data: dict[str, Any], *, task_id: str = "") -> OpticalSpec:
    """Convert normalized LLM JSON into an OpticalSpec."""

    normalized = normalize_llm_spec_dict(data)
    if task_id:
        normalized.setdefault("task", {})["task_id"] = task_id
    try:
        spec = OpticalSpec.model_validate(normalized)
    except ValidationError as exc:
        raise LLMJSONError(f"LLM JSON did not match OpticalSpec schema: {exc}") from exc
    _ensure_status_fields(spec)
    if task_id and not spec.task.task_id:
        spec.task.task_id = task_id
    spec.collect_all()
    return spec


def _strip_markdown_fence(text: str) -> str:
    match = re.search(r"```(?:json)?\s*(.*?)```", text, re.DOTALL | re.IGNORECASE)
    return match.group(1).strip() if match else text


def _slice_first_json_object(text: str) -> str:
    start = text.find("{")
    if start < 0:
        return text
    depth = 0
    in_string = False
    escape = False
    for idx in range(start, len(text)):
        char = text[idx]
        if in_string:
            if escape:
                escape = False
            elif char == "\\":
                escape = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : idx + 1]
    return text[start:]


def _normalize_status_values(node: Any) -> None:
    if isinstance(node, dict):
        if set(node.keys()) >= {"value", "status"} and isinstance(node.get("value"), str):
            node["value"] = _NORMALIZE_VALUES.get(node["value"], node["value"])
        for value in node.values():
            _normalize_status_values(value)
    elif isinstance(node, list):
        for item in node:
            _normalize_status_values(item)


def _ensure_status_fields(spec: OpticalSpec) -> None:
    for section_name in spec._SECTION_NAMES:
        section = getattr(spec, section_name)
        for field_name in type(section).model_fields:
            if field_name == "task_id":
                continue
            value = getattr(section, field_name)
            if not isinstance(value, StatusField):
                setattr(section, field_name, missing())
