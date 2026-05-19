# Material-Template Cross-Checks

Material-template cross-checks verify that each application domain has a
reviewable path through local materials, requirement templates, calculators or
adapters, and missing-input questions.

## What Is Checked

- A linked requirement template exists.
- Suggested materials exist in the local preview material catalog.
- Material suitability diagnostics can be produced for the domain.
- Expected calculators or adapter preview families are recorded.
- Missing-input and disambiguation questions are present.
- Safety flags stay false for solver execution, external LLM usage,
  production-grade validation, and any claimed convergence proof.

## Status Semantics

- `pass`: the domain has local preview coverage for templates, materials,
  questions, and expected tool paths.
- `warning`: the domain is intentionally partial or deferred, but the limitation
  is explicit.
- `fail`: a required local coverage item is missing.

## Former Warning Domains

`fiber_coupling_preview` and `polarization_optics_preview` now have local
deterministic preview calculators. Fiber coupling uses a scalar Gaussian
mode-overlap estimate, and polarization optics uses ideal Jones-calculus
polarizer/waveplate helpers. Real coupling validation, vector EM behavior,
fabrication effects, depolarization, and measured device performance still
require explicit solver or experimental validation.

## Benchmark Link

`examples/application_domain_benchmarks/` extends these cross-checks into
natural-language scenarios. The benchmark evaluator verifies that positive
domains match expected local paths, ambiguous goals preserve candidates and
questions, underconstrained goals report missing inputs, and unsupported
commercial or production-grade requests are blocked/deferred.

## Safety Boundary

The cross-checks do not run solvers, do not call external LLMs, and do not query
external material databases. They are preview/design-assist checks and do not
prove production-grade physical validation.
