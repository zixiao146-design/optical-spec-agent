# Optional Solver Micro-benchmark Execution Approval Packet

This packet prepares future optional solver-backed micro-benchmark execution.
It does not approve execution by itself. It does not approve PyPI/TestPyPI
publication, tag creation, GitHub release creation, or `v1.0.0`.

## Current State

- Current public prerelease: v0.9.0rc7
- Current main development version: 0.9.0rc8.dev0
- PyPI: not published
- TestPyPI uploaded and verified only for: 0.9.0rc6.dev0
- v0.9.0rc8 tag: not created
- v1.0.0 tag: not created
- Solver micro-benchmark approval: granted only for the Gmsh 2026-05-20 run
- Solver micro-benchmark execution performed: yes, Gmsh only on 2026-05-20
- Other solver micro-benchmark execution performed: no

## Execution Principles

- Run one solver at a time.
- Require explicit solver-specific maintainer approval before setting any
  `OSA_RUN_OPTIONAL_*_VALIDATION=1` variable.
- Record the environment profile before execution.
- Record expected artifacts and the report path before execution.
- Review and clean temporary artifacts after the benchmark.
- Stop after each solver and review the report before considering another.
- Do not treat this packet as PyPI, TestPyPI, tag, release, or `v1.0.0`
  authorization.
- Do not claim production-grade physical validation.
- Do not claim a formal convergence proof.

## Recommended Execution Order

1. Gmsh first: CLI mesh generation is the lowest-risk path and validates a
   local `.geo` to `.msh` path only. Status: completed for the approved
   Gmsh-only run on 2026-05-20.
2. Optiland second: local Python/package ray-preview path with no external
   electromagnetic solver.
3. Meep third: requires the solver Python profile, typically
   `OSA_SOLVER_PYTHON=<osa-solvers python>`.
4. MPB fourth: requires the solver Python profile and `meep.mpb`.
5. Elmer deferred: keep deferred until a maintainable `ElmerSolver` install
   route exists.

## Per-solver Approval Packets

### Gmsh

- Solver: Gmsh
- Readiness profile: `homebrew-cli` or current PATH with `gmsh`
- Required env vars after approval:
  - `OSA_RUN_OPTIONAL_GMSH_VALIDATION=1`
- Approval phrase:
  - `I approve running the optional Gmsh micro-benchmark for optical-spec-agent.`
- Command template:
  - `OSA_RUN_OPTIONAL_GMSH_VALIDATION=1 ./scripts/run_optional_solver_micro_benchmarks.sh`
- Expected artifacts:
  - `/tmp/osa-gmsh-micro-benchmark-output/gmsh_preview.geo`
  - `/tmp/osa-gmsh-micro-benchmark-output/gmsh_preview.msh`
  - `/tmp/osa-gmsh-micro-benchmark-report.json`
- Expected report path: `/tmp/osa-gmsh-micro-benchmark-report.json`
- Recorded evidence: `validation/gmsh/gmsh_micro_benchmark_2026-05-20.md`
- Cleanup notes: remove `/tmp/osa-gmsh-micro-benchmark-output/` after review unless the
  maintainer explicitly asks to preserve local evidence.
- Risk notes: syntax/path smoke only; not optical correctness.
- Non-claims: no production-grade physical validation; no formal convergence
  proof.

### Optiland

- Solver: Optiland
- Readiness profile: `current` or a Python profile with `optiland` importable
- Required env vars after approval:
  - `OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1`
- Approval phrase:
  - `I approve running the optional Optiland micro-benchmark for optical-spec-agent.`
- Command template:
  - `OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1 ./scripts/run_optional_solver_micro_benchmarks.sh`
- Expected artifacts:
  - `/tmp/osa-optiland-validation/optiland_preview.py`
  - `/tmp/osa-optiland-validation/optiland_validation_result.json`
  - `/tmp/osa-optiland-validation/optiland_validation_report.json`
- Expected report path:
  `/tmp/osa-optiland-validation/optiland_validation_report.json`
