"""Tests for the spec service (parse + validate integration)."""

from optical_spec_agent.services.spec_service import SpecService


class TestSpecService:
    def test_process_returns_spec(self):
        svc = SpecService()
        text = (
            "用FDTD仿真金纳米球Mie散射，直径100nm，波长400-800nm，"
            "计算散射截面，正入射平面波。"
        )
        spec = svc.process(text, task_id="svc-test-01")
        assert spec.task.task_id == "svc-test-01"
        assert len(spec.confirmed_fields) > 0
        assert len(spec.missing_fields) > 0

    def test_process_to_dict(self):
        svc = SpecService()
        d = svc.process_to_dict("COMSOL有限元分析脊波导模式")
        assert isinstance(d, dict)
        assert "task" in d
        assert "confirmed_fields" in d
        assert "inferred_fields" in d
        assert "validation_status" in d
