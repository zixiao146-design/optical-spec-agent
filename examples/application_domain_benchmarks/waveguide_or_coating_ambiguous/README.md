# waveguide_or_coating_ambiguous

This benchmark scenario is a ambiguous case that should preserve candidates and ask follow-up questions.

## Goals

- EN: Design a waveguide and thin-film coating preview for an integrated photonics stack.
- ZH: 请为集成光子堆栈设计一个波导和薄膜镀膜预览。

## Expected Behavior

- Scenario type: `ambiguous`
- Expected primary domain: `none`
- Expected candidate domains: `slab_waveguide, thin_film_coating`
- Expected confidence: `low`
- Expected requirement template: `none`
- Expected calculators: `none`
- Expected adapters: `none`
- Expected blocked actions: `none`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
