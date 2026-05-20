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

- Gmsh is available through the CLI/PATH profile.
- Optiland is available in the local Python/package profile.
- Meep and `meep.mpb` are detectable through the maintainer-reported
  `osa-solvers` Python profile when `OSA_SOLVER_PYTHON` points there.
- Elmer remains unavailable/deferred.
- No solver micro-benchmark has been executed or approved by this status.

## Readiness By Solver

| Solver | Readiness status | Default execution | Approval required | Notes |
| --- | --- | --- | --- | --- |
| Gmsh | Candidate-ready with previous narrow manual report | no | yes | Availability detection checks `gmsh` on PATH and can optionally probe the `gmsh` Python module. |
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
The current pending/deferred records are stored under
[`optional_solver_approval_records/`](optional_solver_approval_records/).

No PyPI upload, TestPyPI upload, tag creation, GitHub release creation, or
`v1.0.0` release is approved by this readiness status.
