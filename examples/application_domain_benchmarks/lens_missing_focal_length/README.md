# lens_missing_focal_length

This benchmark scenario is a underconstrained case that should report missing inputs and questions.

## Goals

- EN: Optimize a lens preview for imaging.
- ZH: 请优化一个成像透镜预览。

## Expected Behavior

- Scenario type: `underconstrained`
- Expected primary domain: `lens_ray_optics`
- Expected candidate domains: `none`
- Expected confidence: `medium`
- Expected requirement template: `paraxial_lens_imaging`
- Expected calculators: `none`
- Expected adapters: `none`
- Expected blocked actions: `none`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
