# imaging_system_preview_positive

This benchmark scenario is a positive coverage case for a supported local preview domain.

## Goals

- EN: Plan an imaging system preview with magnification, image plane, and aperture questions.
- ZH: 请规划成像系统预览，包含放大率、像面和孔径问题。

## Expected Behavior

- Scenario type: `positive`
- Expected primary domain: `imaging_system_preview`
- Expected candidate domains: `none`
- Expected confidence: `high`
- Expected requirement template: `paraxial_lens_imaging`
- Expected calculators: `optics.paraxial.two_lens_relay`
- Expected adapters: `optiland`
- Expected blocked actions: `none`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
