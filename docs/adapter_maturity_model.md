# Adapter Maturity Model

## Purpose

This document defines maturity levels for adapter families before v1.0. It
separates local artifact evidence from optional solver-backed validation and
from any future production validation claim.

## Maturity Levels

### Level 0 - Registry only

- Adapter is registered or named.
- No stable local artifact evidence yet.

### Level 1 - Local artifact preview

- Adapter can generate local script, config, or preview artifacts.
- No external solver execution is required.
- No solver-backed correctness claim is made.

### Level 2 - Golden/evidence fixtures

- Adapter has fixed input fixtures.
- Generated output has stable fragment or metadata regression tests.
- No solver execution is required.

### Level 3 - Optional manual solver validation

- An open-source solver-backed validation path exists.
- It is skipped by default.
- It is manually enabled only.
- A report template or recorded manual validation exists.
- It is still not automatically production-grade.

### Level 4 - Reproducible solver-backed benchmark

- Solver-backed validation can be repeated.
- High-level expected results are documented.
- Environment assumptions are documented.
- The scope still requires careful review.

### Level 5 - Production-grade validation candidate

- Stronger physical validation standard.
- Reproducibility expectations.
- Benchmark coverage.
- Limitations documented.
- Still subject to maintainer approval before any production claim.

## Current Adapter Maturity Table

| Adapter | Current maturity level | Rationale | Evidence files/tests | External solver required by default | Solver-backed validation run | Production-grade physical validation claimed | Next maturity step |
|---|---|---|---|---|---|---|---|
| Meep | Level 3 - Optional manual solver validation | Registered and CLI-visible; generates local Meep Python preview artifacts with diagnostics and fixture coverage. A narrow opt-in pilot generated the adapter preview artifact and executed a tiny project-owned PyMeep validation path. Default tests, smoke, quality gates, CI, and release validation still do not run Meep. | `tests/test_meep_adapter.py`, `tests/test_adapter_evidence_fixtures.py`, `tests/fixtures/adapter_golden/meep_missing_wavelength_expected_fragments.txt`, `docs/meep_optional_validation_pilot.md`, `docs/meep_level3_readiness.md`, `validation/meep/meep_validation_pilot_2026-05-14.md` | no | yes, only for the 2026-05-14 opt-in pilot | no | Define a reproducible solver-backed benchmark before considering Level 4. |
| Gmsh | Level 3 - Optional manual solver validation | Registered and CLI-visible; generates `.geo` scaffold evidence from fixed fixtures. A narrow opt-in pilot processed the project/adapter `.geo` artifact with Gmsh and recorded manual validation evidence. Default tests, smoke, quality gates, and release validation still do not run Gmsh. | `examples/specs/gmsh_preview.json`, `tests/fixtures/adapter_golden/gmsh/`, `tests/test_adapter_family_evidence.py`, `docs/gmsh_optional_validation_pilot.md`, `docs/gmsh_level3_readiness.md`, `validation/gmsh/gmsh_validation_pilot_2026-05-14.md` | no | yes, only for the 2026-05-14 opt-in pilot | no | Define a reproducible solver-backed benchmark before considering Level 4. |
| Elmer | Level 2 - Golden/evidence fixtures, Level-3-ready | Registered and CLI-visible; generates `.sif` scaffold evidence, with mesh and boundary assumptions still explicit limitations. The Level-3-ready path is documented, and the optional Elmer script exists, but ElmerSolver is not installed locally. The 2026-05-15 conda-forge/Homebrew install attempt was deferred, and no completed manual validation report exists yet. | `examples/specs/elmer_preview.json`, `tests/fixtures/adapter_golden/elmer/`, `tests/test_adapter_family_evidence.py`, `docs/elmer_optional_validation_pilot.md`, `docs/elmer_level3_readiness.md`, `scripts/run_optional_elmer_validation.sh`, `validation/elmer/elmer_install_deferred_2026-05-15.md` | no | no | no | Install ElmerSolver later through a maintainable package route and run explicit opt-in validation before claiming Level 3. |
| MPB | Level 3 - Optional manual solver validation | Registered and CLI-visible; generates MPB Python scaffold evidence for band-structure style workflows. A narrow opt-in pilot generated the adapter scaffold and executed a tiny project-owned MPB/PyMeep validation path through `meep.mpb`. MPB CLI is not required. | `examples/specs/mpb_preview.json`, `tests/fixtures/adapter_golden/mpb/`, `tests/test_adapter_family_evidence.py`, `docs/mpb_optional_validation_pilot.md`, `docs/mpb_level3_readiness.md`, `validation/mpb/mpb_validation_pilot_2026-05-14.md` | no | yes, only for the 2026-05-14 opt-in pilot | no | Define a reproducible solver-backed benchmark before considering Level 4. |
| Optiland | Level 3 - Optional manual backend validation | Registered and CLI-visible; generates Optiland scaffold evidence while lens prescription schema remains incomplete. A narrow opt-in pilot generated the adapter scaffold and executed a tiny project-owned Optiland validation path. | `examples/specs/optiland_preview.json`, `tests/fixtures/adapter_golden/optiland/`, `tests/test_adapter_family_evidence.py`, `docs/optiland_optional_validation_pilot.md`, `docs/optiland_level3_readiness.md`, `validation/optiland/optiland_validation_pilot_2026-05-14.md` | no | yes, only for the 2026-05-14 opt-in pilot | no | Define a reproducible backend-backed benchmark before considering Level 4. |

