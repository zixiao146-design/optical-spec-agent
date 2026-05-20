# Backend Functionality Status

Current public prerelease: v0.9.0rc8. Current main development version:
`0.9.0rc9.dev0`.

This document records what the backend can actually import, call, execute, or
block.

The generated backend capability report now provides the same reality check in
machine-readable and Markdown form:

```bash
python scripts/generate_backend_capability_report.py \
  --json-out /tmp/osa-backend-capability-report.json \
  --markdown-out /tmp/osa-backend-capability-report.md
./scripts/smoke_backend_report.sh
```

The live API surfaces are `GET /api/backend-capability-report` and
`GET /api/design-case-cross-checks`. Requirement templates are exposed through
`GET /api/design-requirements`, `GET /api/design-requirements/{template_id}`,
and `POST /api/design-requirements/match`.
For maintainer review, `scripts/generate_backend_evidence_pack.py`,
`./scripts/smoke_backend_evidence_pack.sh`, and
`GET /api/backend-evidence-summary` collect the same backend evidence into one
preview/design-assist review package.

Post-`v0.9.0rc8` backend planning is tracked in:

- `docs/rc8_backend_roadmap.md`
- `docs/rc8_capability_gap_audit.md`
- `docs/rc8_to_v1_0_decision_path.md`

Those documents identify what is stable enough, what needs backend hardening,
what is deferred, and what is not a goal before any future rc9, PyPI, or v1.0.0
decision.

## Installed / Callable / Executed

| Capability | Installed/importable | Callable | Executed in backend smoke |
| --- | --- | --- | --- |
| Design requirement templates | yes | yes | yes |
| Natural-language goal matching | yes | yes | yes |
| Ambiguous requirement matching | yes | yes | yes |
| Missing-input critical/optional diagnostics | yes | yes | yes |
| Material library | yes | yes | yes |
| Material provenance coverage | yes | yes | yes |
| Material suitability diagnostics | yes | yes | yes |
| Optical design example registry | yes | yes | yes |
| Agent trace builder | yes | yes | yes |
| Agent task session builder | yes | yes | yes |
| Tool-call ledger | yes | yes | yes |
| Application-domain benchmark scenarios | yes | yes | yes |
| Source/monitor inference | yes | yes | yes |
| Source/monitor missing-input diagnostics | yes | yes | yes |
| Observable diagnostics | yes | yes | yes |
| Adapter-native source/monitor mapping | yes | yes | yes |
| Adapter-native golden preview checker | yes | yes | yes |
| Adapter-native golden coverage report | yes | yes | yes |
| Thin-film preview calculator | yes | yes | yes |
| Thin-film spectrum / quarter-wave AR helper | yes | yes | yes |
| Paraxial lens preview calculator | yes | yes | yes |
| Paraxial system / two-lens relay helper | yes | yes | yes |
| Gaussian beam preview calculator | yes | yes | yes |
| Gaussian beam series / focus helper | yes | yes | yes |
| Waveguide V-number preview calculator | yes | yes | yes |
| Waveguide sweep / single-mode range helper | yes | yes | yes |
| Fiber coupling Gaussian mode-overlap preview calculator | yes | yes | yes |
| Polarization Jones-calculus preview calculator | yes | yes | yes |
| Backend capability report generator | yes | yes | yes |
| Backend evidence review pack generator | yes | yes | yes |
| Design case cross-check module | yes | yes | yes |

## Case Integration

Agent task sessions now attach calculator result summaries where applicable:

- `thin_film_coating` records thin-film spectrum and quarter-wave AR helpers.
- `waveguide_mode` records waveguide V-number sweep and single-mode range helpers.
- `lens_raytrace_preview` records a paraxial two-lens relay helper.
- Gaussian beam goals record propagation series and thin-lens focus helpers.
- Fiber coupling goals record a scalar Gaussian mode-overlap helper.
- Polarization optics goals record ideal Jones polarizer/waveplate helpers.

These calls are internal Python design-assist calculations and are recorded in
`tool_call_ledger`; external solvers remain unexecuted.

`docs/design_case_cross_checks.md` records the current example-to-calculator
mapping and pass/warning/fail semantics. The bundled cases currently cross-check
as local preview/design-assist workflows, not production-grade validation.

