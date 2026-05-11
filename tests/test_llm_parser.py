"""Tests for LLMParser with deterministic mock provider."""

import pytest

from optical_spec_agent.parsers.llm import LLMParser, LLMParserConfig, LLMParserError


def test_llm_parser_mock_produces_spec():
    parser = LLMParser(config=LLMParserConfig(provider="mock"))
    spec = parser.parse("Use Meep FDTD to simulate Au sphere scattering.")
    assert spec.simulation.software_tool.value == "meep"
    assert parser.last_report.provider == "mock"


def test_llm_parser_repairs_malformed_json():
    parser = LLMParser(config=LLMParserConfig(provider="mock"))
    spec = parser.parse("MOCK_MALFORMED Use Meep FDTD.")
    assert spec.simulation.solver_method.value == "fdtd"
    assert parser.last_report.repair_used is True


def test_llm_parser_fallback_to_rule_when_irreparable():
    parser = LLMParser(config=LLMParserConfig(provider="mock", fallback_to_rule_based=True))
    spec = parser.parse("MOCK_IRREPARABLE 用 Meep FDTD 仿真金纳米球散射。")
    assert spec.simulation.software_tool.value == "meep"
    assert parser.last_report.fallback_used is True
    assert any("fallback_rule" in item for item in spec.assumption_log)


def test_llm_parser_no_fallback_raises():
    parser = LLMParser(config=LLMParserConfig(provider="mock", fallback_to_rule_based=False))
    with pytest.raises(LLMParserError):
        parser.parse("MOCK_IRREPARABLE Use Meep FDTD.")


def test_oversized_input_records_warning():
    parser = LLMParser(config=LLMParserConfig(provider="mock", max_input_chars=10))
    parser.parse("Use Meep FDTD to simulate a long optical request.")
    assert parser.last_report.warnings
