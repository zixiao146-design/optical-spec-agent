"""Tests for LLM JSON extraction and repair."""

import pytest

from optical_spec_agent.parsers.llm import LLMJSONError, extract_json_object, llm_dict_to_optical_spec


def test_extract_clean_json():
    assert extract_json_object('{"task": {"task_type": {"value": "simulation", "status": "confirmed"}}}')["task"]


def test_extract_fenced_json():
    data = extract_json_object('```json\n{"task": {"task_type": {"value": "simulation", "status": "confirmed"}}}\n```')
    assert data["task"]["task_type"]["value"] == "simulation"


def test_extract_prose_wrapped_json():
    data = extract_json_object('Here:\n{"simulation": {"solver_method": {"value": "FDTD", "status": "confirmed"}}}\nDone')
    spec = llm_dict_to_optical_spec(data)
    assert spec.simulation.solver_method.value == "fdtd"


def test_repair_trailing_comma():
    data = extract_json_object('{"task": {"task_type": {"value": "simulation", "status": "confirmed"}},}')
    assert data["task"]["task_type"]["value"] == "simulation"


def test_irreparable_json_raises():
    with pytest.raises(LLMJSONError):
        extract_json_object("not json")
