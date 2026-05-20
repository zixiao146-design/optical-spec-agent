# v0.9.0rc8 Release Notes

## Summary

v0.9.0rc8 is a backend-readiness release candidate draft for the v0.9.0 line.
It consolidates application-domain benchmarks, material provenance and
ambiguous requirement diagnostics, calculator sanity evidence, validation
maturity boundaries, preview boundary policy, and optional solver evidence.

This document is release-note preparation only. The v0.9.0rc8 tag and GitHub
release have not been created, TestPyPI upload for 0.9.0rc8 has not been
performed, and PyPI publication is not approved. The v0.9.0rc8 tag and GitHub
release have not been created.

The v0.9.0rc8 tag and GitHub release have not been created.
TestPyPI upload for 0.9.0rc8 has not been performed.

## Highlights

- Application domain benchmarks report 19 pass / 0 warn / 0 fail.
- Material provenance and suitability diagnostics are explicit and testable.
- Ambiguous natural-language and missing-input diagnostics are expanded.
- Fiber coupling and polarization preview calculators include reference sanity
  evidence.
- Backend validation maturity and preview boundary policy are documented.
- Validation claim audit guards against overclaiming.
- Optional solver evidence is summarized and reviewed for Gmsh, Optiland, Meep,
  and MPB.
- Elmer remains deferred and not Level 3.

## Application Domain Benchmarks

The application-domain benchmark suite covers positive, ambiguous,
underconstrained, unsupported, and blocked requests. The current result is
19 pass / 0 warn / 0 fail. These benchmarks test deterministic routing,
diagnostics, and safety boundaries; they do not prove physical correctness.

## Material Provenance and Ambiguous Diagnostics

The material library remains a preview/design-assist catalog with user
verification requirements. Requirement matching produces confidence levels,
candidate templates, missing-input diagnostics, and recommended questions for
ambiguous or underconstrained goals.

## Fiber Coupling and Polarization Calculators

Fiber coupling and polarization preview calculators include deterministic
reference sanity cases and bounded quality fields. These are sanity-checked
preview calculators, not production-grade physical validation.

## Backend Validation Maturity and Preview Boundary Policy

The backend validation maturity matrix maps calculators, materials, application
domains, adapter-native golden coverage, optional solver evidence, and task
session traces to conservative evidence levels. The preview boundary policy
states what users may rely on and what must be verified externally.

## Optional Solver Micro-benchmark Evidence

- Gmsh: executed, passed, reviewed, accepted as optional manual mesh-generation
  smoke evidence.
- Optiland: executed, passed, reviewed, accepted as optional manual ray/path
  smoke evidence.
- Meep: executed, passed, reviewed, accepted as optional manual PyMeep/FDTD
  smoke evidence.
- MPB: executed, passed, reviewed, accepted as optional manual
  MPB/band-structure smoke evidence.
- Elmer: deferred, not Level 3, and not executed.

Optional solver evidence proves opt-in path viability and recorded review
discipline. It does not prove production-grade solver validation, formal
convergence, optical correctness, or production band-structure validation.

## TestPyPI / PyPI Status

- TestPyPI uploaded and verified only for 0.9.0rc6.dev0.
- TestPyPI upload for 0.9.0rc8: not performed.
- PyPI: not published.
- PyPI publication approval: not granted.

## Verification

- validation claim audit: passed.
- application domain benchmarks: 19 pass / 0 warn / 0 fail.
- sub-agent audit: passed.
- optional solver wrapper default no-execute: passed.
- backend capability/report/evidence smoke: passed.
- API fixture check and API smoke: passed.
- TestPyPI no-upload preflight: passed.
- quality gates: passed.
- normal smoke and wheel smoke: passed.
- pytest: passed.
- python -m build: passed.
- make check: passed.
- CLI examples: passed.
- dist filenames:
  - optical_spec_agent-0.9.0rc8-py3-none-any.whl
  - optical_spec_agent-0.9.0rc8.tar.gz

## Scope Limitations

- No PyPI publish.
- No TestPyPI upload for 0.9.0rc8.
- No production-grade physical validation.
- No production-grade solver validation.
- No production-grade FDTD validation.
- No production-grade MPB validation.
- No production band-structure validation.
- No formal convergence proof.
- No optical correctness claim.
- External solvers are not run by default.
- External LLMs are not called by default.
- Proprietary solvers are not default dependencies.
- Elmer Level 3 validation remains deferred.

## Tag / Release Note

The v0.9.0rc8 tag and GitHub release are not created by this release-draft
preparation. They require separate maintainer approval.
