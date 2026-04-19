# Release v0.2.0 — Spec Hardening + Meep Adapter Preview

## Overview

v0.2.0 is the transition from "spec-only agent" to "spec + first adapter preview". The core spec layer has been hardened with a stability policy, expanded benchmarks, and stricter validation. A Meep adapter preview demonstrates the spec → solver script path for the first time.

**This is NOT a full solver integration.** The Meep adapter generates Python scripts but does not execute them or parse results.

## What's new

### Spec hardening
- **Schema stability policy** (`docs/schema_stability.md`): 20+ core fields frozen for the 0.x series, append-only compatibility rules
- **Expanded benchmarks**: 8 → 16 golden cases covering grating, multilayer, Mie scattering, coupled system, V-antenna, Lorentzian fitting, photonic crystal, rod-on-film
- **Stricter validation**: FWHM/T2 without spectrum → error (was warning), FDTD/FEM minimum executable checks, nanoparticle_on_film geometry severity escalation, physical_system + structure_type combination validation
- **9 new validator tests** (85 → 99 total)

### Meep adapter preview
- **New package** `adapters/meep/`: translator (OpticalSpec → MeepInputModel), template renderer (MeepInputModel → Python script)
- **CLI**: `optical-spec meep-generate <spec.json> -o <script.py>`
- **Scope**: nanoparticle_on_film + fdtd + meep + plane_wave + scattering_spectrum only
- **14 adapter tests**: success cases, rejection cases, missing field handling
- **Generated scripts**: syntax-validated with Meep 1.33.0-beta, import-verified on macOS

### Data workflow design
- **Extraction workflow** (`docs/optics_extraction_workflow.md`): design for web search → optical structure extraction pipeline
- **ExtractionRecord model** (`models/extraction.py`): Pydantic schema for structured extraction results

## Current limitations

- Meep adapter: **script generation only** — no execution, no result parsing, no visualization
- Meep adapter: only `nanoparticle_on_film` + `plane_wave` + `scattering_spectrum` supported
- Material model: simplified single-Drude (not production-grade Johnson-Christy)
- No adapters for other solvers (MPB, Gmsh, Elmer, Optiland)
- Parser remains rule-based (no LLM integration)
- Generated scripts use fixed time steps and simplified flux monitor placement

## Next focus

- Meep adapter v0.2: execution wrapper, result parsing, material model upgrade
- Expand Meep adapter to support sweep result collection
- Consider TFSF source support for cleaner scattering cross-section computation

## Migration from v0.1.x

- All API surfaces are backward-compatible
- `validation_status.errors` may contain new entries (stricter rules) — specs that previously passed may now have errors
- Golden benchmark cases updated — run `python benchmarks/run_benchmark.py --update` to sync
