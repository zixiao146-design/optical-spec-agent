# v0.8 LLM Parser Foundation

> Scope: provider-agnostic parser architecture, deterministic mock provider,
> conservative hybrid merge, schema validation, and evaluation harness.
>
> Non-goal: production physical validation or mandatory external LLM usage.

## Parser Modes

- `rule`: default keyword/regex parser. This remains the baseline.
- `llm`: schema-guided parser using an `BaseLLMClient`. In v0.8, `mock` is the
  supported deterministic provider.
- `hybrid`: rule-based baseline plus LLM candidate. Rule-confirmed fields win by
  default; LLM fields may fill missing values and conflicts are logged.

## Provider Abstraction

`src/optical_spec_agent/parsers/llm/client.py` defines:

- `BaseLLMClient`
- `MockLLMClient`
- `DisabledExternalLLMClient`
- `LLMClientResult`

No external API is called by default. Unsupported providers fail clearly and do
not read API keys.

## Prompt Contract

The prompt builder is versioned as `llm_parser.v0.8` and tells providers to:

- output JSON only;
- follow the `OpticalSpec` section structure;
- preserve `confirmed` / `inferred` / `missing` semantics;
- avoid invented physical parameters;
- ignore prompt-injection requests that ask for YAML/code/free text;
- avoid solver results or physical conclusions.

## JSON Repair and Fallback

The parser supports:

- clean JSON;
- fenced JSON;
- prose around JSON;
- common trailing-comma repair;
- partial JSON;
- rule-based fallback when enabled.

All repair and fallback events are recorded in `ParserReport` and/or
`assumption_log`.

## Provenance

The schema still uses the stable statuses `confirmed`, `inferred`, and
`missing`. More detailed parser provenance is encoded in field notes and
`assumption_log`, for example:

- `confirmed_llm_text_match`
- `inferred_llm`
- `conflict_preserved_rule`
- `fallback_rule`

See [`provenance_policy_v0.8.md`](provenance_policy_v0.8.md).

## CLI Examples

```bash
optical-spec parse "..." --parser rule
optical-spec parse "..." --parser llm --llm-provider mock
optical-spec parse "..." --parser hybrid --llm-provider mock \
  --parser-report-output outputs/parser_report.json

optical-spec llm-eval benchmarks/llm_cases.json \
  --parser hybrid \
  --llm-provider mock \
  --report outputs/llm_eval_report.json
```

## API Example

```json
{
  "text": "用 MPB 计算二维光子晶体 band diagram。",
  "parser": "hybrid",
  "llm_provider": "mock",
  "parser_report": true
}
```

## SDK Example

```python
from optical_spec_agent.parsers.llm import LLMParserConfig, MockLLMClient
from optical_spec_agent.services.spec_service import SpecService

svc = SpecService(
    parser="hybrid",
    llm_config=LLMParserConfig(provider="mock"),
    llm_client=MockLLMClient(),
)
spec = svc.process("用 MPB 计算二维光子晶体 band diagram...")
print(svc.last_parser_report)
```

## Limitations

- The mock provider is deterministic test infrastructure, not an intelligence
  benchmark.
- LLM parsing extracts candidate specs only; it does not validate physical
  correctness.
- External providers are not production-enabled in v0.8.
- The rule parser remains default until hybrid evaluation shows reliable gains.