Calculator responses now expose `quality`, `warnings`, `assumptions`, and
`limitations`. Formula-level reference cases are documented in
`docs/optical_calculator_reference_cases.md` and
`docs/fiber_polarization_reference_cases.md`; they are sanity checks, not
production-grade validation.

## Sub-agent Reality

The current sub-agents are deterministic backend roles, not separate installed
autonomous packages. `scripts/audit_sub_agents.py` reports this honestly:
role names are present in traces, callable backend functions exist, but
importable `SpecAgent` / `MaterialAgent` / similar classes are not currently
installed as standalone classes.

## External Solvers

External solvers are not run by default. `/api/tool-capabilities` may detect
whether Meep, Gmsh, MPB, ElmerSolver, or Optiland appear importable or on PATH,
but detection is not execution. Elmer remains Level 2 + Level-3-ready with
install deferred.
The approved Gmsh-only optional micro-benchmark passed on 2026-05-20 and is
reviewed as accepted optional manual mesh-generation smoke evidence, not
optical correctness evidence. That review does not approve Optiland, Meep, MPB,
Elmer, or any future Gmsh rerun.
The separately approved Optiland-only optional micro-benchmark also passed on
2026-05-20 and is reviewed as accepted optional manual ray/path smoke evidence,
not production lens design validation. The separately approved Meep-only
optional micro-benchmark passed on 2026-05-20 using `OSA_SOLVER_PYTHON` and is
reviewed as accepted optional manual PyMeep/FDTD smoke evidence, not production
FDTD validation. The separately approved MPB-only optional micro-benchmark
passed on 2026-05-20 using `OSA_SOLVER_PYTHON` and `meep.mpb` and is reviewed
as accepted optional manual MPB/band-structure smoke evidence.
Elmer remains unexecuted by these tasks.
The Meep record does not authorize MPB, uploads, tags, releases, or future Meep
reruns.
The MPB decision packet now documents the required `OSA_SOLVER_PYTHON` profile,
`meep.mpb` import-only readiness path, expected artifacts, and approval phrase,
but it does not authorize future MPB reruns.
The consolidated optional solver evidence summary is now recorded in
`docs/optional_solver_evidence_summary.md`, the rc8 backend readiness review in
`docs/rc8_backend_readiness_review.md`, and the solver evidence maturity mapping
in `docs/solver_evidence_validation_maturity_mapping.md`. These documents close
the reviewed optional evidence loop for Gmsh, Optiland, Meep, and MPB while
keeping Elmer deferred, default gates no-execute, and all PyPI/TestPyPI,
tag/release, production validation, convergence, and optical-correctness
decisions separately gated.

## Publication / Release Actions

The backend does not expose TestPyPI upload, PyPI publication, git tag creation,
or GitHub release creation endpoints. PyPI remains unpublished, and publication
approval remains not granted.
The `v0.9.0rc8` GitHub prerelease has been created and the `v0.9.0rc9` tag has
not been created, `v1.0.0` has not been released, and `0.9.0rc9.dev0` is not a
public release.

## Current Gap Audit

`docs/rc8_capability_gap_audit.md` identified calculator depth, material
provenance, ambiguous natural-language matching, metadata-only adapter-native
mapping evidence, and Elmer Level 3 deferral as the main backend gaps to review
before future rc8 or v1.0 decisions. rc8 now has structured material
provenance fields, `POST /api/materials/diagnose`, ambiguous/negative
requirement examples, candidate-template matching, recommended questions, and
critical/optional missing-input diagnostics. These additions reduce the audit
gap but remain preview/design-assist evidence, not production validation.

## Verification

Use:

```bash
python scripts/audit_sub_agents.py
./scripts/smoke_backend_capabilities.sh
./scripts/smoke_backend_report.sh
./scripts/smoke_backend_evidence_pack.sh
python scripts/evaluate_application_domain_benchmarks.py
```

Backend source/monitor functionality is implemented as local Python helpers:

- `optical_language.infer_source_monitor`
- `optical_language.diagnose_missing_inputs`
- `optical_language.diagnose_observable`
- `optical_language.map_source_monitor_to_adapter`

