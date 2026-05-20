# rc8.dev0 Backend Roadmap

Current public prerelease: `v0.9.0rc7`.
Current main development version: `0.9.0rc8.dev0`.

This roadmap describes post-`v0.9.0rc7` backend engineering toward a future
`v0.9.0rc8` candidate. It is not a release draft, does not create a tag, does
not approve PyPI publication, and does not authorize TestPyPI upload.

## Operating Boundaries

- `0.9.0rc8.dev0` is not a public release.
- `v0.9.0rc8` tag has not been created.
- `v1.0.0` tag has not been created.
- PyPI remains unpublished.
- PyPI publication approval remains not granted.
- TestPyPI uploaded and verified only for `0.9.0rc6.dev0`.
- TestPyPI upload for `0.9.0rc8.dev0` has not been performed.
- External solvers are not run by default.
- External LLMs are not called by default.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
- Elmer remains Level 2 + Level-3-ready, install deferred.

## Classification

| Area | Classification | Current evidence | rc8 backend direction |
| --- | --- | --- | --- |
| Sub-agent reality | Done / stable enough | `scripts/audit_sub_agents.py`, deterministic traces, backend evidence pack | Keep honest role-vs-class reporting and ensure sessions keep all eight roles visible. |
| Tool-call ledger | Done / stable enough | Agent task sessions record internal tools, blocked external actions, calculators, source/monitor diagnostics | Add regression cases when new backend tools are introduced. |
| Material library | Done / stable enough | Local preview catalog, suggestions, API fixtures, docs | Harden provenance notes and example coverage, but keep values preview/design-assist. |
| Optical calculators | Needs backend hardening | Thin-film, paraxial, Gaussian beam, waveguide calculators with reference sanity cases | Expand reference cases, invalid-input diagnostics, and domain-specific result summaries before any production claim is considered. |
| Source/monitor diagnostics | Done / stable enough | Source/monitor inference, missing-input diagnostics, API fixtures | Add more ambiguous-goal fixtures and source/monitor defaults for new design templates. |
| Observable diagnostics | Done / stable enough | Observable taxonomy and diagnostics for scattering, reflectance, fields, band, focal, and mesh observables | Add richer required-input diagnostics for multi-observable cases. |
| Adapter-native mappings | Needs backend hardening | Meep, MPB, Gmsh, Elmer, Optiland preview mappings and metadata | Improve native metadata completeness and keep real-result requirements explicit. |
| Adapter golden coverage | Done / stable enough | Golden cases, strict metadata diffs, coverage API/report | Add new golden cases when adapter preview semantics change. |
| Design requirement templates | Done / stable enough | Seven templates with EN/ZH goals, expected tools, and deterministic matching | Add requirement variants for tolerances, constraints, and missing-input question generation. |
| Natural-language to optical-language matching | Needs backend hardening | Deterministic heuristic matching, source/monitor inference, diagnostics | Broaden bilingual keyword coverage and add low-confidence fallback examples. |
| Frontend Agent Studio | Deferred / non-blocker | Local MVP, Command Center, Example Gallery, Agent Trace Timeline | Do not add UI in rc8 backend hardening unless maintainers explicitly reprioritize frontend evidence display. |
| PyPI publication | Deferred / non-blocker | PyPI decision docs and checklist | Decide separately after explicit maintainer approval; rc8.dev0 does not imply publication. |
| v1.0.0 release criteria | Needs backend hardening | Public contract freeze approved, scorecard and criteria docs exist | Keep API/CLI/schema contract stable and close backend evidence gaps before planning v1.0.0. |
| Elmer Level 3 | Deferred / non-blocker | Elmer Level 2 + Level-3-ready docs, install deferred record | Revisit only when a maintainable ElmerSolver install route exists. |

## Done / Stable Enough

- Backend evidence review pack summarizes current backend reality in one place.
- Sub-agent roles are visible in deterministic traces and audit output.
- Tool-call ledger records executed internal tools and blocked external actions.
- Material library is local, deterministic, and explicitly preview-only.
- Optical design examples and design requirement templates connect goals to
  materials, geometry, adapters, calculators, artifacts, and evidence.
