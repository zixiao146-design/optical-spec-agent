"""Tests for Pydantic models."""

import json

from optical_spec_agent.models.base import (
    GeometryDefinition,
    MaterialEntry,
    MaterialSystem,
    ParticleInfo,
    SourceSetting,
    SweepPlan,
    StatusField,
    ValidationStatus,
    confirmed,
    inferred,
    missing,
)
from optical_spec_agent.models.enums import (
    ModelDimension,
    SolverMethod,
    TaskType,
)
from optical_spec_agent.models.spec import OpticalSpec, TaskSection


class TestStatusField:
    def test_confirmed(self):
        sf = confirmed("fdtd")
        assert sf.value == "fdtd"
        assert sf.status == "confirmed"
        assert sf.note == ""

    def test_inferred_with_note(self):
        sf = inferred("3d", note="from structure type")
        assert sf.value == "3d"
        assert sf.status == "inferred"
        assert "structure" in sf.note

    def test_missing(self):
        sf = missing("not provided")
        assert sf.value is None
        assert sf.status == "missing"

    def test_validation_status(self):
        vs = ValidationStatus()
        assert vs.is_executable is False
        assert vs.errors == []


class TestStructuredModels:
    def test_geometry_definition(self):
        gd = GeometryDefinition(
            geometry_type="cube",
            dimensions={"edge_length": "80 nm"},
        )
        assert gd.geometry_type == "cube"
        assert gd.dimensions["edge_length"] == "80 nm"

    def test_material_system(self):
        ms = MaterialSystem(
            materials=[
                MaterialEntry(name="Au", role="particle"),
                MaterialEntry(name="SiO2", role="substrate"),
            ]
        )
        assert len(ms.materials) == 2
        assert ms.materials[0].name == "Au"

    def test_sweep_plan(self):
        sp = SweepPlan(
            sweep_type="wavelength",
            range_start=400.0,
            range_end=900.0,
            unit="nm",
        )
        assert sp.range_start == 400.0
        assert sp.sweep_type == "wavelength"

    def test_source_setting(self):
        ss = SourceSetting(
            source_type="tfsf",
            wavelength_range="400-900 nm",
        )
        assert ss.source_type == "tfsf"


class TestOpticalSpec:
    def test_default_spec_has_missing_fields(self):
        spec = OpticalSpec()
        missing_list = spec.collect_missing_fields()
        assert len(missing_list) > 0
        assert "task.task_name" in missing_list

    def test_collect_confirmed_inferred(self):
        spec = OpticalSpec()
        spec.task.task_type = inferred("simulation", "deduced from keywords")
        spec.task.task_name = confirmed("test task")
        c, i = spec.collect_confirmed_inferred()
        assert "task.task_name" in c
        assert c["task.task_name"] == "test task"
        assert "task.task_type" in i
        assert i["task.task_type"]["value"] == "simulation"

    def test_collect_assumptions(self):
        spec = OpticalSpec()
        spec.task.task_type = inferred("simulation", "deduced from keywords")
        assumptions = spec.collect_assumptions()
        assert len(assumptions) >= 1
        assert any("task.task_type" in a for a in assumptions)

    def test_to_flat_dict(self):
        spec = OpticalSpec()
        spec.task.task_id = "test-001"
        spec.task.task_type = confirmed("simulation")
        d = spec.to_flat_dict()
        assert "task" in d
        assert d["task"]["task_id"] == "test-001"
        assert d["task"]["task_type"]["value"] == "simulation"
        assert "confirmed_fields" in d
        assert "inferred_fields" in d

    def test_spec_round_trip_json(self):
        spec = OpticalSpec()
        spec.task.task_id = "rt-001"
        spec.task.task_name = confirmed("test task")
        d = spec.to_flat_dict()
        json_str = json.dumps(d, ensure_ascii=False)
        parsed = json.loads(json_str)
        assert parsed["task"]["task_name"]["value"] == "test task"

    def test_structured_value_in_flat_dict(self):
        spec = OpticalSpec()
        spec.geometry_material.geometry_definition = confirmed(
            GeometryDefinition(geometry_type="sphere", dimensions={"diameter": "100 nm"})
        )
        d = spec.to_flat_dict()
        geom = d["geometry_material"]["geometry_definition"]["value"]
        assert geom["geometry_type"] == "sphere"

    def test_export_json_schema(self):
        schema_str = OpticalSpec.export_json_schema()
        schema = json.loads(schema_str)
        assert "properties" in schema
        assert "task" in schema["properties"]

    def test_export_json_schema_dict(self):
        schema = OpticalSpec.export_json_schema_dict()
        assert isinstance(schema, dict)
        assert "properties" in schema
