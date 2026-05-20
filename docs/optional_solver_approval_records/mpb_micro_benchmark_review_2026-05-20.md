# MPB Optional Micro-benchmark Review - 2026-05-20

- Solver: MPB / `meep.mpb`
- Benchmark type: optional manual micro-benchmark
- Review status: accepted as optional manual MPB / band-structure smoke evidence
- Execution result: passed
- MPB / PyMeep version: 1.33.0
- `OSA_SOLVER_PYTHON`: `/opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python`
- MPB CLI required: no
- Execution path: `meep.mpb` through solver Python profile
- External solver/package executed: yes, MPB only
- Meep FDTD benchmark executed: no
- Gmsh rerun in this task: no
- Optiland rerun in this task: no
- Elmer executed: no
- PyPI/TestPyPI upload: no
- Tag/release action: no
- Production-grade physical validation claimed: no
- Production-grade MPB validation claimed: no
- Production band-structure validation claimed: no
- Formal convergence proof claimed: no
- Optical correctness claimed: no
- Evidence record: `validation/mpb/mpb_micro_benchmark_2026-05-20.md`
- Approval record: `docs/optional_solver_approval_records/mpb_micro_benchmark_approval_2026-05-20.md`

## Decision

- This evidence may be used as optional manual MPB / band-structure smoke evidence.
- This evidence does not change default test, quality gate, or release gate behavior.
- This evidence does not authorize PyPI publication.
- This evidence does not authorize any further solver execution.
- This evidence does not authorize Elmer execution.
- This evidence does not establish production-grade band-structure validation or optical correctness.

## Optional Solver Evidence Summary

- Gmsh: executed, passed, reviewed / accepted
- Optiland: executed, passed, reviewed / accepted
- Meep: executed, passed, reviewed / accepted
- MPB: executed, passed, reviewed / accepted
- Elmer: deferred, not Level 3

## Next Candidate

- Elmer remains deferred until a maintainable install route exists.
- No additional solver execution is approved.
- Future solver reruns require separate explicit approval.
