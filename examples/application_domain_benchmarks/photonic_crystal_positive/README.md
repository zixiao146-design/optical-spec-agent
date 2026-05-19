# photonic_crystal_positive

This benchmark scenario is a positive coverage case for a supported local preview domain.

## Goals

- EN: Create a photonic crystal band structure preview with an MPB adapter path.
- ZH: 请生成光子晶体能带结构的 MPB adapter 本地预览。

## Expected Behavior

- Scenario type: `positive`
- Expected primary domain: `photonic_crystal`
- Expected candidate domains: `none`
- Expected confidence: `high`
- Expected requirement template: `photonic_crystal_band_preview`
- Expected calculators: `none`
- Expected adapters: `mpb`
- Expected blocked actions: `none`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
