# Optional Solver Micro-benchmark Approval Matrix

This matrix is a maintainer review aid for optional solver-backed
micro-benchmarks. It does not approve solver execution by itself. Default
pytest, smoke checks, quality gates, release gates, and package builds do not
run external solvers.

Missing solvers are non-blocking. PyPI/TestPyPI publication, tag creation, and
GitHub release actions are unrelated to this matrix and remain separately
gated. These checks are preview/design-assist evidence only; they do not claim
production-grade physical validation or a formal convergence proof.
Elmer remains deferred until a maintainable ElmerSolver install route exists.

Readiness is profile/environment-specific. The default profile uses the current
Python and current `PATH`; maintainers can set `OSA_SOLVER_PYTHON` and
`OSA_SOLVER_READINESS_PROFILE=osa-solvers` to probe a dedicated solver Python
such as the local `osa-solvers` conda environment. This is still import/path
detection only, not solver execution.

| Solver | Current status | Availability detection | Opt-in env var | Script path | Expected input fixture | Expected output artifact | Risk / limitation | Requires explicit approval | Default execution | Production-grade claim | Formal convergence claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gmsh | Executed/passed for the approved 2026-05-20 Gmsh-only run; reviewed and accepted as optional manual mesh-generation smoke evidence | `command -v gmsh` on current `PATH`; optional `gmsh` Python import probe | `OSA_RUN_OPTIONAL_GMSH_VALIDATION=1` | `scripts/run_optional_gmsh_validation.sh` | `examples/specs/gmsh_preview.json` | `/tmp/osa-gmsh-micro-benchmark-output/gmsh_preview.msh` and `/tmp/osa-gmsh-micro-benchmark-report.json` | Mesh path smoke only; not optical correctness | approved/executed/reviewed for Gmsh only on 2026-05-20; future runs need fresh approval | no | no | no |
| Meep | Executed/passed for the approved 2026-05-20 Meep-only run; recorded as optional manual PyMeep/FDTD smoke evidence | `meep` import probe through current Python or `OSA_SOLVER_PYTHON`; recommended profile is `osa-solvers` | `OSA_RUN_OPTIONAL_MEEP_VALIDATION=1` | `scripts/run_optional_meep_validation.sh` | `examples/specs/missing_wavelength_meep_preview.json` | `/tmp/osa-meep-micro-benchmark-output/` artifacts and `/tmp/osa-meep-micro-benchmark-report.json` | Tiny PyMeep path smoke only; not production FDTD validation; MPB remains separate even if `meep.mpb` is detected | approved/executed for Meep only on 2026-05-20 using `OSA_SOLVER_PYTHON=/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python`; future runs need fresh approval | no | no | no |
| MPB | Candidate-ready with previous narrow manual report | `meep.mpb` import probe through current Python or `OSA_SOLVER_PYTHON`; optional `mpb` CLI path | `OSA_RUN_OPTIONAL_MPB_VALIDATION=1` | `scripts/run_optional_mpb_validation.sh` | `examples/specs/mpb_preview.json` | `/tmp/osa-mpb-validation/mpb_validation_result.json` and report JSON | Tiny band path smoke only; not band convergence evidence | yes | no | no | no |
| Optiland | Executed/passed for the approved 2026-05-20 Optiland-only run; reviewed and accepted as optional manual ray/path smoke evidence | `optiland` import probe through current Python or `OSA_SOLVER_PYTHON`, optional CLI path check | `OSA_RUN_OPTIONAL_OPTILAND_VALIDATION=1` | `scripts/run_optional_optiland_validation.sh` | `examples/specs/optiland_preview.json` | `/tmp/osa-optiland-micro-benchmark-output/optiland_validation_result.json` and `/tmp/osa-optiland-micro-benchmark-report.json` | Tiny ray/backend path smoke only; not lens design validation | accepted for Optiland only on 2026-05-20; future runs need fresh approval | no | no | no |
| Elmer | Deferred | `command -v ElmerSolver` only | `OSA_RUN_OPTIONAL_ELMER_VALIDATION=1` | `scripts/run_optional_elmer_validation.sh` | future local `.sif` fixture | `/tmp/osa-elmer-validation/elmer_validation_report.json` | Deferred until a maintainable ElmerSolver install route exists; Elmer remains Level 2 + Level-3-ready | yes | no | no | no |

Required approval must be explicit and solver-specific. The approval template is
documented in
[`optional_solver_micro_benchmark_approval_record_template.md`](optional_solver_micro_benchmark_approval_record_template.md).
Readiness status is recorded in
[`optional_solver_micro_benchmark_readiness_status.md`](optional_solver_micro_benchmark_readiness_status.md).
Environment profiles are documented in
[`optional_solver_environment_profiles.md`](optional_solver_environment_profiles.md).
Future execution approval is packaged in
[`optional_solver_micro_benchmark_execution_packet.md`](optional_solver_micro_benchmark_execution_packet.md),
with pending per-solver records under
[`optional_solver_approval_records/`](optional_solver_approval_records/) and a
one-solver-at-a-time sequence in
[`optional_solver_execution_sequence.md`](optional_solver_execution_sequence.md).
The Gmsh review record is
[`optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md`](optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md).
It accepts only Gmsh mesh-generation smoke evidence and does not approve
Optiland, Meep, MPB, Elmer, PyPI/TestPyPI upload, tag creation, or release
creation.
The Optiland approval record is
[`optional_solver_approval_records/optiland_micro_benchmark_approval_2026-05-20.md`](optional_solver_approval_records/optiland_micro_benchmark_approval_2026-05-20.md).
The Optiland review record is
[`optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md`](optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md).
It accepts only optional manual ray/path smoke evidence and does not approve
Meep, MPB, Elmer, any future Gmsh or Optiland rerun, PyPI/TestPyPI upload,
tag creation, or release creation.
The Meep approval record is
[`optional_solver_approval_records/meep_micro_benchmark_approval_2026-05-20.md`](optional_solver_approval_records/meep_micro_benchmark_approval_2026-05-20.md).
The Meep evidence record is
[`../validation/meep/meep_micro_benchmark_2026-05-20.md`](../validation/meep/meep_micro_benchmark_2026-05-20.md).
It accepts only optional manual PyMeep/FDTD smoke evidence and does not approve
MPB, Elmer, any future Gmsh/Optiland/Meep rerun, PyPI/TestPyPI upload, tag
creation, or release creation.
The Meep decision packet is
[`optional_solver_approval_records/meep_micro_benchmark_decision_packet.md`](optional_solver_approval_records/meep_micro_benchmark_decision_packet.md).
It documents the required `OSA_SOLVER_PYTHON` profile, command, artifacts, and
non-claims for the approved Meep-only run.
