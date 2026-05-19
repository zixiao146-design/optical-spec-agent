# waveguide_missing_core_thickness

This benchmark scenario is a underconstrained case that should report missing inputs and questions.

## Goals

- EN: Plan a single mode slab waveguide preview.
- ZH: 请规划一个单模平板波导预览。

## Expected Behavior

- Scenario type: `underconstrained`
- Expected primary domain: `slab_waveguide`
- Expected candidate domains: `none`
- Expected confidence: `high`
- Expected requirement template: `slab_waveguide_single_mode`
- Expected calculators: `none`
- Expected adapters: `none`
- Expected blocked actions: `none`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