These helpers are included in backend capability reports and agent-session
tool-call ledgers. They infer preview source/monitor metadata and report
missing inputs, observable requirements, and adapter-native preview semantics
without running solvers or calling external LLMs.

Adapter-native golden preview cases are stored under
`examples/adapter_native_golden/` and checked by
`python scripts/check_adapter_native_golden.py`. They verify Meep, MPB, Gmsh,
Elmer, and Optiland source/monitor/observable fragments plus strict
`expected_metadata.json` diffs against live local API responses. The coverage
matrix is exposed through `GET /api/adapter-native-golden-coverage` and the
`adapter_native_golden_coverage` section of the backend capability report.

Both scripts are local-only and print:

- NO SOLVER EXECUTION PERFORMED
- NO EXTERNAL LLM CALLED
- NO UPLOAD PERFORMED
- NO TAG CREATED
- NO RELEASE CREATED

## Application Domain Coverage

The rc8 backend now includes `GET /api/application-domains`,
`POST /api/application-domains/match`, and `GET /api/application-domain-cross-checks`.
These local-only endpoints connect ten preview domains to material suitability,
requirement templates, expected calculators/adapters, missing-input questions,
and deferred capability notes. They do not execute solvers, call external LLMs,
or claim production-grade physical validation.

Fiber coupling and polarization optics now close the former benchmark warning
cases with deterministic preview calculators. The fiber coupling helper
estimates scalar Gaussian mode overlap and the polarization helper applies
ideal Jones-calculus elements. These are still preview/design-assist tools; real
coupling validation, vector EM propagation, device fabrication effects, and
measured performance require explicit solver or experimental evidence.

The same domain registry is benchmarked through
`examples/application_domain_benchmarks/`,
`python scripts/evaluate_application_domain_benchmarks.py`,
`GET /api/application-domain-benchmarks`,
`POST /api/application-domain-benchmarks/{scenario_id}/evaluate`, and
`GET /api/application-domain-benchmark-results`. The benchmark suite checks
positive, ambiguous, underconstrained, unsupported, and unsafe/blocked scenario
behavior without solver execution or external LLM calls.

## Validation Maturity Boundary

Backend status is now consolidated in
[`backend_validation_maturity_matrix.md`](backend_validation_maturity_matrix.md)
and [`preview_boundary_policy.md`](preview_boundary_policy.md). In short:

- calculators are `sanity_checked_preview`;
- application-domain scenarios are `benchmark_checked_preview`;
- adapter/source-monitor mappings and golden coverage are fixture-guarded
  preview metadata;
- the material library remains local preview data that users must verify;
- frontend Agent Studio is a UI/demo surface, not validation evidence.

`scripts/audit_validation_claims.py` checks docs, source, tests, examples, and
README files for unsafe validation overclaims before future release-draft work.

Optional solver execution readiness is now separated from execution:
`scripts/check_optional_solver_readiness.py` performs availability detection
only, while
[`optional_solver_micro_benchmark_approval_matrix.md`](optional_solver_micro_benchmark_approval_matrix.md)
and
[`optional_solver_micro_benchmark_approval_record_template.md`](optional_solver_micro_benchmark_approval_record_template.md)
record expected artifacts, risks, and the explicit approval phrase. Default
backend checks still do not execute solvers, upload packages, create tags, or
create releases.
The execution approval packet, per-solver approval records, and
one-solver-at-a-time sequence are prepared as future review aids only; all
execution remains unauthorized until explicit solver-specific approval is
recorded.
The Gmsh review decision closes only the already approved Gmsh run. The
Optiland review decision closes only the separately approved Optiland run.
The Meep review decision closes only the separately approved Meep run. The MPB
review decision closes only the separately approved MPB run; Elmer remains
deferred. The MPB-specific decision packet and review record do not authorize
future MPB reruns, uploads, tags, releases, or any production validation claim.
The Meep-specific decision packet records the approval phrase and expected
artifacts for the approved smoke run, but it does not authorize future Meep
reruns.
Readiness is calibrated by environment profile: current Python/current `PATH`
is the default, while `OSA_SOLVER_PYTHON` can probe a dedicated solver Python
such as `osa-solvers` for PyMeep and `meep.mpb`; see
[`optional_solver_environment_profiles.md`](optional_solver_environment_profiles.md).
