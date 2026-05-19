# fiber_coupling_preview_positive

This benchmark scenario is a positive coverage case for a supported local preview domain.

## Goals

- EN: Preview fiber coupling with mode overlap and Gaussian beam assumptions.
- ZH: 请预览光纤耦合，包含模式重叠和高斯光束假设。

## Expected Behavior

- Scenario type: `positive`
- Expected primary domain: `fiber_coupling_preview`
- Expected candidate domains: `none`
- Expected confidence: `high`
- Expected requirement template: `gaussian_beam_focus`
- Expected calculators: `optics.fiber_coupling.gaussian_mode_overlap`
- Expected adapters: `mpb, optiland`
- Expected blocked actions: `none`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
