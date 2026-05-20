# Meep Optional Micro-benchmark Review — 2026-05-20

- Solver: Meep / PyMeep
- Benchmark type: optional manual micro-benchmark
- Review status: accepted as optional manual PyMeep/FDTD smoke evidence
- Execution result: passed
- Meep / PyMeep version: 1.33.0
- OSA_SOLVER_PYTHON: /opt/homebrew/Caskroom/miniforge/base/envs/osa-solvers/bin/python
- External solver/package executed: yes, Meep only
- MPB executed: no
- Gmsh rerun in this task: no
- Optiland rerun in this task: no
- Elmer executed: no
- PyPI/TestPyPI upload: no
- Tag/release action: no
- Production-grade physical validation claimed: no
- Production-grade FDTD validation claimed: no
- Formal convergence proof claimed: no
- Optical correctness claimed: no
- Evidence record: validation/meep/meep_micro_benchmark_2026-05-20.md
- Approval record: docs/optional_solver_approval_records/meep_micro_benchmark_approval_2026-05-20.md

Decision:

- This evidence may be used as optional manual PyMeep/FDTD smoke evidence.
- This evidence does not change default test, quality gate, or release gate behavior.
- This evidence does not authorize PyPI publication.
- This evidence does not authorize any further solver execution.
- This evidence does not authorize MPB execution.

Next candidate:

- MPB may be considered next, but requires explicit OSA_SOLVER_PYTHON profile and separate approval.
- MPB approval must remain separate from Meep, even though meep.mpb is detectable through the same Python profile.
- Elmer remains deferred.
- Gmsh, Optiland, and Meep are already recorded; do not rerun without separate approval.
