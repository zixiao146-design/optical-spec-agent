# slab_waveguide_positive

This benchmark scenario is a positive coverage case for a supported local preview domain.

## Goals

- EN: Design a single mode slab waveguide preview at 1550 nm with SiN core and SiO2 cladding.
- ZH: 请设计 1550 nm 的单模平板波导预览，芯层为氮化硅，包层为二氧化硅。

## Expected Behavior

- Scenario type: `positive`
- Expected primary domain: `slab_waveguide`
- Expected candidate domains: `none`
- Expected confidence: `high`
- Expected requirement template: `slab_waveguide_single_mode`
- Expected calculators: `optics.waveguide.sweep`
- Expected adapters: `mpb, elmer`
- Expected blocked actions: `none`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
