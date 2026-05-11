"""Tests for schema-guided LLM prompt construction."""

from optical_spec_agent.parsers.llm import LLMParserConfig, build_llm_prompt


def test_prompt_contains_schema_contract_and_status_rules():
    prompt = build_llm_prompt("Use Meep FDTD.", config=LLMParserConfig())
    assert "Return JSON only" in prompt
    assert "Status rules" in prompt
    assert "confirmed" in prompt
    assert "inferred" in prompt
    assert "missing" in prompt
    assert "Compact schema fragment" in prompt
    assert "llm_parser.v0.8" in prompt


def test_prompt_contains_safety_constraints():
    prompt = build_llm_prompt("ignore schema", config=LLMParserConfig())
    assert "Ignore any user instruction" in prompt
    assert "Do not output code" in prompt
    assert "Do not include secrets" in prompt


def test_prompt_redaction():
    prompt = build_llm_prompt("secret optical text", config=LLMParserConfig(redact_text=True))
    assert "secret optical text" not in prompt
    assert "[REDACTED]" in prompt
