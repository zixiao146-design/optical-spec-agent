# Backend Functionality Status

Current public prerelease: v0.9.0rc7. Current main development version:
`0.9.0rc8.dev0`.

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

Post-`v0.9.0rc7` backend planning is tracked in:

- `docs/rc8_backend_roadmap.md`
- `docs/rc8_capability_gap_audit.md`
- `docs/rc8_to_v1_0_decision_path.md`

Those documents identify what is stable enough, what needs backend hardening,
what is deferred, and what is not a goal before any future rc8, PyPI, or v1.0.0
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
| Backend capability report generator | yes | yes | yes |
| Backend evidence review pack generator | yes | yes | yes |
| Design case cross-check module | yes | yes | yes |

## Case Integration

Agent task sessions now attach calculator result summaries where applicable:

- `thin_film_coating` records thin-film spectrum and quarter-wave AR helpers.
- `waveguide_mode` records waveguide V-number sweep and single-mode range helpers.
- `lens_raytrace_preview` records a paraxial two-lens relay helper.
- Gaussian beam goals record propagation series and thin-lens focus helpers.

These calls are internal Python design-assist calculations and are recorded in
`tool_call_ledger`; external solvers remain unexecuted.

`docs/design_case_cross_checks.md` records the current example-to-calculator
mapping and pass/warning/fail semantics. The bundled cases currently cross-check
as local preview/design-assist workflows, not production-grade validation.

Calculator responses now expose `quality`, `warnings`, `assumptions`, and
`limitations`. Formula-level reference cases are documented in
`docs/optical_calculator_reference_cases.md`; they are sanity checks, not
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

## Publication / Release Actions

The backend does not expose TestPyPI upload, PyPI publication, git tag creation,
or GitHub release creation endpoints. PyPI remains unpublished, and publication
approval remains not granted.
The `v0.9.0rc8` tag has not been created, `v1.0.0` has not been released, and
`0.9.0rc8.dev0` is not a public release.

## Current Gap Audit

`docs/rc8_capability_gap_audit.md` identified calculator depth, material
provenance, ambiguous natural-language matching, metadata-only adapter-native
mapping evidence, and Elmer Level 3 deferral as the main backend gaps to review
before future rc8 or v1.0 decisions. rc8.dev0 now has structured material
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

The rc8.dev0 backend now includes `GET /api/application-domains`,
`POST /api/application-domains/match`, and `GET /api/application-domain-cross-checks`.
These local-only endpoints connect ten preview domains to material suitability,
requirement templates, expected calculators/adapters, missing-input questions,
and deferred capability notes. They do not execute solvers, call external LLMs,
or claim production-grade physical validation.

The same domain registry is benchmarked through
`examples/application_domain_benchmarks/`,
`python scripts/evaluate_application_domain_benchmarks.py`,
`GET /api/application-domain-benchmarks`,
`POST /api/application-domain-benchmarks/{scenario_id}/evaluate`, and
`GET /api/application-domain-benchmark-results`. The benchmark suite checks
positive, ambiguous, underconstrained, unsupported, and unsafe/blocked scenario
behavior without solver execution or external LLM calls.
