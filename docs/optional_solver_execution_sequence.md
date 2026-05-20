# Optional Solver Execution Sequence

Optional solver-backed micro-benchmarks should be executed one solver at a time
only after explicit solver-specific approval. This sequence is a planning aid,
not execution approval.

## Recommended Order

1. Gmsh first.
   - Lowest risk because it checks a CLI mesh generation path from a local
     `.geo` preview to `.msh`.
   - Stop after Gmsh and review the report before considering another solver.
   - Status: completed for the approved Gmsh-only run on 2026-05-20; see
     `validation/gmsh/gmsh_micro_benchmark_2026-05-20.md`.
   - Review status: accepted as optional manual mesh-generation smoke evidence;
     see `docs/optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md`.
2. Optiland second.
   - Checks a local Python/package ray-preview path.
   - Stop after Optiland and review whether the artifact path is useful.
   - Status: completed for the approved Optiland-only run on 2026-05-20; see
     `validation/optiland/optiland_micro_benchmark_2026-05-20.md`.
   - Review status: accepted as optional manual ray/path smoke evidence; see
     `docs/optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md`.
   - Scope: optional manual ray/path smoke evidence only, not lens design
     validation.
3. Meep third.
   - Requires `OSA_SOLVER_PYTHON` pointing at a solver Python profile such as
     `osa-solvers`.
   - Decision packet:
     `docs/optional_solver_approval_records/meep_micro_benchmark_decision_packet.md`.
   - Status: completed for the approved Meep-only run on 2026-05-20; see
     `validation/meep/meep_micro_benchmark_2026-05-20.md`.
   - Review status: accepted as optional manual PyMeep/FDTD smoke evidence;
     see `docs/optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md`.
   - Scope: optional manual PyMeep/FDTD smoke evidence only, not production
     FDTD validation or optical correctness evidence.
   - Stop after Meep and review the PyMeep report before considering MPB.
4. MPB fourth.
   - Requires `OSA_SOLVER_PYTHON` and `meep.mpb`.
   - Decision packet:
     `docs/optional_solver_approval_records/mpb_micro_benchmark_decision_packet.md`.
   - MPB CLI is not required if the `meep.mpb` Python import path is available.
   - Status: completed for the approved 2026-05-20 MPB-only run and reviewed
     as optional manual MPB/band-structure smoke evidence.
   - Evidence: `validation/mpb/mpb_micro_benchmark_2026-05-20.md`.
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
The accepted Gmsh review did not authorize Optiland; Optiland was run only
after its separate approval record. The accepted Optiland review does not
authorize Meep; Meep was run only after its separate approval record. The
accepted Meep evidence does not authorize MPB, Elmer, any future Gmsh rerun,
any future Optiland rerun, or any future Meep rerun.
The approved MPB evidence closes only the MPB-only run and does not authorize
Elmer, any future Gmsh/Optiland/Meep/MPB rerun, PyPI/TestPyPI upload, tag
creation, or release creation.
