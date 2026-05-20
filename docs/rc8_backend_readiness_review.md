# rc8 Backend Readiness Review

Current public prerelease: v0.9.0rc8.
Current main development version: `0.9.0rc9.dev0`.

This review summarizes backend readiness after closing the optional solver
evidence loop for Gmsh, Optiland, Meep, and MPB. v0.9.0rc8 has since been
created as a verified GitHub prerelease. The review remains a backend evidence
record and does not authorize PyPI publication, TestPyPI upload, v0.9.0rc9 tag
creation, or `v1.0.0` release.

## Current Status

- PyPI: not published.
- TestPyPI: only `0.9.0rc6.dev0` uploaded and verified.
- `v0.9.0rc8` GitHub prerelease: created and verified.
- `v0.9.0rc9` tag: not created.
- `v1.0.0` tag: not created.
- Application domain benchmarks: 19 pass / 0 warn / 0 fail.
- Default gates: no external solver execution.

## Backend Evidence Completed

- Backend evidence pack exists and includes package/release status, sub-agent
  reality, tool-call reality, calculators, material provenance, ambiguous
  requirement matching, missing-input diagnostics, application-domain coverage,
  adapter-native golden coverage, validation maturity, and preview boundaries.
- Validation claim audit exists and is expected to run before any release-draft
  work.
- Backend capability report exists and remains conservative.

## Optional Solver Evidence Completed

- Gmsh: executed, passed, reviewed, accepted as optional manual
  mesh-generation smoke evidence.
- Optiland: executed, passed, reviewed, accepted as optional manual ray/path
  smoke evidence.
- Meep: executed, passed, reviewed, accepted as optional manual PyMeep/FDTD
  smoke evidence.
- MPB: executed, passed, reviewed, accepted as optional manual
  MPB/band-structure smoke evidence.
- Elmer: deferred, not Level 3, not executed.

## Application Domain Benchmarks

The application domain benchmark suite reports 19 pass / 0 warn / 0 fail. The
suite checks deterministic routing, candidate-domain behavior, missing-input
questions, unsupported/deferred behavior, and safe boundaries. It does not
establish physical correctness.

## Calculator / Reference Sanity Evidence

Thin-film, paraxial, Gaussian beam, waveguide, fiber-coupling, and polarization
calculators have sanity/reference cases and failure-mode tests. These are
sanity-checked preview/design-assist calculators, not production-grade physical
validation.

## Material Provenance And Ambiguous Diagnostics

The material catalog is a local preview/design-assist catalog with provenance
fields and user-verification requirements. Ambiguous and unknown natural-language
goals produce confidence, candidates, missing inputs, and recommended questions
instead of unsafe solver actions.

## Adapter-native Golden Coverage

Adapter-native golden coverage checks metadata and expected preview fragments for
Meep, MPB, Gmsh, Elmer, and Optiland adapters. These checks do not run solvers
and are not real solver monitor results.

## Preview Boundary And Validation Maturity

Validation maturity now maps calculators to `sanity_checked_preview`,
application-domain benchmarks to `benchmark_checked_preview`, adapter/source
monitor evidence to `fixture_guarded_preview`, and the reviewed Gmsh, Optiland,
Meep, and MPB solver evidence to optional manual smoke evidence. No
production-grade physical validation and no formal convergence proof are
claimed.

## Remaining Deferred Items

- Elmer remains deferred until a maintainable `ElmerSolver` install route exists.
- PyPI publication remains a separate maintainer decision.
- TestPyPI upload for `0.9.0rc8` is not approved here.
- `v0.9.0rc8` release draft work may be considered later, but this review does
  not authorize it.
- `v1.0.0` remains unreleased.

## Recommendation

Backend readiness is stronger after optional solver evidence closure for Gmsh,
Optiland, Meep, and MPB. Continue v1.0 readiness/backend engineering, keep Elmer
deferred, and keep PyPI/TestPyPI/tag/release decisions separately gated. Do not
claim production-grade validation, formal convergence proof, or optical
correctness from this evidence.

## Post-rc8 rc9 audit follow-up

Post-rc8 planning continues in `0.9.0rc9.dev0` through:

- `docs/rc9_v1_0_readiness_gap_audit.md`
- `docs/rc9_backend_stabilization_plan.md`
- `docs/rc9_pypi_publication_decision_review.md`
- `docs/rc9_go_no_go_matrix.md`
- `docs/rc9_release_strategy.md`

Current public prerelease remains `v0.9.0rc8`. PyPI remains unpublished,
`v1.0.0` remains unapproved, and Elmer remains deferred and not Level 3.
