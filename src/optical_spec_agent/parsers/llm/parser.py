"""LLM and hybrid parser implementations for v0.8."""

from __future__ import annotations

import uuid
from copy import deepcopy

from optical_spec_agent.models.spec import OpticalSpec
from optical_spec_agent.parsers.base import BaseParser
from optical_spec_agent.parsers.llm.client import BaseLLMClient, LLMProviderError, make_llm_client
from optical_spec_agent.parsers.llm.config import LLMParserConfig, ParserReport
from optical_spec_agent.parsers.llm.merge import merge_specs_conservatively, summarize_spec
from optical_spec_agent.parsers.llm.prompt import build_llm_prompt
from optical_spec_agent.parsers.llm.repair import (
    LLMJSONError,
    extract_json_object,
    llm_dict_to_optical_spec,
    repair_common_json_issues,
)
from optical_spec_agent.parsers.rule_based import RuleBasedParser


class LLMParserError(RuntimeError):
    """Raised when LLM parsing fails without fallback."""


class LLMParser(BaseParser):
    """Schema-guided LLM parser using a provider-agnostic client."""

    def __init__(
        self,
        *,
        config: LLMParserConfig | None = None,
        client: BaseLLMClient | None = None,
    ) -> None:
        self.config = config or LLMParserConfig(parser_mode="llm")
        self.client = client or make_llm_client(self.config.provider)
        self.last_report = ParserReport(
            parser_mode=self.config.parser_mode,
            provider=self.config.provider,
            model=self.config.model,
            prompt_version=self.config.prompt_version,
        )

    def parse(self, text: str, *, task_id: str = "") -> OpticalSpec:
        if not task_id:
            task_id = uuid.uuid4().hex[:8]

        report = ParserReport(
            parser_mode=self.config.parser_mode,
            provider=self.config.provider,
            model=self.config.model,
            prompt_version=self.config.prompt_version,
        )
        self.last_report = report

        parse_text = text
        if len(parse_text) > self.config.max_input_chars:
            parse_text = parse_text[: self.config.max_input_chars]
            report.warnings.append("Input text exceeded max_input_chars and was truncated.")

        prompt = build_llm_prompt(parse_text, config=self.config)
        try:
            result = self.client.generate(prompt, config=self.config)
            report.warnings.extend(result.warnings)
            report.errors.extend(result.errors)
            if self.config.allow_repair:
                repaired_text = repair_common_json_issues(result.raw_text)
                report.repair_used = repaired_text != result.raw_text.strip()
                data = extract_json_object(result.raw_text)
            else:
                import json

                parsed = json.loads(result.raw_text)
                if not isinstance(parsed, dict):
                    raise LLMJSONError("LLM response must contain a JSON object")
                data = parsed
            if result.raw_text.strip() != result.raw_text or not result.raw_text.strip().startswith("{"):
                report.repair_used = report.repair_used or self.config.allow_repair
            spec = llm_dict_to_optical_spec(data, task_id=task_id)
            spec.assumption_log.append(
                f"[parser] llm provider={self.config.provider} model={self.config.model} "
                f"prompt_version={self.config.prompt_version}"
            )
            if report.repair_used:
                spec.assumption_log.append("[parser] LLM JSON extraction/repair was used")
            report.llm_summary = summarize_spec(spec)
            spec.collect_all()
            return spec
        except LLMProviderError as exc:
            report.errors.append(str(exc))
            raise LLMParserError(str(exc)) from exc
        except (LLMJSONError, Exception) as exc:
            report.errors.append(str(exc))
            if self.config.fallback_to_rule_based:
                report.fallback_used = True
                fallback = RuleBasedParser().parse(text, task_id=task_id)
                fallback.collect_all()
                fallback.assumption_log.append(f"[fallback_rule] LLM parser failed: {exc}")
                report.rule_based_summary = summarize_spec(fallback)
                return fallback
            raise LLMParserError(str(exc)) from exc


class HybridParser(BaseParser):
    """Rule baseline + LLM candidate + conservative merge."""

    def __init__(
        self,
        *,
        config: LLMParserConfig | None = None,
        client: BaseLLMClient | None = None,
    ) -> None:
        base_config = config or LLMParserConfig(parser_mode="hybrid")
        self.config = base_config.model_copy(update={"parser_mode": "hybrid"})
        self.client = client or make_llm_client(self.config.provider)
        self.rule_parser = RuleBasedParser()
        self.last_report = ParserReport(
            parser_mode="hybrid",
            provider=self.config.provider,
            model=self.config.model,
            prompt_version=self.config.prompt_version,
        )

    def parse(self, text: str, *, task_id: str = "") -> OpticalSpec:
        if not task_id:
            task_id = uuid.uuid4().hex[:8]

        rule_spec = self.rule_parser.parse(text, task_id=task_id)
        report = ParserReport(
            parser_mode="hybrid",
            provider=self.config.provider,
            model=self.config.model,
            prompt_version=self.config.prompt_version,
            rule_based_summary=summarize_spec(rule_spec),
        )
        self.last_report = report

        llm_config = self.config.model_copy(update={"parser_mode": "llm"})
        llm_parser = LLMParser(config=llm_config, client=self.client)
        try:
            llm_spec = llm_parser.parse(text, task_id=task_id)
            report.fallback_used = llm_parser.last_report.fallback_used
            report.repair_used = llm_parser.last_report.repair_used
            report.warnings.extend(llm_parser.last_report.warnings)
            report.errors.extend(llm_parser.last_report.errors)
            report.llm_summary = summarize_spec(llm_spec)
        except LLMParserError as exc:
            report.errors.append(str(exc))
            if self.config.fallback_to_rule_based:
                report.fallback_used = True
                fallback = deepcopy(rule_spec)
                fallback.collect_all()
                fallback.assumption_log.append(f"[fallback_rule] Hybrid LLM candidate failed: {exc}")
                return fallback
            raise

        if report.fallback_used and not self.config.fallback_to_rule_based:
            return llm_spec

        merged = merge_specs_conservatively(rule_spec, llm_spec, report)
        merged.assumption_log.append(
            f"[parser] hybrid provider={self.config.provider} model={self.config.model}"
        )
        if report.fallback_used:
            merged.assumption_log.append("[fallback_rule] Hybrid parser used rule fallback")
        existing_assumptions = list(merged.assumption_log)
        merged.collect_all()
        merged.assumption_log.extend(item for item in existing_assumptions if item not in merged.assumption_log)
        return merged
