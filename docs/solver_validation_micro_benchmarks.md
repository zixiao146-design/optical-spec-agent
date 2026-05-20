# Optional Solver-backed Validation Micro-benchmarks

## Purpose

These micro-benchmarks define an optional, manual, explicit opt-in path for
checking tiny open-source solver execution paths from local adapter previews.
They are intended to validate the narrow chain from preview artifact generation
to a minimal open-source solver run when a maintainer explicitly asks for it.

They are not default release gates, not default quality gates, and not default
pytest behavior. They do not claim production-grade physical validation, formal
convergence proof, or real optical-design correctness.

## Current Default

- Default pytest does not run external solvers.
- pytest does not run solvers by default.
- Default smoke scripts do not run external solvers.
- Default quality gates do not run external solvers.
- Default release gates do not run external solvers.
- Missing solvers are non-blocking in default checks.
- Elmer remains deferred until a maintainable install route exists.

## Candidate Micro-benchmarks

| Solver | Candidate benchmark | Expected artifact | Boundary |
| --- | --- | --- | --- |
| Gmsh | Tiny mesh generation from a local `.geo` preview | `.msh` | Executed/passed on 2026-05-20 for the approved Gmsh-only run; validates syntax/path only, not optical correctness. |
| Meep | Tiny PyMeep smoke from a generated preview artifact | result JSON | Validates import/run path only, not production-grade FDTD. |
| MPB | Tiny band-structure smoke through `meep.mpb` | band summary JSON | Validates MPB Python path only. |
| Optiland | Tiny ray-trace or import/run smoke | result JSON | Executed/passed on 2026-05-20 for the approved Optiland-only run; review accepted it as optional manual ray/path smoke evidence only, not lens design correctness. |
| Elmer | Deferred until maintainable `ElmerSolver` install exists | deferred report | No Level 3 validation is claimed. |

The 2026-05-20 Gmsh result has been reviewed and accepted only as optional
manual mesh-generation smoke evidence. It does not authorize any further solver
execution and does not change default test, quality gate, or release gate
behavior. A separate 2026-05-20 Optiland-only run was approved, passed, and
reviewed as optional manual ray/path smoke evidence. Meep and MPB require
`OSA_SOLVER_PYTHON` plus separate approval; Elmer remains deferred. No future
Gmsh or Optiland rerun is approved by these records.

## Required Approval

Solver-backed runs require explicit opt-in environment variables. Do not set
these in default CI, default smoke, release gates, or quality gates:

- `OSA_RUN_OPTIONAL_GMSH_VALIDATION=1`
- `OSA_RUN_OPTIONAL_MEEP_VALIDATION=1`
- `OSA_RUN_OPTIONAL_MPB_VALIDATION=1`
- `OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1`

Elmer remains deferred. `OSA_RUN_OPTIONAL_ELMER_VALIDATION=1` is documented for
the existing pilot script, but this micro-benchmark plan does not promote Elmer
to Level 3.

The unified wrapper is:

```bash
./scripts/run_optional_solver_micro_benchmarks.sh
```

By default it prints the manifest summary, writes an optional JSON report when
`OSA_SOLVER_MICRO_BENCHMARK_REPORT` is set, and performs no solver execution.

Before any opt-in run, review the
[`optional_solver_micro_benchmark_approval_matrix.md`](optional_solver_micro_benchmark_approval_matrix.md)
readiness matrix and fill the
[`optional_solver_micro_benchmark_approval_record_template.md`](optional_solver_micro_benchmark_approval_record_template.md)
for the selected solver. The no-execution readiness check is:

```bash
python scripts/check_optional_solver_readiness.py
```

That script performs availability detection only; it does not run solver
binaries or solver examples. Readiness is environment-specific: by default it
uses the current Python and current `PATH`, while `OSA_SOLVER_PYTHON` can point
Python import probes at a solver-specific interpreter such as a maintainer-local
`osa-solvers` conda environment:

```bash
OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python \
OSA_SOLVER_READINESS_PROFILE=osa-solvers \
python scripts/check_optional_solver_readiness.py
```

This can distinguish a base project environment from a dedicated PyMeep /
`meep.mpb` environment without executing a solver. Environment profiles are
documented in
[`optional_solver_environment_profiles.md`](optional_solver_environment_profiles.md).
Execution approval is prepared in
[`optional_solver_micro_benchmark_execution_packet.md`](optional_solver_micro_benchmark_execution_packet.md),
with one-solver-at-a-time sequencing in
[`optional_solver_execution_sequence.md`](optional_solver_execution_sequence.md)
and per-solver pending/deferred approval records, plus the approved Gmsh-only
and Optiland-only 2026-05-20 execution records, under
[`optional_solver_approval_records/`](optional_solver_approval_records/).

## Claims

These micro-benchmarks may support optional manual validation evidence for a
tiny project-owned path when explicitly run and recorded. They do not imply:

- production-grade physical validation
- formal convergence proof
- real solver monitor results for application-domain benchmarks
- default external solver dependencies
- default external LLM usage
- PyPI/TestPyPI publication readiness
