# generic_optical_system_ambiguous

This benchmark scenario is a ambiguous case that should preserve candidates and ask follow-up questions.

## Goals

- EN: Design an optical system.
- ZH: 设计一个光学系统。

## Expected Behavior

- Scenario type: `ambiguous`
- Expected primary domain: `none`
- Expected candidate domains: `thin_film_coating, slab_waveguide, lens_ray_optics, gaussian_beam_focusing, nanoparticle_plasmonics`
- Expected confidence: `low`
- Expected requirement template: `none`
- Expected calculators: `none`
- Expected adapters: `none`
- Expected blocked actions: `none`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