## Non-goals

- No default external solver execution.
- No production-grade physical validation claim.
- No formal convergence proof.
- No proprietary solver default dependency.
- No PyPI/TestPyPI publication in this task.

## Gmsh Level 3 Boundary

Gmsh Level 3 is limited to the optional manual validation report recorded in
`validation/gmsh/gmsh_validation_pilot_2026-05-14.md`. It means Gmsh processed a
project/adapter-generated `.geo` artifact after explicit maintainer opt-in. It
does not make Gmsh a default dependency, does not add Gmsh to default pytest,
smoke, quality gates, or release validation, and does not claim production-grade
physical validation or a formal convergence proof.

## Meep Level 3 Boundary

Meep Level 3 is limited to the optional manual validation report recorded in
`validation/meep/meep_validation_pilot_2026-05-14.md`. It means PyMeep executed
a tiny project-owned validation path after explicit maintainer opt-in and after
generating an adapter Meep preview artifact. It does not make Meep a default
dependency, does not add Meep to default pytest, smoke, quality gates, CI, or
release validation, and does not claim production-grade physical validation or a
formal convergence proof.

## MPB Level 3 Boundary

MPB Level 3 is limited to the optional manual validation report recorded in
`validation/mpb/mpb_validation_pilot_2026-05-14.md`. It means MPB/PyMeep
executed a tiny project-owned validation path after explicit maintainer opt-in
and after generating an adapter MPB preview artifact. It does not make MPB a
default dependency, does not require MPB CLI, does not add MPB to default
pytest, smoke, quality gates, CI, or release validation, and does not claim
production-grade physical validation or a formal convergence proof.

## Optiland Level 3 Boundary

Optiland Level 3 is limited to the optional manual validation report recorded in
`validation/optiland/optiland_validation_pilot_2026-05-14.md`. It means Optiland
executed a tiny project-owned validation path after explicit maintainer opt-in
and after generating an adapter Optiland preview artifact. It does not make
Optiland a default dependency, and it does not make Optiland a default
pytest, smoke, quality gates, CI, or release validation requirement. It does not claim
production-grade optical validation or a formal convergence proof.

In short: this evidence does not make Optiland a default dependency.

## Elmer Level-3-ready Boundary

Elmer remains Level 2, but the Level-3-ready path is documented in
`docs/elmer_optional_validation_pilot.md` and `docs/elmer_level3_readiness.md`.
The default script `scripts/run_optional_elmer_validation.sh` checks
`ElmerSolver` availability and fixture presence without executing Elmer.
ElmerSolver is not installed locally, the 2026-05-15 package-manager install
attempt is deferred, no completed manual validation report has been recorded,
and Level 3 is not achieved. This does not make Elmer a default
dependency, does not add Elmer to default pytest, smoke, quality gates, CI, or
release validation, and does not claim production-grade physical validation or a
formal convergence proof.

In short: this evidence does not make Elmer a default dependency.
