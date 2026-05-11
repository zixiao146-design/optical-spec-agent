"""High-level service: parse -> validate -> format."""

from __future__ import annotations

from typing import Any

from optical_spec_agent.models.spec import OpticalSpec
from optical_spec_agent.parsers.base import BaseParser
from optical_spec_agent.parsers.llm import BaseLLMClient, LLMParserConfig, ParserReport
from optical_spec_agent.parsers.registry import get_parser
from optical_spec_agent.validators.spec_validator import SpecValidator


class SpecService:
    """Orchestrates parsing and validation.

    This is the main entry-point for both CLI and API usage.
    """

    def __init__(
        self,
        parser: str | BaseParser | None = None,
        *,
        llm_config: LLMParserConfig | None = None,
        llm_client: BaseLLMClient | None = None,
    ) -> None:
        if isinstance(parser, BaseParser):
            self.parser = parser
        else:
            self.parser = get_parser(parser or "rule", llm_config=llm_config, llm_client=llm_client)
        self.validator = SpecValidator()
        self.last_parser_report: ParserReport | None = None

    def process(
        self,
        text: str,
        *,
        task_id: str = "",
        parser: str | BaseParser | None = None,
        llm_config: LLMParserConfig | None = None,
        llm_client: BaseLLMClient | None = None,
    ) -> OpticalSpec:
        """Parse natural language -> validate -> return enriched spec."""
        parser_obj = (
            parser
            if isinstance(parser, BaseParser)
            else get_parser(parser, llm_config=llm_config, llm_client=llm_client)
            if parser is not None
            else self.parser
        )
        spec = parser_obj.parse(text, task_id=task_id)
        self.last_parser_report = getattr(parser_obj, "last_report", None)
        spec = self.validator.validate(spec)
        return spec

    def process_to_dict(
        self,
        text: str,
        *,
        task_id: str = "",
        parser: str | BaseParser | None = None,
        llm_config: LLMParserConfig | None = None,
        llm_client: BaseLLMClient | None = None,
    ) -> dict[str, Any]:
        """Convenience: returns the flat dict representation."""
        spec = self.process(
            text,
            task_id=task_id,
            parser=parser,
            llm_config=llm_config,
            llm_client=llm_client,
        )
        return spec.to_flat_dict()
