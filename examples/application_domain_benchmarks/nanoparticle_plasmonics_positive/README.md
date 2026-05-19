# nanoparticle_plasmonics_positive

This benchmark scenario is a positive coverage case for a supported local preview domain.

## Goals

- EN: Create a local preview for a silver nanoparticle plasmonic scattering spectrum from 400 to 900 nm.
- ZH: 请为银纳米颗粒等离激元散射谱生成 400 到 900 nm 的本地预览。

## Expected Behavior

- Scenario type: `positive`
- Expected primary domain: `nanoparticle_plasmonics`
- Expected candidate domains: `none`
- Expected confidence: `high`
- Expected requirement template: `nanoparticle_plasmonics`
- Expected calculators: `none`
- Expected adapters: `meep, gmsh`
- Expected blocked actions: `none`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
