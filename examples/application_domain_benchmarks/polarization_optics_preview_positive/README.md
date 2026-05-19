# polarization_optics_preview_positive

This benchmark scenario is a positive coverage case for a supported local preview domain.

## Goals

- EN: Create a polarization waveplate preview with input polarization and retardance questions.
- ZH: 请创建偏振波片预览，包含输入偏振和延迟量问题。

## Expected Behavior

- Scenario type: `positive`
- Expected primary domain: `polarization_optics_preview`
- Expected candidate domains: `none`
- Expected confidence: `high`
- Expected requirement template: `none`
- Expected calculators: `none`
- Expected adapters: `none`
- Expected blocked actions: `none`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
