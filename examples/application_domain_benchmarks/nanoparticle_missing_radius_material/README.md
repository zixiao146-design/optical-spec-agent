# nanoparticle_missing_radius_material

This benchmark scenario is a underconstrained case that should report missing inputs and questions.

## Goals

- EN: Plan a nanoparticle scattering preview.
- ZH: 请规划一个纳米颗粒散射预览。

## Expected Behavior

- Scenario type: `underconstrained`
- Expected primary domain: `nanoparticle_plasmonics`
- Expected candidate domains: `none`
- Expected confidence: `high`
- Expected requirement template: `nanoparticle_plasmonics`
- Expected calculators: `none`
- Expected adapters: `none`
- Expected blocked actions: `none`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
