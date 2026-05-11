"""Tests for conservative hybrid parser behavior."""

from optical_spec_agent.models.base import StatusField, confirmed, missing
from optical_spec_agent.models.spec import OpticalSpec
from optical_spec_agent.parsers.llm import HybridParser, LLMParserConfig, ParserReport
from optical_spec_agent.parsers.llm.merge import merge_specs_conservatively


def test_hybrid_parser_uses_mock_and_logs_report():
    parser = HybridParser(config=LLMParserConfig(provider="mock"))
    spec = parser.parse("Use MPB to compute a photonic crystal band diagram.")
    assert spec.simulation.software_tool.value == "mpb"
    assert parser.last_report.parser_mode == "hybrid"


def test_llm_fills_rule_missing_field():
    rule_spec = OpticalSpec()
    rule_spec.task.task_id = "merge"
    rule_spec.task.task_type = confirmed("simulation")
    llm_spec = OpticalSpec()
    llm_spec.task.task_id = "merge"
    llm_spec.task.task_type = confirmed("simulation")
    llm_spec.simulation.software_tool = StatusField(
        value="mpb",
        status="confirmed",
        note="text says MPB",
    )
    report = ParserReport(parser_mode="hybrid")
    merged = merge_specs_conservatively(rule_spec, llm_spec, report)
    assert merged.simulation.software_tool.value == "mpb"
    assert merged.simulation.software_tool.status == "confirmed"
    assert "simulation.software_tool" in report.merged_fields


def test_rule_confirmed_field_wins_conflict():
    rule_spec = OpticalSpec()
    rule_spec.simulation.software_tool = confirmed("meep", "rule saw Meep")
    llm_spec = OpticalSpec()
    llm_spec.simulation.software_tool = confirmed("mpb", "LLM suggested MPB")
    report = ParserReport(parser_mode="hybrid")
    merged = merge_specs_conservatively(rule_spec, llm_spec, report)
    assert merged.simulation.software_tool.value == "meep"
    assert report.conflicts


def test_observables_merge_without_duplicates():
    rule_spec = OpticalSpec()
    rule_spec.output.output_observables = confirmed(["scattering_spectrum"])
    llm_spec = OpticalSpec()
    llm_spec.output.output_observables = confirmed(["scattering_spectrum", "absorption_spectrum"])
    report = ParserReport(parser_mode="hybrid")
    merged = merge_specs_conservatively(rule_spec, llm_spec, report)
    assert merged.output.output_observables.value == ["scattering_spectrum", "absorption_spectrum"]


def test_missing_llm_field_does_not_override():
    rule_spec = OpticalSpec()
    rule_spec.simulation.software_tool = confirmed("meep")
    llm_spec = OpticalSpec()
    llm_spec.simulation.software_tool = missing()
    report = ParserReport(parser_mode="hybrid")
    merged = merge_specs_conservatively(rule_spec, llm_spec, report)
    assert merged.simulation.software_tool.value == "meep"
