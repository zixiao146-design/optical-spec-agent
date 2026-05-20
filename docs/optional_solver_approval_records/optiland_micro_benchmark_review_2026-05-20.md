# Optiland Optional Micro-benchmark Review - 2026-05-20

- Solver: Optiland
- Benchmark type: optional manual micro-benchmark
- Review status: accepted as optional manual ray/path smoke evidence
- Execution result: passed
- External solver/package executed: yes, Optiland only
- Gmsh rerun in this task: no
- Meep executed: no
- MPB executed: no
- Elmer executed: no
- PyPI/TestPyPI upload: no
- Tag/release action: no
- Production-grade physical validation claimed: no
- Formal convergence proof claimed: no
- Optical correctness claimed: no
- Evidence record: validation/optiland/optiland_micro_benchmark_2026-05-20.md
- Approval record: docs/optional_solver_approval_records/optiland_micro_benchmark_approval_2026-05-20.md

Decision:

- This evidence may be used as optional manual Optiland ray/path smoke evidence.
- This evidence does not change default test, quality gate, or release gate behavior.
- This evidence does not authorize PyPI publication.
- This evidence does not authorize any further solver execution.

Next candidate:

- Meep may be considered next, but requires explicit OSA_SOLVER_PYTHON profile and separate approval.
- MPB may be considered after Meep or separately, but requires explicit OSA_SOLVER_PYTHON profile and separate approval.
- Elmer remains deferred.
- Gmsh and Optiland are already recorded; do not rerun without separate approval.
