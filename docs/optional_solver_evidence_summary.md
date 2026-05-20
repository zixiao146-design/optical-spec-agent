# Optional Solver Evidence Summary

Current public prerelease: v0.9.0rc7.
Current main release draft: `0.9.0rc8`.

PyPI is not published. TestPyPI has only `0.9.0rc6.dev0` uploaded and
verified. The `v0.9.0rc8` tag has not been created. The `v1.0.0` tag has not
been created.

This document consolidates the optional solver micro-benchmark evidence that is
already recorded and reviewed. It does not authorize any solver rerun, upload,
tag, release, or publication action.

## Evidence Summary Table

| Solver | Readiness status | Approval status | Execution status | Review status | Evidence record | Review record | Accepted evidence type | Default gate behavior | Production-grade claim | Formal convergence claim | Optical correctness claim |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Gmsh | candidate ready through CLI/PATH profile | approved for the recorded 2026-05-20 run only | executed / passed | reviewed / accepted | `validation/gmsh/gmsh_micro_benchmark_2026-05-20.md` | `docs/optional_solver_approval_records/gmsh_micro_benchmark_review_2026-05-20.md` | optional manual mesh-generation smoke evidence | no solver execution by default | no | no | no |
| Optiland | candidate ready through local Python/package profile | approved for the recorded 2026-05-20 run only | executed / passed | reviewed / accepted | `validation/optiland/optiland_micro_benchmark_2026-05-20.md` | `docs/optional_solver_approval_records/optiland_micro_benchmark_review_2026-05-20.md` | optional manual ray/path smoke evidence | no solver execution by default | no | no | no |
| Meep | candidate ready through `OSA_SOLVER_PYTHON` profile | approved for the recorded 2026-05-20 run only | executed / passed | reviewed / accepted | `validation/meep/meep_micro_benchmark_2026-05-20.md` | `docs/optional_solver_approval_records/meep_micro_benchmark_review_2026-05-20.md` | optional manual PyMeep/FDTD smoke evidence | no solver execution by default | no | no | no |
| MPB | candidate ready through `OSA_SOLVER_PYTHON` and `meep.mpb` | approved for the recorded 2026-05-20 run only | executed / passed | reviewed / accepted | `validation/mpb/mpb_micro_benchmark_2026-05-20.md` | `docs/optional_solver_approval_records/mpb_micro_benchmark_review_2026-05-20.md` | optional manual MPB/band-structure smoke evidence | no solver execution by default | no | no | no |
| Elmer | deferred until maintainable install route exists | deferred | not executed | deferred | `validation/elmer/elmer_install_deferred_2026-05-15.md` | `docs/optional_solver_approval_records/elmer_micro_benchmark_deferred.md` | none; not Level 3 | no solver execution by default | no | no | no |

## What This Evidence Proves

- The optional opt-in wrapper can execute the recorded solver-specific smoke
  paths for Gmsh, Optiland, Meep, and MPB when each solver is separately
  approved.
- The wrapper and records preserve no-upload, no-tag, and no-release
  boundaries.
- Default pytest, smoke, release, and quality gates do not execute solvers.
- Evidence records and maintainer review decisions exist for Gmsh, Optiland,
  Meep, and MPB.

## What This Evidence Does Not Prove

- No production-grade physical validation is claimed.
- No production-grade solver validation is claimed.
- No production-grade FDTD validation is claimed.
- No production-grade MPB validation is claimed.
- No production band-structure validation is claimed.
- No formal convergence proof is claimed.
- No optical correctness claim is made.
- No Elmer Level 3 validation is claimed.
- No PyPI readiness decision is implied.

## Recommended Next Step

Use this evidence as one input to the rc8 backend readiness review. Keep Elmer
deferred. Keep PyPI, TestPyPI, tag/release, and `v1.0.0` decisions separately
gated.

