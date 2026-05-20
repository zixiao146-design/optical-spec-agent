# Optional Solver Micro-benchmark Readiness Status

- Current public prerelease: v0.9.0rc8
- Current main development version: 0.9.0rc9.dev0
- PyPI: not published
- v0.9.0rc9 tag: absent
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
- Optiland is available in the local Python/package profile, and the approved
  Optiland-only optional micro-benchmark passed on 2026-05-20.
- Maintainer review accepted the Optiland result as optional manual ray/path
  smoke evidence, not optical correctness evidence.
- Meep and `meep.mpb` are detectable through the maintainer-reported
  `osa-solvers` Python profile when `OSA_SOLVER_PYTHON` points there.
- A Meep-specific decision packet is recorded at
  `docs/optional_solver_approval_records/meep_micro_benchmark_decision_packet.md`.
  The approved Meep-only optional micro-benchmark used `OSA_SOLVER_PYTHON` and
  passed on 2026-05-20 as optional manual PyMeep/FDTD smoke evidence only.
- Maintainer review accepted the Meep result as optional manual PyMeep/FDTD
  smoke evidence, not production-grade FDTD validation, optical correctness
  evidence, or MPB authorization.
- An MPB-specific decision packet is recorded at
  `docs/optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md`.
  The approved MPB-only optional micro-benchmark used `OSA_SOLVER_PYTHON`,
  executed through `meep.mpb`, and passed on 2026-05-20 as optional manual
  MPB/band-structure smoke evidence only.
- Elmer remains unavailable/deferred.
- Gmsh was executed only for the approved Gmsh run. Optiland was executed only
  for the separately approved Optiland run. Meep was executed only for the
  separately approved Meep run. MPB was executed only for the separately
  approved MPB run. No Elmer micro-benchmark has been executed or approved by
  this status.

## Readiness By Solver

| Solver | Readiness status | Default execution | Approval required | Notes |
| --- | --- | --- | --- | --- |
| Gmsh | Executed/passed for the approved Gmsh-only optional micro-benchmark on 2026-05-20; review accepted it as optional manual mesh-generation smoke evidence | no by default; yes only for the completed approved Gmsh run | future Gmsh runs require fresh approval | Evidence: `validation/gmsh/gmsh_micro_benchmark_2026-05-20.md`; review: `docs/optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md`; availability detection checks `gmsh` on PATH and can optionally probe the `gmsh` Python module. |
| Meep | Executed/passed for the approved Meep-only optional micro-benchmark on 2026-05-20; review accepted it as optional manual PyMeep/FDTD smoke evidence | no by default; yes only for the completed approved Meep run | future Meep runs require fresh approval | Evidence: `validation/meep/meep_micro_benchmark_2026-05-20.md`; approval: `docs/optional_solver_approval_records/meep_micro_benchmark_approval_2026-05-20.md`; review: `docs/optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md`; decision packet: `docs/optional_solver_approval_records/meep_micro_benchmark_decision_packet.md`; MPB remains separate and requires `OSA_SOLVER_PYTHON` plus separate approval. |
| MPB | Executed/passed for the approved MPB-only optional micro-benchmark on 2026-05-20 through `meep.mpb`; recorded as optional manual MPB/band-structure smoke evidence reviewed and accepted | no by default; yes only for the completed approved MPB run | future MPB runs require fresh approval | Evidence: `validation/mpb/mpb_micro_benchmark_2026-05-20.md`; approval: `docs/optional_solver_approval_records/mpb_micro_benchmark_approval_2026-05-20.md`; decision packet: `docs/optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md`; availability detection checks `meep.mpb` through current Python or `OSA_SOLVER_PYTHON`; MPB CLI is not required if the Python path is available. |
| Optiland | Executed/passed for the approved Optiland-only optional micro-benchmark on 2026-05-20; review accepted it as optional manual ray/path smoke evidence | no by default; yes only for the completed approved Optiland run | future Optiland runs require fresh approval | Evidence: `validation/optiland/optiland_micro_benchmark_2026-05-20.md`; approval: `docs/optional_solver_approval_records/optiland_micro_benchmark_approval_2026-05-20.md`; review: `docs/optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md`; availability detection checks `optiland` through current Python or `OSA_SOLVER_PYTHON`, plus optional CLI path. |
| Elmer | deferred | no | yes | Elmer remains Level 2 + Level-3-ready until a maintainable ElmerSolver install route exists. |

## Next Step

Before any opt-in execution, the maintainer must provide explicit
solver-specific approval using the phrase in
[`optional_solver_micro_benchmark_approval_record_template.md`](optional_solver_micro_benchmark_approval_record_template.md).
Profile setup is documented in
[`optional_solver_environment_profiles.md`](optional_solver_environment_profiles.md).
The one-solver-at-a-time execution sequence is documented in
[`optional_solver_execution_sequence.md`](optional_solver_execution_sequence.md).
The current pending/deferred records plus the approved Gmsh-only, Optiland-only,
Meep-only, and MPB-only execution records are stored under
[`optional_solver_approval_records/`](optional_solver_approval_records/).
The reviewed Meep evidence is accepted only as optional manual PyMeep/FDTD
smoke evidence. It does not approve Elmer, any future
Gmsh/Optiland/Meep rerun, PyPI/TestPyPI upload, tag creation, or release
creation.
The MPB evidence is reviewed and accepted only as optional manual MPB/band-structure smoke
evidence. It does not approve future MPB reruns,
PyPI/TestPyPI upload, tag creation, or release creation.
The reviewed Optiland run closes only the separately approved Optiland execution step;
it does not approve Elmer, any future Gmsh, Optiland, Meep, or MPB rerun,
PyPI/TestPyPI upload, tag creation, or release creation.

No PyPI upload, TestPyPI upload, tag creation, GitHub release creation, or
`v1.0.0` release is approved by this readiness status.