- Source/monitor inference, observable diagnostics, adapter-native mappings,
  and adapter golden metadata checks are present and covered by tests.

## Needs Backend Hardening

- Add more reference cases for calculators, especially layered lossy thin-film
  examples, Gaussian focusing edge cases, and waveguide boundary cases.
- Plan optional solver-backed micro-benchmarks through
  [`solver_validation_micro_benchmarks.md`](solver_validation_micro_benchmarks.md)
  without adding solvers to default pytest, smoke, quality gates, or release
  gates.
- Review the approved Gmsh-only 2026-05-20 optional micro-benchmark evidence
  before considering any separately approved Meep, MPB, Optiland, or Elmer run.
- Record that the Gmsh review accepted the evidence only as optional manual
  mesh-generation smoke evidence; Optiland is a next candidate only, not an
  approved run.
- Improve missing-input diagnostics for goals with multiple possible observables.
- Add structured material provenance fields for every preview material entry.
- Expand deterministic natural-language matching for bilingual and terse goals.
- Add backend regression tests that compare design requirement templates to
  expected tool-call ledger entries.
- Keep backend capability reports stable as API fixtures evolve.

## Deferred / Non-blocker

- PyPI publication and TestPyPI upload for `0.9.0rc8.dev0`.
- `v0.9.0rc8` tag creation and GitHub prerelease creation.
- Frontend display of backend evidence review data.
- Elmer Level 3 validation.
- Optional external solver execution.
- Optional solver-backed micro-benchmark execution unless explicitly approved
  through `OSA_RUN_OPTIONAL_*_VALIDATION=1`.
- Optional external LLM integration.

## Future / Phase 2

- Async task sessions and persisted backend run history.
- Larger optical design benchmark corpus.
- Optional solver execution adapters with explicit approval gates.
- More formal material provenance and user-supplied material datasets.
- Frontend presentation of backend evidence only after backend contracts remain
  stable.

## Not a Goal

- Production-grade physical validation.
- Formal convergence proof.
- Default proprietary solver dependency.
- Default external solver execution.
- Default external LLM calls.
- PyPI/TestPyPI upload without explicit maintainer approval.
- Tag or GitHub release creation without explicit maintainer approval.

## Validation Maturity Track

The rc8 backend roadmap now uses
[`backend_validation_maturity_matrix.md`](backend_validation_maturity_matrix.md)
and [`preview_boundary_policy.md`](preview_boundary_policy.md) as the shared
boundary for future hardening. Any future rc8/PyPI/v1.0 decision should keep the
calculator, material, adapter, application-domain, and frontend evidence levels
separate from physical validation claims.

Optional solver-backed validation planning is tracked separately in
[`solver_validation_micro_benchmarks.md`](solver_validation_micro_benchmarks.md)
and `validation/solver_validation_micro_benchmarks.json`. It is manual,
explicit opt-in only, keeps Elmer deferred, and does not change the default
no-solver release path.
The approval/readiness layer is tracked in
[`optional_solver_micro_benchmark_approval_matrix.md`](optional_solver_micro_benchmark_approval_matrix.md),
[`optional_solver_micro_benchmark_approval_record_template.md`](optional_solver_micro_benchmark_approval_record_template.md),
[`optional_solver_micro_benchmark_execution_packet.md`](optional_solver_micro_benchmark_execution_packet.md),
[`optional_solver_execution_sequence.md`](optional_solver_execution_sequence.md), and
[`optional_solver_micro_benchmark_readiness_status.md`](optional_solver_micro_benchmark_readiness_status.md);
it is still default no-execution and does not authorize PyPI/TestPyPI upload,
tag creation, or release creation.
Readiness is now environment-aware through
[`optional_solver_environment_profiles.md`](optional_solver_environment_profiles.md):
the default profile uses current Python/current `PATH`, while
`OSA_SOLVER_PYTHON` can probe a dedicated solver Python such as `osa-solvers`
for PyMeep and `meep.mpb` without running any solver benchmark.
The Gmsh review decision is recorded in
[`optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md`](optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md)
and does not authorize PyPI/TestPyPI upload, tag/release creation, Optiland,
Meep, MPB, Elmer, or future Gmsh reruns.