- Cleanup notes: remove `/tmp/osa-optiland-validation/` after review unless
  preservation is requested.
- Risk notes: ray/backend path smoke only; not lens design validation.
- Non-claims: no production-grade physical validation; no formal convergence
  proof.

### Meep

- Solver: Meep / PyMeep
- Readiness profile: `osa-solvers`
- Required env vars after approval:
  - `OSA_SOLVER_PYTHON=<path to solver Python>`
  - `OSA_SOLVER_READINESS_PROFILE=osa-solvers`
  - `OSA_RUN_OPTIONAL_MEEP_VALIDATION=1`
- Approval phrase:
  - `I approve running the optional Meep micro-benchmark for optical-spec-agent using OSA_SOLVER_PYTHON=<path>.`
- Command template:
  - `OSA_SOLVER_PYTHON=<path> OSA_SOLVER_READINESS_PROFILE=osa-solvers OSA_RUN_OPTIONAL_MEEP_VALIDATION=1 ./scripts/run_optional_solver_micro_benchmarks.sh`
- Expected artifacts:
  - `/tmp/osa-meep-validation/meep_preview.py`
  - `/tmp/osa-meep-validation/meep_validation_result.json`
  - `/tmp/osa-meep-validation/meep_validation_report.json`
- Expected report path: `/tmp/osa-meep-validation/meep_validation_report.json`
- Cleanup notes: remove `/tmp/osa-meep-validation/` after review unless
  preservation is requested.
- Risk notes: tiny PyMeep path smoke only; not FDTD accuracy or convergence
  evidence.
- Non-claims: no production-grade physical validation; no formal convergence
  proof.

### MPB

- Solver: MPB through `meep.mpb`
- Readiness profile: `osa-solvers`
- Required env vars after approval:
  - `OSA_SOLVER_PYTHON=<path to solver Python>`
  - `OSA_SOLVER_READINESS_PROFILE=osa-solvers`
  - `OSA_RUN_OPTIONAL_MPB_VALIDATION=1`
- Approval phrase:
  - `I approve running the optional MPB micro-benchmark for optical-spec-agent using OSA_SOLVER_PYTHON=<path>.`
- Command template:
  - `OSA_SOLVER_PYTHON=<path> OSA_SOLVER_READINESS_PROFILE=osa-solvers OSA_RUN_OPTIONAL_MPB_VALIDATION=1 ./scripts/run_optional_solver_micro_benchmarks.sh`
- Expected artifacts:
  - `/tmp/osa-mpb-validation/mpb_preview.py`
  - `/tmp/osa-mpb-validation/mpb_validation_result.json`
  - `/tmp/osa-mpb-validation/mpb_validation_report.json`
- Expected report path: `/tmp/osa-mpb-validation/mpb_validation_report.json`
- Cleanup notes: remove `/tmp/osa-mpb-validation/` after review unless
  preservation is requested.
- Risk notes: tiny band path smoke only; not band convergence evidence.
- Non-claims: no production-grade physical validation; no formal convergence
  proof.

### Elmer

- Solver: Elmer / ElmerSolver
- Readiness profile: `deferred-elmer`
- Required env vars: none authorized now
- Approval phrase:
  - `I approve running the optional Elmer micro-benchmark for optical-spec-agent.`
- Command template:
  - Deferred; do not run without a maintainable `ElmerSolver` install route and
    a new explicit approval.
- Expected artifacts:
  - `/tmp/osa-elmer-validation/case.sif`
  - `/tmp/osa-elmer-validation/elmer_validation_report.json`
- Expected report path: `/tmp/osa-elmer-validation/elmer_validation_report.json`
- Cleanup notes: deferred until install route exists.
- Risk notes: Elmer remains Level 2 + Level-3-ready, install deferred.
- Non-claims: no Elmer Level 3 claim; no production-grade physical validation;
  no formal convergence proof.

## Explicitly Not Approved

- PyPI publication
- TestPyPI upload
- Tag or GitHub release creation
- `v1.0.0` release
- Not approved: production-grade physical validation claim
- Not approved: formal convergence proof claim
