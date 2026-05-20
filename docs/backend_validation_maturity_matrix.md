# Backend Validation Maturity Matrix

This matrix consolidates backend evidence levels for `0.9.0rc8.dev0`.
It is a conservative maintainer view: every row is preview/design-assist
evidence, no production-grade physical validation is claimed, and no formal
convergence proof is claimed.

## Maturity Levels

| Level | Meaning |
| --- | --- |
| `documented_preview` | Behavior and limitations are documented, but the evidence is not a physical validation result. |
| `fixture_guarded_preview` | Stable fixtures, API shapes, or metadata-diff checks guard the behavior. |
| `sanity_checked_preview` | Local analytic calculators have reference sanity cases and failure-mode tests. |
| `benchmark_checked_preview` | Deterministic scenario benchmarks check routing, diagnostics, missing inputs, and blocked actions. |
| `optional_manual_solver_validated` | Manual solver validation may exist for selected adapters, but external solvers are not run by default. |
| `production_grade_not_claimed` | Explicit boundary marker: production-grade validation is outside current claims. |

## Current Matrix

| Area | Component | Current level | Evidence | Limitation |
| --- | --- | --- | --- | --- |
| Materials | material library | `documented_preview` | material provenance docs and tests | User must verify constants; not a production-grade optical constants database. |
| Requirements | design requirement templates | `fixture_guarded_preview` | requirement fixtures and matching tests | Heuristic matching only; ambiguous goals generate questions. |
| Requirements | natural-language to optical-language | `fixture_guarded_preview` | ambiguous matching and missing-input tests | No external LLM by default; confidence is routing evidence. |
| Calculators | thin-film | `sanity_checked_preview` | single-interface and quarter-wave AR reference cases | Transfer-matrix preview only. |
| Calculators | paraxial | `sanity_checked_preview` | thin-lens, ABCD, and relay reference cases | First-order optics only. |
| Calculators | Gaussian beam | `sanity_checked_preview` | Rayleigh range and beam-radius reference cases | Scalar paraxial model only. |
| Calculators | waveguide | `sanity_checked_preview` | V-number and sweep reference cases | Slab-waveguide approximation only. |
| Calculators | fiber coupling | `sanity_checked_preview` | Gaussian overlap reference cases | Scalar Gaussian mode-overlap approximation only. |
| Calculators | polarization | `sanity_checked_preview` | Jones polarizer and waveplate reference cases | Jones-calculus preview only. |
| Optical language | source/monitor diagnostics | `fixture_guarded_preview` | source/monitor inference fixtures and tests | Monitor records are preview metadata. |
| Optical language | observable diagnostics | `fixture_guarded_preview` | observable taxonomy fixtures and tests | Observable fit is not a computed physical result. |
| Adapters | adapter-native source/monitor mapping | `fixture_guarded_preview` | adapter mapping fixtures and tests | Real adapter results require explicit solver execution. |
| Adapters | adapter golden coverage | `fixture_guarded_preview` | golden cases and strict metadata diff | Metadata checks are not solver monitor outputs. |
| Optional solver validation | Gmsh/Meep/MPB/Optiland micro-benchmark plan | `optional_manual_solver_validated` for recorded pilots | `validation/solver_validation_micro_benchmarks.json`, existing 2026-05-14 manual reports, the approved Gmsh-only, Optiland-only, and Meep-only 2026-05-20 evidence records, the Gmsh, Optiland, and Meep review decisions, the Meep decision packet, and `scripts/run_optional_solver_micro_benchmarks.sh` | Explicit opt-in only; default pytest, smoke, release gates, and quality gates do not run solvers. Gmsh evidence is accepted only as mesh-generation smoke, Optiland evidence only as ray/path smoke, and Meep evidence only as PyMeep/FDTD smoke; none proves optical correctness. MPB remains not executed. |
| Optional solver validation | Elmer micro-benchmark plan | `documented_preview` / deferred | `validation/elmer/elmer_install_deferred_2026-05-15.md` and Elmer optional pilot docs | Elmer remains Level 2 + Level-3-ready; Level 3 is not claimed. |
| Application domains | domain benchmarks | `benchmark_checked_preview` | 19 pass / 0 warn / 0 fail scenario suite | Benchmarks test deterministic behavior, not physical correctness. |
| Agents | sub-agent task sessions | `fixture_guarded_preview` | audit script and tool-call ledger tests | Roles are deterministic local backend roles. |
| Agents | tool-call ledger | `fixture_guarded_preview` | ledger tests and evidence pack | Ledger shows local tool calls and blocked external actions. |
| Frontend | Agent Studio | `documented_preview` | UI smoke and docs | UI/demo surface only, not validation evidence. |

## What Is Not Claimed

- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
- No real solver monitor result is claimed by default.
- No external solver execution is performed by default.
- Optional solver-backed micro-benchmarks require explicit opt-in environment
  variables and are not part of default pytest, smoke, quality gates, or release
  gates.
- Optional solver readiness is now reviewable through
  [`optional_solver_micro_benchmark_approval_matrix.md`](optional_solver_micro_benchmark_approval_matrix.md),
  [`optional_solver_micro_benchmark_approval_record_template.md`](optional_solver_micro_benchmark_approval_record_template.md),
  [`optional_solver_micro_benchmark_execution_packet.md`](optional_solver_micro_benchmark_execution_packet.md),
  [`optional_solver_execution_sequence.md`](optional_solver_execution_sequence.md),
  and `scripts/check_optional_solver_readiness.py`; this readiness layer still
  performs no solver execution by default.
- Solver readiness is profile/environment-specific. `OSA_SOLVER_PYTHON` can
  point import probes at a dedicated solver Python such as `osa-solvers`, while
  CLI tools such as Gmsh are detected from the current `PATH`; see
  [`optional_solver_environment_profiles.md`](optional_solver_environment_profiles.md).
- The Gmsh review record
  [`optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md`](optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md)
  accepts only optional manual mesh-generation smoke evidence. The separately
  reviewed Optiland evidence
  [`../validation/optiland/optiland_micro_benchmark_2026-05-20.md`](../validation/optiland/optiland_micro_benchmark_2026-05-20.md)
  is only optional manual ray/path smoke evidence. The separately approved and
  reviewed Meep
  evidence
  [`../validation/meep/meep_micro_benchmark_2026-05-20.md`](../validation/meep/meep_micro_benchmark_2026-05-20.md)
  is only optional manual PyMeep/FDTD smoke evidence. MPB requires
  `OSA_SOLVER_PYTHON` and separate approval. The Meep decision packet
  [`optional_solver_approval_records/meep_micro_benchmark_decision_packet.md`](optional_solver_approval_records/meep_micro_benchmark_decision_packet.md)
  and review record
  [`optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md`](optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md)
  document the approved Meep-only path, accepted smoke-evidence scope, and
  non-claims.
- No external LLM is required by default.
- Elmer remains Level 2 + Level-3-ready; Level 3 is deferred.

Run:

```bash
python scripts/audit_validation_claims.py
```

The audit blocks unsafe claim language while allowing explicit negated forms.
