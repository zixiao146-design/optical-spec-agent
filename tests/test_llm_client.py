"""Tests for deterministic LLM client abstractions."""

import pytest

from optical_spec_agent.parsers.llm import (
    LLMParserConfig,
    LLMProviderError,
    MockLLMClient,
    build_llm_prompt,
    make_llm_client,
)


def test_mock_llm_client_is_deterministic():
    config = LLMParserConfig(provider="mock")
    prompt = build_llm_prompt("Use MPB to compute a photonic crystal band diagram.", config=config)
    client = MockLLMClient()
    first = client.generate(prompt, config=config).raw_text
    second = client.generate(prompt, config=config).raw_text
    assert first == second
    assert "photonic_crystal" in first


def test_mock_llm_client_can_simulate_malformed_output():
    config = LLMParserConfig(provider="mock")
    prompt = build_llm_prompt("MOCK_MALFORMED Use Meep FDTD.", config=config)
    result = MockLLMClient().generate(prompt, config=config)
    assert result.raw_text.endswith(",}")
    assert result.warnings


def test_mock_llm_client_can_simulate_partial_output():
    config = LLMParserConfig(provider="mock")
    prompt = build_llm_prompt("MOCK_PARTIAL ambiguous request", config=config)
    result = MockLLMClient().generate(prompt, config=config)
    assert "partial mock output" in result.raw_text


def test_unsupported_provider_errors_without_network():
    with pytest.raises(LLMProviderError):
        make_llm_client("real-provider")
