# lens_or_gaussian_focus_ambiguous

This benchmark scenario is a ambiguous case that should preserve candidates and ask follow-up questions.

## Goals

- EN: Focus a Gaussian beam with a lens, but decide whether this is a beam or ray-optics task.
- ZH: 请用透镜聚焦高斯光束，但需要判断这是光束任务还是光线光学任务。

## Expected Behavior

- Scenario type: `ambiguous`
- Expected primary domain: `none`
- Expected candidate domains: `gaussian_beam_focusing, lens_ray_optics`
- Expected confidence: `low`
- Expected requirement template: `none`
- Expected calculators: `none`
- Expected adapters: `none`
- Expected blocked actions: `none`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
