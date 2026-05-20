# Optional Solver Micro-benchmark Readiness Status

- Current public prerelease: v0.9.0rc7
- Current main development version: 0.9.0rc8.dev0
- PyPI: not published
- v0.9.0rc8 tag: absent
- v1.0.0 tag: absent
- Solver micro-benchmark default mode: no execution
- TestPyPI uploaded and verified only for: 0.9.0rc6.dev0
- Optional solver execution approval packet:
  [`optional_solver_micro_benchmark_execution_packet.md`](optional_solver_micro_benchmark_execution_packet.md)
- Per-solver approval records:
  [`optional_solver_approval_records/`](optional_solver_approval_records/)

Readiness is calibrated by profile. Default checks use the current Python and
current `PATH`. A maintainer may set `OSA_SOLVER_PYTHON` to a dedicated solver
Python, for example the local `osa-solvers` conda environment, and label the
report with `OSA_SOLVER_READINESS_PROFILE=osa-solvers`. This changes only the
import/path probes; it does not run solver micro-benchmarks.

Latest local readiness findings are environment-specific:

- Gmsh is available through the CLI/PATH profile, and the approved Gmsh-only
  optional micro-benchmark passed on 2026-05-20.
- Maintainer review accepted the Gmsh result as optional manual
  mesh-generation smoke evidence, not optical correctness evidence.
- Optiland is available in the local Python/package profile.
- Meep and `meep.mpb` are detectable through the maintainer-reported
  `osa-solvers` Python profile when `OSA_SOLVER_PYTHON` points there.
- Elmer remains unavailable/deferred.
- Gmsh was executed only for the approved 2026-05-20 run. No Meep, MPB,
  Optiland, or Elmer micro-benchmark has been executed or approved by this
  status.
- Optiland is the next candidate only; it is not approved by the Gmsh review.

## Readiness By Solver

| Solver | Readiness status | Default execution | Approval required | Notes |
| --- | --- | --- | --- | --- |
| Gmsh | Executed/passed for the approved Gmsh-only optional micro-benchmark on 2026-05-20; review accepted it as optional manual mesh-generation smoke evidence | no by default; yes only for the completed approved Gmsh run | future Gmsh runs require fresh approval | Evidence: `validation/gmsh/gmsh_micro_benchmark_2026-05-20.md`; review: `docs/optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md`; availability detection checks `gmsh` on PATH and can optionally probe the `gmsh` Python module. |
| Meep | Candidate-ready with previous narrow manual report | no | yes | Availability detection checks `meep` through current Python or `OSA_SOLVER_PYTHON`. |
| MPB | Candidate-ready with previous narrow manual report | no | yes | Availability detection checks `meep.mpb` through current Python or `OSA_SOLVER_PYTHON`; MPB CLI is optional. |
| Optiland | Candidate-ready with previous narrow manual report | no | yes | Availability detection checks `optiland` through current Python or `OSA_SOLVER_PYTHON`, plus optional CLI path. |
| Elmer | deferred | no | yes | Elmer remains Level 2 + Level-3-ready until a maintainable ElmerSolver install route exists. |

## Next Step

Before any opt-in execution, the maintainer must provide explicit
solver-specific approval using the phrase in
[`optional_solver_micro_benchmark_approval_record_template.md`](optional_solver_micro_benchmark_approval_record_template.md).
Profile setup is documented in
[`optional_solver_environment_profiles.md`](optional_solver_environment_profiles.md).
The one-solver-at-a-time execution sequence is documented in
[`optional_solver_execution_sequence.md`](optional_solver_execution_sequence.md).
The current pending/deferred records and the approved Gmsh-only execution
record are stored under
[`optional_solver_approval_records/`](optional_solver_approval_records/).
The Gmsh review decision closes the Gmsh loop but does not approve Optiland,
Meep, MPB, Elmer, any future Gmsh rerun, PyPI/TestPyPI upload, tag creation, or
release creation.

No PyPI upload, TestPyPI upload, tag creation, GitHub release creation, or
`v1.0.0` release is approved by this readiness status.
