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
| Gmsh | Tiny mesh generation from a local `.geo` preview | `.msh` | Validates syntax/path only, not optical correctness. |
| Meep | Tiny PyMeep smoke from a generated preview artifact | result JSON | Validates import/run path only, not production-grade FDTD. |
| MPB | Tiny band-structure smoke through `meep.mpb` | band summary JSON | Validates MPB Python path only. |
| Optiland | Tiny ray-trace or import/run smoke | result JSON | Validates local Optiland path only. |
| Elmer | Deferred until maintainable `ElmerSolver` install exists | deferred report | No Level 3 validation is claimed. |

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

## Claims

These micro-benchmarks may support optional manual validation evidence for a
tiny project-owned path when explicitly run and recorded. They do not imply:

- production-grade physical validation
- formal convergence proof
- real solver monitor results for application-domain benchmarks
- default external solver dependencies
- default external LLM usage
- PyPI/TestPyPI publication readiness
