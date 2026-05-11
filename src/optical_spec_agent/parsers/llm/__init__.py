"""v0.8 provider-agnostic LLM parser foundation."""

from optical_spec_agent.parsers.llm.client import (
    BaseLLMClient,
    DisabledExternalLLMClient,
    LLMProviderError,
    MockLLMClient,
    make_llm_client,
)
from optical_spec_agent.parsers.llm.config import LLMClientResult, LLMParserConfig, ParserReport
from optical_spec_agent.parsers.llm.parser import HybridParser, LLMParser, LLMParserError
from optical_spec_agent.parsers.llm.prompt import build_llm_prompt
from optical_spec_agent.parsers.llm.repair import (
    LLMJSONError,
    extract_json_object,
    llm_dict_to_optical_spec,
    normalize_llm_spec_dict,
    repair_common_json_issues,
)

__all__ = [
    "BaseLLMClient",
    "DisabledExternalLLMClient",
    "HybridParser",
    "LLMClientResult",
    "LLMJSONError",
    "LLMParser",
    "LLMParserConfig",
    "LLMParserError",
    "LLMProviderError",
    "MockLLMClient",
    "ParserReport",
    "build_llm_prompt",
    "extract_json_object",
    "llm_dict_to_optical_spec",
    "make_llm_client",
    "normalize_llm_spec_dict",
    "repair_common_json_issues",
]
