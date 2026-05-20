# Backend Evidence Review Pack

The backend evidence review pack is a maintainer-facing summary of what the
local backend actually proves today. It is a preview/design-assist review
artifact. It is not production-grade physical validation, does not claim a
formal convergence proof, and does not execute external solvers.

## Generate the Pack

```bash
python scripts/generate_backend_evidence_pack.py \
  --json-out /tmp/osa-backend-evidence-pack.json \
  --markdown-out /tmp/osa-backend-evidence-pack.md
```

The generated `/tmp` files are review artifacts and should not be committed by
default.

## Smoke Check

```bash
./scripts/smoke_backend_evidence_pack.sh
```

The smoke script verifies that the generated JSON and Markdown include the
expected sections and safety markers.

## Review Decision

The maintained review decision is recorded in
[`backend_evidence_review_decision.md`](backend_evidence_review_decision.md).
That decision records backend evidence as sufficient to prepare a
`v0.9.0rc7` release draft. Maintainers later approved and completed the
`v0.9.0rc7` GitHub prerelease, while PyPI publication, TestPyPI upload for
`0.9.0rc8.dev0`, future `v0.9.0rc8` tag/release work, and `v1.0.0` release
approval remain separate and not granted.

## Sections

- Package and release status: current public prerelease, main development
  version, PyPI/TestPyPI state, and no tag/release actions.
- Sub-agent reality: whether each deterministic backend role exists and runs in
  a sample session.
- Tool-call reality: internal tools executed, calculator tools executed, and
  blocked external actions.
- Optical calculators: thin-film, paraxial, Gaussian beam, waveguide, fiber
  coupling, and polarization preview calculators with sanity reference cases
  and failure modes. Fiber coupling covers perfect match, waist mismatch,
  offset loss, and tilt loss; polarization covers linear states, Malus-like
  polarizer projection, half-wave rotation, and quarter-wave phase.
- Material provenance coverage: starter materials expose provenance fields,
  require user verification, and remain non-production optical constants.
- Ambiguous requirement matching: deterministic confidence, candidate template,
  and question generation for under-specified goals.
- Missing-input diagnostics: critical and optional missing inputs, defaults,
  blocking questions, and `safe_to_run_solver=false`.
- Application-domain coverage: ten local optical domains mapped to materials,
  templates, calculators/adapters, and missing-input questions.
- Material-template cross-checks: pass/warning/fail checks for domain material,
  template, expected tool, and preview-only evidence coverage.
- Application-domain benchmarks: positive, ambiguous, underconstrained,
  unsupported, and unsafe/blocked scenarios evaluated against expected matching,
  tool-call, missing-input, and safety behavior. The previous fiber coupling
  and polarization warning cases are now covered by deterministic preview
  calculators.
- Optional solver micro-benchmarks: a manifest-backed plan for tiny open-source
  solver-backed checks that remain manual and explicit opt-in only. Default
  evidence pack generation does not run solvers. The approved Gmsh-only
  2026-05-20 run is reviewed and accepted as optional manual mesh-generation
  smoke evidence only. The separately approved Optiland-only 2026-05-20 run
  is reviewed and accepted only as optional manual ray/path smoke evidence.
- Optional solver readiness/approval: availability detection, expected
  artifacts, risk notes, and explicit approval phrase are documented before any
  solver-backed micro-benchmark can be run. The execution approval packet,
  one-solver-at-a-time sequence, the reviewed Gmsh-only, Optiland-only, and
  Meep-only records, and pending/deferred records for
  other solvers are review aids only.
  This does not authorize PyPI, TestPyPI, tag, release, or other solver
  execution actions. The Meep and MPB runs used `OSA_SOLVER_PYTHON`; Elmer
  remains deferred. The
  Meep decision packet at
  `docs/optional_solver_approval_records/meep_micro_benchmark_decision_packet.md`
  records the `OSA_SOLVER_PYTHON` path and required approval phrase for the
  approved Meep-only smoke run. The Meep review record
  `docs/optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md`
  accepts the result only as optional manual PyMeep/FDTD smoke evidence and
  does not authorize future Meep reruns.
  The MPB decision packet at
  `docs/optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md`
  records the required `OSA_SOLVER_PYTHON` profile, `meep.mpb` import-only
  readiness path, approved command, artifacts, cleanup, and non-claims for the
  approved MPB-only run. The MPB evidence is recorded as optional manual
  MPB/band-structure smoke evidence only and does not authorize future MPB
  reruns.
- Design-case cross-checks: optical design examples mapped to expected
  calculators, adapters, and tool-call ledger entries.
- Source / monitor / observable diagnostics: deterministic inference,
  missing-input diagnostics, observable taxonomy, and adapter-native mapping.
- Adapter-native golden coverage: Meep, MPB, Gmsh, Elmer, and Optiland golden
  preview cases with metadata, fragment, and safety checks.
- Blocked or deferred capabilities: external solver execution, external LLM,
  publication, tag/release, Elmer Level 3, production-grade validation, and
  formal convergence proof.
- Maintainer review questions: prompts for deciding what to review or deepen
  next.

## Interpreting Status

`pass` means the local deterministic evidence matched the expected preview
contract. `warn` means a capability is intentionally partial or deferred. `fail`
means a local evidence check did not match the expected contract.

## Limitations

- No external solver is executed by default.
- Optional solver-backed micro-benchmarks require explicit
  `OSA_RUN_OPTIONAL_*_VALIDATION=1` approval and are not default gates.
- Optional solver readiness uses `scripts/check_optional_solver_readiness.py`
  and the approval matrix/template; it performs no solver execution.
  `OSA_SOLVER_PYTHON` can calibrate import-only probes for a dedicated solver
  Python environment such as `osa-solvers`. The approved Meep-only
  micro-benchmark used that profile support, but default checks still do not
  execute Meep or MPB.
- No external LLM is called by default.
- No TestPyPI/PyPI upload is performed.
- No Git tag or GitHub release is created.
- Adapter-native monitor metadata is preview-only and is not a real solver
  monitor result.
- Calculator outputs are sanity-checked preview/design-assist results, not
  production-grade physical validation.

## Validation Maturity and Preview Boundaries

The generated evidence pack now includes:

- `validation_maturity_summary`: conservative levels for calculators,
  materials, application domains, adapter metadata, sub-agent sessions, and the
  frontend UI/demo surface.
- `preview_boundary_summary`: plain-language reminders of what each evidence
  area proves and what users must verify independently.
- `validation_claim_audit_available`: records that
  `scripts/audit_validation_claims.py` is part of the backend evidence
  workflow.
- `optional_solver_micro_benchmarks`: includes readiness/approval matrix
  availability, default no-execution status, and explicit approval requirement.

See [`backend_validation_maturity_matrix.md`](backend_validation_maturity_matrix.md)
and [`preview_boundary_policy.md`](preview_boundary_policy.md).
