# Open-source Solver Validation Plan

## Purpose

This plan defines how optional solver-backed validation may be added later for
open-source tools without making external solvers default release blockers.

The default path remains local artifact preview, offline evidence, and no
external solver execution by default.

The optional availability preflight is
`scripts/open_solver_validation_preflight.sh`. It detects candidate solver CLI
commands and Python-backed module availability, and can write an availability
JSON report, but it does not execute Meep, MPB, Gmsh, Elmer, Optiland, or any
other solver.

The rc8.dev0 micro-benchmark planning layer is documented in
`docs/solver_validation_micro_benchmarks.md` and summarized by
`validation/solver_validation_micro_benchmarks.json`. The unified wrapper
`scripts/run_optional_solver_micro_benchmarks.sh` is default no-execute: unless
an explicit `OSA_RUN_OPTIONAL_*_VALIDATION=1` variable is set, it only prints
the manifest summary and optional JSON report metadata.

The readiness/approval layer is documented in
`docs/optional_solver_micro_benchmark_approval_matrix.md` and
`docs/optional_solver_micro_benchmark_approval_record_template.md`.
`scripts/check_optional_solver_readiness.py` performs availability detection
only; it does not execute solver commands, create releases, create tags, or
authorize PyPI/TestPyPI publication.

## Candidate open-source solver families

- Meep: current research-preview adapter and optional explicit local execution
  harness.
- Gmsh: current MVP/scaffold geometry and mesh artifact preview.
- Elmer: current MVP/scaffold FEM input preview.
- MPB: current MVP/scaffold band-structure input preview.
- Optiland: current MVP/scaffold optical design preview; solver-backed
  validation is not claimed and depends on future schema maturity.

## Manual validation path

Future optional solver-backed validation should follow this pattern:

- User installs the solver manually.
- `scripts/open_solver_validation_preflight.sh` records CLI and Python module
  availability only; it records availability only and does not perform
  solver-backed validation.
- An environment variable enables solver-backed validation.
- Tests are skipped by default unless enabled.
- Generated artifacts are compared against expected high-level diagnostics.
- Failures do not block default smoke unless explicitly configured.
- Release notes state whether solver-backed validation was actually run.
- Manual results are recorded with
  `docs/manual_solver_validation_report_template.md`.

The first pilot-ready candidate is Gmsh. Its opt-in guide is
`docs/gmsh_optional_validation_pilot.md`, and its default script path is
`scripts/run_optional_gmsh_validation.sh`. Default mode does not run Gmsh; it
only checks availability, fixture presence, and report metadata.

The first Gmsh opt-in pilot was run on 2026-05-14 and is recorded in
`validation/gmsh/gmsh_validation_pilot_2026-05-14.md` and
`docs/gmsh_level3_readiness.md`. It supports a limited Level 3 claim for
optional manual validation of the project/adapter `.geo` artifact path only.
It does not make Gmsh a default test, smoke, quality-gate, or release
dependency.

The first Meep opt-in pilot was run on 2026-05-14 and is recorded in
`validation/meep/meep_validation_pilot_2026-05-14.md` and
`docs/meep_level3_readiness.md`. It supports a limited Level 3 claim for an
optional manual PyMeep validation path only. It does not make Meep a default
test, smoke, quality-gate, CI, or release dependency.

The first MPB opt-in pilot was run on 2026-05-14 and is recorded in
`validation/mpb/mpb_validation_pilot_2026-05-14.md` and
`docs/mpb_level3_readiness.md`. It supports a limited Level 3 claim for an
optional manual MPB/PyMeep validation path only. MPB CLI is not required, and
the report does not make MPB a default test, smoke, quality-gate, CI, or release
dependency.

The first Optiland opt-in pilot was run on 2026-05-14 and is recorded in
`validation/optiland/optiland_validation_pilot_2026-05-14.md` and
`docs/optiland_level3_readiness.md`. It supports a limited Level 3 claim for an
optional manual Optiland backend path only. The report does not make Optiland a
default test, smoke, quality-gate, CI, or release dependency.

Elmer is prepared for a future Level 3 pilot but remains Level 2. Its opt-in
guide is `docs/elmer_optional_validation_pilot.md`, readiness checklist is
`docs/elmer_level3_readiness.md`, and default script is
`scripts/run_optional_elmer_validation.sh`. Default mode only checks
ElmerSolver availability and fixture presence; ElmerSolver unavailable is
non-blocking, and no Elmer execution or completed report exists yet. The
2026-05-15 conda-forge/Homebrew install attempt is recorded as deferred in
`validation/elmer/elmer_install_deferred_2026-05-15.md`.

For Python-backed stacks, Meep availability can be reported through
`import meep as mp`, MPB availability can be reported through `from meep import
mpb`, and Optiland availability can be reported through `import optiland`.
MPB CLI absence is acceptable when `meep.mpb` is available. ElmerSolver remains
optional/manual and may be unavailable without failing default preflight.

## Required guardrails

- No external solver is run by default.
- No proprietary license required.
- No network required by default.
- No production-grade claim unless evidence exists.
- Release notes must state whether solver-backed validation was actually run.
- Solver-backed checks must remain separate from default package, CLI, docs, and
  smoke gates unless maintainers explicitly approve a narrower release gate.

## Future optional test naming

- Tests should use `solver_optional`, `external_solver`, and
  `manual_validation` markers, with optional solver-specific markers if needed.
- Tests should be skipped unless an environment variable is set.
- Tests should not be part of default `pytest`.
- Tests should not be part of default `scripts/smoke_release.sh`.
- Tests should not require proprietary tools or proprietary licenses.
- Marker policy is documented in `docs/pytest_marker_policy.md`.
- Optional solver micro-benchmarks remain outside default quality gates and do
  not claim production-grade physical validation or formal convergence proof.
