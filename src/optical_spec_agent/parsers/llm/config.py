"""Configuration and report models for the v0.8 LLM parser foundation."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


ParserMode = Literal["llm", "hybrid"]


class LLMParserConfig(BaseModel):
    """Provider-agnostic parser configuration.

    The default provider is deterministic and local. External providers are not
    enabled by this foundation layer.
    """

    provider: str = "mock"
    model: str = "mock-optical-parser"
    temperature: float = 0.0
    max_tokens: int | None = None
    strict_json: bool = True
    allow_repair: bool = True
    fallback_to_rule_based: bool = True
    parser_mode: ParserMode = "llm"
    prompt_version: str = "llm_parser.v0.8"
    schema_version: str = "optical_spec.v0"
    timeout_seconds: int | None = None
    redact_text: bool = False
    max_input_chars: int = 12000


class LLMClientResult(BaseModel):
    """Raw provider response plus optional parsed metadata."""

    raw_text: str
    parsed_json: dict[str, Any] | None = None
    finish_reason: str = "stop"
    model: str = ""
    provider: str = ""
    usage: dict[str, Any] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    latency_ms: float | None = None


class ParserReport(BaseModel):
    """Machine-readable parser report for CLI/API/evaluation."""

    parser_mode: str
    provider: str = ""
    model: str = ""
    prompt_version: str = "llm_parser.v0.8"
    fallback_used: bool = False
    repair_used: bool = False
    conflicts: list[dict[str, Any]] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    errors: list[str] = Field(default_factory=list)
    rule_based_summary: dict[str, Any] = Field(default_factory=dict)
    llm_summary: dict[str, Any] = Field(default_factory=dict)
    merged_fields: list[str] = Field(default_factory=list)
