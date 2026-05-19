# Design Requirement Templates

This document describes the local requirement-template layer that maps natural-language optical design goals into deterministic optical language. It is backend functionality for Agent Studio and the Agent Command Center.

Current public prerelease: `v0.9.0rc6`
Current main release draft: `0.9.0rc7`
API contract version: `0.1`
PyPI: not published

## Purpose

Requirement templates make the path clearer:

natural language goal -> optical language -> design case -> expected tool calls -> preview artifacts -> evidence boundary.

This mapping is deterministic heuristic code. It is not an external LLM call, does not access the network, and does not execute external solvers.

## Templates

| Template | Optical intent | Expected tool/calculator path |
| --- | --- | --- |
| `thin_film_ar_coating` | thin-film anti-reflection coating preview | `optics.thin_film.spectrum`, quarter-wave AR helper |
| `gaussian_beam_focus` | Gaussian beam propagation/focus preview | `optics.gaussian_beam.series`, focus helper |
| `slab_waveguide_single_mode` | slab waveguide single-mode estimate | `optics.waveguide.sweep`, single-mode range helper |
| `paraxial_lens_imaging` | paraxial lens imaging preview | `optics.paraxial.two_lens_relay`, thin-lens helper |
| `photonic_crystal_band_preview` | photonic crystal band preview | MPB adapter-preview path |
| `dielectric_metasurface_preview` | dielectric metasurface preview | Meep/Gmsh adapter-preview path |
| `nanoparticle_plasmonics` | nanoparticle scattering preview | Meep/Gmsh adapter-preview path |

## Matching Rules

The matcher uses local keyword heuristics only. Examples:

- `coating`, `anti-reflection`, `thin film`, `增透`, `镀膜` -> `thin_film_ar_coating`
- `Gaussian`, `beam waist`, `Rayleigh`, `高斯光束`, `光腰` -> `gaussian_beam_focus`
- `waveguide`, `single mode`, `波导`, `单模` -> `slab_waveguide_single_mode`
- `lens`, `imaging`, `relay`, `透镜`, `成像` -> `paraxial_lens_imaging`
- `photonic crystal`, `band diagram`, `光子晶体`, `能带` -> `photonic_crystal_band_preview`
- `metasurface`, `metalens`, `超表面`, `超透镜` -> `dielectric_metasurface_preview`
- `nanoparticle`, `plasmonic`, `scattering`, `纳米颗粒`, `散射` -> `nanoparticle_plasmonics`

Unknown goals return a low-confidence safe result with missing inputs and recommended clarification steps.

## Expected Tool Calls

Every matched template expects:

- `requirements.match_template`
- `requirements.extract_optical_intent`
- `optical_language.infer_source_monitor`
- `optical_language.diagnose_missing_inputs`
- `material_catalog.suggest`
- `example_registry.load` when a local design case is available
- `agent_trace.build`
- `workflow_plan.preview`
- `adapter_preview.generate`

Calculator-backed cases add the relevant local optical calculator call. These calls are internal Python preview/design-assist functions.

Each template also includes:

- `source_model`
- `monitor_model`
- `required_source_inputs`
- `required_monitor_inputs`
- `default_source_assumptions`
- `default_monitor_assumptions`

These fields make source, monitor, and observable assumptions visible before
workflow or adapter preview.

## Safety Boundaries

- No external solver is executed by default.
- No external LLM is called by default.
- No network material lookup is performed.
- No PyPI/TestPyPI upload, tag, or release action is exposed.
- Outputs are preview/design-assist only.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
