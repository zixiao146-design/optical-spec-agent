"""Schema/API contract tests for v1.0 readiness."""

from __future__ import annotations

import json

from optical_spec_agent.models.base import SourceSetting, confirmed
from optical_spec_agent.models.spec import OpticalSpec
from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.validators.spec_validator import SpecValidator


def _minimal_executable_spec() -> OpticalSpec:
    spec = OpticalSpec()
    spec.task.task_type = confirmed("simulation")
    spec.task.research_goal = confirmed("contract smoke")
    spec.simulation.solver_method = confirmed("fdtd")
    spec.simulation.software_tool = confirmed("meep")
    spec.simulation.excitation_source = confirmed("plane_wave")
    spec.simulation.source_setting = confirmed(SourceSetting(source_type="plane_wave"))
    spec.simulation.boundary_condition = confirmed({"x_min": "PML"})
    spec.simulation.monitor_setting = confirmed({"monitor_type": "frequency_domain"})
    return spec


def test_schema_contains_documented_public_sections():
    schema = OpticalSpec.export_json_schema_dict()
    assert schema["type"] == "object"
    assert {
        "task",
        "physics",
        "geometry_material",
        "simulation",
        "output",
        "confirmed_fields",
        "inferred_fields",
        "missing_fields",
        "assumption_log",
        "validation_status",
    } <= set(schema["properties"])


def test_minimal_executable_spec_validation_contract():
    result = SpecValidator().validate(_minimal_executable_spec())
    assert result.validation_status.is_executable is True
    assert result.validation_status.errors == []


def test_invalid_empty_spec_has_deterministic_validation_errors():
    result = SpecValidator().validate(OpticalSpec())
    assert result.validation_status.is_executable is False
    assert "缺少必填字段: task.task_type" in result.validation_status.errors
    assert "缺少必填字段: task.research_goal" in result.validation_status.errors


def test_rule_parser_default_requires_no_external_llm():
    spec = SpecService().process("用 Meep FDTD 仿真金纳米球散射。", task_id="schema-contract")
    data = json.loads(spec.model_dump_json())
    assert data["task"]["task_id"] == "schema-contract"
    assert data["simulation"]["software_tool"]["value"] == "meep"
    assert data["simulation"]["solver_method"]["value"] == "fdtd"
