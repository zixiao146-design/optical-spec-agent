# Adapter-Native Source/Monitor Mapping

Current public prerelease: v0.9.0rc6. Current main development version:
`0.9.0rc7.dev0`.

This document explains how local optical source, monitor, and observable intent
is mapped into each adapter family's native preview vocabulary. The mapping is
preview/design-assist metadata only. No external solver is executed, no external
LLM is called, no upload or release action is available, and no production-grade
physical validation or formal convergence proof is claimed.

## Purpose

The backend now follows this deterministic path:

natural-language goal -> source/monitor inference -> observable diagnostics ->
adapter-native preview mapping -> adapter preview metadata -> tool-call ledger
-> next action recommendations.

The mapping tells maintainers what a real solver setup would need later; it is
not a real solver monitor result.

Golden preview cases for the five registered adapter families are documented in
`docs/adapter_native_golden_cases.md` and stored under
`examples/adapter_native_golden/`. They lock expected source, monitor,
observable, and adapter-native fragments without executing solvers.

## Meep

- Plane-wave-like source intent maps to Meep source metadata.
- Broadband wavelength bands map to GaussianSource or broadband pulse metadata
  in preview form.
- Scattering or extinction spectra map to flux / DFT flux monitor metadata.
- Near-field and far-field requests map to DFT field / far-field monitor
  metadata.
- Real scattering, extinction, near-field, far-field, or phase-profile results
  require explicit Meep execution, which this backend does not do by default.

## MPB

- Time-domain source semantics do not apply directly to MPB.
- Mode-source or photonic-crystal goals map to eigenmode / band context
  metadata.
- Band-structure observables map to k-point and band-frequency metadata.
- Real band frequencies or mode fields require explicit MPB execution.

## Gmsh

- Gmsh does not compute optical observables by itself.
- Source and monitor intent is preserved as geometry, mesh-region, and
  Physical Surface / Volume annotation metadata.
- Mesh regions are preview-supported; optical fields, spectra, and mode results
  require another solver after explicit approval.

## Elmer

- Source and monitor intent maps to FEM source, boundary-condition, solver
  section, and output placeholders.
- Real FEM optical/electromagnetic fields require explicit ElmerSolver
  execution. Elmer remains Level 2 + Level-3-ready; this task does not change
  Elmer to Level 3.

## Optiland

- Gaussian or ray-style source intent maps to object/ray-bundle metadata.
- Focal spot, image plane, and ray fan observables map to raytrace output
  metadata.
- Real raytrace results require explicit Optiland execution if later approved.

## Tool-Call Reality

Agent sessions record `optical_language.diagnose_observable` and
`optical_language.map_source_monitor_to_adapter` as executed internal Python
tool calls. External solver records remain `executed=false` and blocked or
explicit-approval-only.

`scripts/check_adapter_native_golden.py` verifies the Meep, MPB, Gmsh, Elmer,
and Optiland golden preview cases through local API/TestClient calls.

## Safety Boundary

No production-grade physical validation is claimed. No formal convergence proof
is claimed. Adapter-native source/monitor mapping is local preview metadata,
not proof that an external solver run has occurred.
