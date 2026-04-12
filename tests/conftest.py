"""Shared fixtures for tests."""

import pytest

from optical_spec_agent.services.spec_service import SpecService
from optical_spec_agent.parsers.rule_based import RuleBasedParser
from optical_spec_agent.parsers.llm_placeholder import LLMParser


@pytest.fixture
def svc() -> SpecService:
    return SpecService()


@pytest.fixture
def rule_parser() -> RuleBasedParser:
    return RuleBasedParser()


@pytest.fixture
def llm_parser() -> LLMParser:
    return LLMParser()
