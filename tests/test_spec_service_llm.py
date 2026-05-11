"""Tests for SpecService parser selection."""

from optical_spec_agent.parsers.llm import LLMParserConfig, MockLLMClient
from optical_spec_agent.services.spec_service import SpecService


def test_default_spec_service_remains_rule_based():
    svc = SpecService()
    spec = svc.process("用 Meep FDTD 仿真金纳米球散射。")
    assert spec.simulation.software_tool.value == "meep"
    assert svc.last_parser_report is None


def test_spec_service_llm_mock():
    svc = SpecService(
        parser="llm",
        llm_config=LLMParserConfig(provider="mock"),
        llm_client=MockLLMClient(),
    )
    spec = svc.process("Use MPB to compute a photonic crystal band diagram.")
    assert spec.simulation.software_tool.value == "mpb"
    assert svc.last_parser_report is not None


def test_spec_service_hybrid_mock_validation_runs():
    svc = SpecService(parser="hybrid", llm_config=LLMParserConfig(provider="mock"))
    spec = svc.process("用 Optiland 计算 spot diagram 和 MTF。")
    assert spec.simulation.software_tool.value == "optiland"
    assert spec.validation_status.errors


def test_process_can_override_parser_per_call():
    svc = SpecService()
    spec = svc.process(
        "Use Gmsh to mesh a waveguide cross-section.",
        parser="hybrid",
        llm_config=LLMParserConfig(provider="mock"),
    )
    assert spec.simulation.software_tool.value == "gmsh"
    assert svc.last_parser_report is not None
