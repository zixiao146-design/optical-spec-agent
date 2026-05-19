# thin_film_coating_positive

This benchmark scenario is a positive coverage case for a supported local preview domain.

## Goals

- EN: Design a thin film anti-reflection coating on glass at 550 nm using local preview calculators.
- ZH: 请为玻璃基底在 550 nm 设计薄膜增透镀膜，并只使用本地预览计算器。

## Expected Behavior

- Scenario type: `positive`
- Expected primary domain: `thin_film_coating`
- Expected candidate domains: `none`
- Expected confidence: `high`
- Expected requirement template: `thin_film_ar_coating`
- Expected calculators: `optics.thin_film.spectrum`
- Expected adapters: `none`
- Expected blocked actions: `none`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
