# Release Notes: v0.9.0rc7

## Summary

v0.9.0rc7 is a release-draft-ready candidate focused on backend evidence,
optical design agent capability, deterministic tool-call visibility, and local
preview workflows. It follows the verified public `v0.9.0rc6` prerelease.

## Highlights

- Backend evidence review decision recorded as sufficient for rc7 draft.
- Material Library and optical design examples added.
- Agent Command Center task sessions added.
- Design requirement templates and natural-language to optical-language matching added.
- Tool-call ledger added to backend task sessions.
- Local optical calculators deepened with sanity/reference cases.
- Source/monitor diagnostics and observable diagnostics added.
- Adapter-native source/monitor mappings added.
- Adapter golden coverage and strict metadata diff checks added.
- Backend evidence review pack added.
- Agent Studio frontend, Chinese localization, quickstart, and local demo package remain available.

## Backend Evidence Review Decision

`docs/backend_evidence_review_decision.md` records backend evidence as sufficient
to prepare a `v0.9.0rc7` release draft. It does not approve `v0.9.0rc7` tag
creation, GitHub release creation, TestPyPI upload, PyPI publication, or
`v1.0.0` release.

## Material Library

The local material library is a preview/design-assist catalog for examples and
agent planning. It is not a production-grade optical constants database.

## Optical Design Examples

The optical design examples now cover nanoparticle plasmonics, thin-film
coating, waveguide mode, photonic crystal band, dielectric metasurface preview,
and lens raytrace preview.

## Agent Command Center

Agent task sessions connect natural-language goals to optical intent, design
cases, plan steps, sub-agent traces, permission gates, artifacts, evidence, and
next actions without calling an external LLM by default.

## Tool-call Ledger

The backend records internal tools that executed, calculator calls that ran, and
external solver/LLM/publication/release actions that remained blocked.

## Optical Calculators

Thin-film, paraxial, Gaussian beam, and waveguide calculators are available as
sanity-checked preview/design-assist tools with reference cases and failure-mode
tests.

## Source/Monitor Diagnostics

The optical-language layer infers source models, monitor models, missing inputs,
default assumptions, and safe-to-preview diagnostics.

## Observable Diagnostics

Observable diagnostics map scattering, reflection/transmission, near/far field,
band structure, focal spot, image plane, ray fan, phase profile, mesh region,
and related preview observables to required inputs and limitations.

## Adapter-native Mappings

Adapter-native mappings explain how source/monitor/observable intent maps to
Meep, MPB, Gmsh, Elmer, and Optiland preview metadata without executing solvers.

## Adapter Golden Coverage

Adapter-native golden cases and strict metadata diff checks cover Meep, MPB,
Gmsh, Elmer, and Optiland preview semantics.

## TestPyPI/PyPI Status

- TestPyPI uploaded and verified only for `0.9.0rc6.dev0`.
- TestPyPI upload for `0.9.0rc7`: not performed.
- PyPI: not published.
- PyPI publication approval: not granted.

## Verification

- backend evidence pack smoke: passed
- backend capability smoke: passed
- adapter-native golden checker: passed
- sub-agent audit: passed
- API fixture check: passed
- API smoke: passed
- TestPyPI no-upload preflight: passed
- normal smoke: passed
- wheel smoke: passed
- quality gates: passed
- pytest: 761 passed, 4 warnings
- python -m build: passed
- make check: passed
- CLI examples: passed

## Scope Limitations

- No PyPI publication.
- No TestPyPI upload for 0.9.0rc7.
- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLMs are not called by default.
- Proprietary solvers are not required by default.
- Elmer Level 3 remains deferred.
- Adapter-native golden cases are preview metadata checks, not real solver monitor results.

## Tag/Release Note

The `v0.9.0rc7` tag and GitHub release are not created yet. They require
separate explicit maintainer approval.
