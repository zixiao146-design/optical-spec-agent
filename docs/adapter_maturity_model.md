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
| Meep | Level 2 - Golden/evidence fixtures | Registered and CLI-visible; generates local Meep Python preview artifacts with diagnostics and fixture coverage. Explicit Meep execution remains separate and manual. | `tests/test_meep_adapter.py`, `tests/test_adapter_evidence_fixtures.py`, `tests/fixtures/adapter_golden/meep_missing_wavelength_expected_fragments.txt` | no | no for the default rc5.dev0 path | no | Define optional manual solver validation reports without making Meep a release gate. |
| Gmsh | Level 2 - Golden/evidence fixtures, with pilot path toward Level 3 | Registered and CLI-visible; generates `.geo` scaffold evidence from fixed fixtures. This sprint adds an opt-in Gmsh pilot path, but default tests do not run Gmsh. | `examples/specs/gmsh_preview.json`, `tests/fixtures/adapter_golden/gmsh/`, `tests/test_adapter_family_evidence.py`, `docs/gmsh_optional_validation_pilot.md` | no | no | no | Use the optional pilot to record a manual validation report after explicit maintainer opt-in. |
| Elmer | Level 2 - Golden/evidence fixtures | Registered and CLI-visible; generates `.sif` scaffold evidence, with mesh and boundary assumptions still explicit limitations. | `examples/specs/elmer_preview.json`, `tests/fixtures/adapter_golden/elmer/`, `tests/test_adapter_family_evidence.py` | no | no | no | Define richer FEM mesh/boundary contracts before optional solver validation. |
| MPB | Level 2 - Golden/evidence fixtures | Registered and CLI-visible; generates MPB Python scaffold evidence for band-structure style workflows. | `examples/specs/mpb_preview.json`, `tests/fixtures/adapter_golden/mpb/`, `tests/test_adapter_family_evidence.py` | no | no | no | Define optional MPB validation fixtures and high-level expected diagnostics. |
| Optiland | Level 2 - Golden/evidence fixtures | Registered and CLI-visible; generates Optiland scaffold evidence while lens prescription schema remains incomplete. | `examples/specs/optiland_preview.json`, `tests/fixtures/adapter_golden/optiland/`, `tests/test_adapter_family_evidence.py` | no | no | no | Extend lens prescription schema before solver-backed validation claims. |

## Non-goals

- No default external solver execution.
- No production-grade physical validation claim.
- No formal convergence proof.
- No proprietary solver default dependency.
- No PyPI/TestPyPI publication in this task.
