# Parser Provenance Policy v0.8

`OpticalSpec` keeps the stable status surface:

- `confirmed`
- `inferred`
- `missing`

v0.8 does not expand the enum-like status values because schema stability is a
project goal. More detailed parser provenance is encoded in `note`,
`assumption_log`, and parser reports.

## Detailed Provenance Labels

- `confirmed_rule`: field was matched directly by deterministic rules.
- `confirmed_llm_text_match`: LLM/mock candidate supplied a value grounded in
  text evidence.
- `inferred_rule`: rule-based conservative inference.
- `inferred_llm`: LLM/mock conservative inference.
- `missing`: insufficient information.
- `conflict_preserved_rule`: hybrid parser kept the rule-based value over an
  LLM conflict.
- `fallback_rule`: LLM parsing failed and the rule parser was used.

## Policy

- `confirmed` requires text evidence.
- LLM-only extrapolation should be `inferred`, not `confirmed`.
- Ungrounded LLM content should become a warning or remain missing.
- Rule-confirmed fields win hybrid conflicts by default.
- Repair, fallback, and conflicts must be visible in parser reports.
- LLM output is parsed as JSON only; it is never executed as code.

## Known Compromise

Because `StatusField.status` remains schema-compatible, detailed labels are not
new status values. They are stored in notes and logs until a future schema
revision explicitly broadens provenance categories.
