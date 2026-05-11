"""Parser registry for rule, LLM, and hybrid parser modes."""

from __future__ import annotations

from optical_spec_agent.parsers.base import BaseParser
from optical_spec_agent.parsers.llm import BaseLLMClient, HybridParser, LLMParser, LLMParserConfig
from optical_spec_agent.parsers.rule_based import RuleBasedParser


class ParserRegistryError(ValueError):
    """Raised for unknown parser names."""


_ALIASES = {
    "rule": "rule",
    "rules": "rule",
    "rule_based": "rule",
    "rule-based": "rule",
    "llm": "llm",
    "hybrid": "hybrid",
}


def normalize_parser_name(name: str | None) -> str:
    key = (name or "rule").strip().lower()
    try:
        return _ALIASES[key]
    except KeyError as exc:
        raise ParserRegistryError(
            f"Unknown parser {name!r}. Expected one of: rule, llm, hybrid."
        ) from exc


def get_parser(
    name: str | None = "rule",
    *,
    llm_config: LLMParserConfig | None = None,
    llm_client: BaseLLMClient | None = None,
) -> BaseParser:
    """Construct a parser by name."""

    normalized = normalize_parser_name(name)
    if normalized == "rule":
        return RuleBasedParser()
    if normalized == "llm":
        return LLMParser(config=llm_config, client=llm_client)
    if normalized == "hybrid":
        return HybridParser(config=llm_config, client=llm_client)
    raise ParserRegistryError(f"Unknown parser {name!r}")
