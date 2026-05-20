# Optional Solver Micro-benchmark Readiness Status

- Current public prerelease: v0.9.0rc7
- Current main development version: 0.9.0rc8.dev0
- PyPI: not published
- v0.9.0rc8 tag: absent
- v1.0.0 tag: absent
- Solver micro-benchmark default mode: no execution
- TestPyPI uploaded and verified only for: 0.9.0rc6.dev0

## Readiness By Solver

| Solver | Readiness status | Default execution | Approval required | Notes |
| --- | --- | --- | --- | --- |
| Gmsh | Candidate-ready with previous narrow manual report | no | yes | Availability detection checks `gmsh` on PATH only. |
| Meep | Candidate-ready with previous narrow manual report | no | yes | Availability detection checks Python module spec `meep` only. |
| MPB | Candidate-ready with previous narrow manual report | no | yes | Availability detection checks Python module spec `meep.mpb` only. |
| Optiland | Candidate-ready with previous narrow manual report | no | yes | Availability detection checks Python module spec `optiland` and optional CLI path only. |
| Elmer | deferred | no | yes | Elmer remains Level 2 + Level-3-ready until a maintainable ElmerSolver install route exists. |

## Next Step

Before any opt-in execution, the maintainer must provide explicit
solver-specific approval using the phrase in
[`optional_solver_micro_benchmark_approval_record_template.md`](optional_solver_micro_benchmark_approval_record_template.md).

No PyPI upload, TestPyPI upload, tag creation, GitHub release creation, or
`v1.0.0` release is approved by this readiness status.
