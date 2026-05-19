# dielectric_metasurface_positive

This benchmark scenario is a positive coverage case for a supported local preview domain.

## Goals

- EN: Plan a dielectric metasurface phase profile preview for a TiO2 periodic meta atom.
- ZH: 请为 TiO2 周期性超表面单元结构规划介质超表面相位预览。

## Expected Behavior

- Scenario type: `positive`
- Expected primary domain: `dielectric_metasurface`
- Expected candidate domains: `none`
- Expected confidence: `high`
- Expected requirement template: `dielectric_metasurface_preview`
- Expected calculators: `none`
- Expected adapters: `meep, gmsh`
- Expected blocked actions: `none`

The local evaluator records actual domain matching, requirement matching, tool-call ledger entries, missing inputs, and recommended questions in `expected_result.json`.

## Safety Boundary

This benchmark performs no solver execution, calls no external LLM, performs no upload, creates no tag, and creates no release. It is preview/design-assist evidence only and claims no production-grade physical validation or formal convergence proof.
