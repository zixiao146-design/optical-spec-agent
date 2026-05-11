"""Tests for parser registry."""

import pytest

from optical_spec_agent.parsers import HybridParser, LLMParser, RuleBasedParser, get_parser
from optical_spec_agent.parsers.registry import ParserRegistryError


def test_get_parser_rule_aliases():
    assert isinstance(get_parser("rule"), RuleBasedParser)
    assert isinstance(get_parser("rules"), RuleBasedParser)
    assert isinstance(get_parser("rule_based"), RuleBasedParser)


def test_get_parser_llm_and_hybrid():
    assert isinstance(get_parser("llm"), LLMParser)
    assert isinstance(get_parser("hybrid"), HybridParser)


def test_unknown_parser_errors():
    with pytest.raises(ParserRegistryError, match="Unknown parser"):
        get_parser("magic")
