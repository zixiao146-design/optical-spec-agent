"""Provider abstraction for v0.8 LLM parsing.

Only deterministic local providers are implemented here. External provider
support is intentionally represented as a disabled stub so tests never require
network access or API keys.
"""

from __future__ import annotations

import json
import re
from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from optical_spec_agent.parsers.llm.config import LLMClientResult, LLMParserConfig
from optical_spec_agent.parsers.rule_based import RuleBasedParser


class LLMProviderError(RuntimeError):
    """Raised when an LLM provider is unsupported or disabled."""


class BaseLLMClient(ABC):
    """Provider-agnostic LLM client interface."""

    @abstractmethod
    def generate(self, prompt: str, *, config: LLMParserConfig) -> LLMClientResult:
        """Generate a parser response for *prompt*."""
        ...


class MockLLMClient(BaseLLMClient):
    """Deterministic no-network mock provider used by tests and demos."""

    provider_name = "mock"

    def generate(self, prompt: str, *, config: LLMParserConfig) -> LLMClientResult:
        text = _extract_user_text(prompt)
        spec = RuleBasedParser().parse(text, task_id="mock-llm")
        spec.assumption_log.append("LLM mock provider generated schema-shaped JSON from local rules.")
        payload = json.loads(json.dumps(spec.to_flat_dict(), ensure_ascii=False, default=_json_default))
        _enrich_mock_payload(payload, text)

        raw = json.dumps(payload, ensure_ascii=False)
        lowered = text.lower()
        warnings: list[str] = []

        if "mock_partial" in lowered:
            raw = json.dumps(
                {
                    "task": {
                        "task_type": {
                            "value": "simulation",
                            "status": "inferred",
                            "note": "partial mock output",
                        },
                        "research_goal": {
                            "value": text[:200],
                            "status": "confirmed",
                            "note": "partial mock output",
                        },
                    }
                },
                ensure_ascii=False,
            )
            warnings.append("Mock provider returned partial JSON.")
        elif "mock_malformed" in lowered:
            raw = raw[:-1] + ",}"
            warnings.append("Mock provider returned JSON with a trailing comma.")
        elif "mock_irreparable" in lowered:
            raw = "This is not JSON and cannot be repaired."
            warnings.append("Mock provider returned irreparable text.")
        elif "mock_fenced_json" in lowered:
            raw = f"```json\n{raw}\n```"
        elif "mock_prose_json" in lowered:
            raw = f"Here is the extracted spec:\n{raw}\nDone."

        return LLMClientResult(
            raw_text=raw,
            parsed_json=payload if raw.startswith("{") and raw.endswith("}") else None,
            finish_reason="stop",
            model=config.model,
            provider=self.provider_name,
            usage={"prompt_chars": len(prompt), "response_chars": len(raw)},
            warnings=warnings,
        )


class DisabledExternalLLMClient(BaseLLMClient):
    """Explicit disabled stub for unsupported external providers."""

    def __init__(self, provider: str = "disabled") -> None:
        self.provider = provider

    def generate(self, prompt: str, *, config: LLMParserConfig) -> LLMClientResult:
        raise LLMProviderError(
            f"LLM provider {config.provider!r} is not enabled. "
            "Use --llm-provider mock for deterministic local parsing."
        )


def make_llm_client(provider: str) -> BaseLLMClient:
    """Create an LLM client without network access."""

    normalized = provider.lower().strip()
    if normalized == "mock":
        return MockLLMClient()
    if normalized == "disabled":
        return DisabledExternalLLMClient(provider=normalized)
    raise LLMProviderError(
        f"Unsupported LLM provider {provider!r}. "
        "Only 'mock' and 'disabled' are available without external APIs."
    )


def _extract_user_text(prompt: str) -> str:
    match = re.search(r"USER_TEXT:\s*(.*)\Z", prompt, re.DOTALL)
    if not match:
        return prompt
    return match.group(1).strip()


def _enrich_mock_payload(payload: dict, text: str) -> None:
    """Fill conservative fields the mock LLM can infer from solver-intent text."""

    lowered = text.lower()
    task_type = payload.setdefault("task", {}).setdefault("task_type", {})
    if task_type.get("status") == "missing" and any(
        token in lowered
        for token in (
            "simulate",
            "simulation",
            "compute",
            "calculate",
            "mode",
            "solver",
            "band",
            "mesh",
            "ray tracing",
            "mtf",
            "spot diagram",
            "design",
            "仿真",
            "计算",
            "模式",
            "网格",
            "能带",
        )
    ):
        payload["task"]["task_type"] = {
            "value": "simulation",
            "status": "inferred",
            "note": "inferred_llm: solver or calculation intent in text",
        }


def _json_default(value: Any) -> Any:
    if isinstance(value, BaseModel):
        return value.model_dump()
    return str(value)
