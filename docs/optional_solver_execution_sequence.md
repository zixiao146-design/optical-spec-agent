# Optional Solver Execution Sequence

Optional solver-backed micro-benchmarks should be executed one solver at a time
only after explicit solver-specific approval. This sequence is a planning aid,
not execution approval.

## Recommended Order

1. Gmsh first.
   - Lowest risk because it checks a CLI mesh generation path from a local
     `.geo` preview to `.msh`.
   - Stop after Gmsh and review the report before considering another solver.
2. Optiland second.
   - Checks a local Python/package ray-preview path.
   - Stop after Optiland and review whether the artifact path is useful.
3. Meep third.
   - Requires `OSA_SOLVER_PYTHON` pointing at a solver Python profile such as
     `osa-solvers`.
   - Stop after Meep and review the PyMeep report before considering MPB.
4. MPB fourth.
   - Requires `OSA_SOLVER_PYTHON` and `meep.mpb`.
   - Stop after MPB and review the band-path smoke report.
5. Elmer deferred.
   - Do not run until a maintainable `ElmerSolver` install route exists.
   - Elmer remains Level 2 + Level-3-ready, not Level 3.

## Stop Conditions

- The solver is unavailable in the selected environment profile.
- The approval phrase does not name the exact solver.
- The command would set more than one `OSA_RUN_OPTIONAL_*_VALIDATION=1` flag.
- The expected output directory already contains artifacts that should be
  preserved.
- The result report is missing required safety fields.
- Any step suggests PyPI/TestPyPI upload, tag creation, GitHub release creation,
  or `v1.0.0` release.

## Review After Each Benchmark

- Read the solver-specific report JSON.
- Confirm `production_grade_validation_claimed=false`.
- Confirm `formal_convergence_proof_claimed=false`.
- Confirm the benchmark stayed within the approved solver and environment.
- Decide whether to preserve or remove temporary artifacts.
- Record any follow-up in a manual validation report before considering the
  next solver.

Do not batch all solvers without separate approval.
