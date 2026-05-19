# Optical Language Source and Monitor

This document records the local, deterministic source/monitor inference used by
Agent Studio backend previews.

Current public prerelease: v0.9.0rc7. Current main development version:
`0.9.0rc8.dev0`.

## Purpose

Natural-language optical goals are now mapped into preview source and monitor
metadata before an agent session creates workflow, adapter, calculator, or
evidence artifacts. This makes the path explicit:

natural language goal -> optical intent -> source model -> monitor model ->
observable -> observable diagnostics -> adapter-native source/monitor mapping ->
missing-input diagnostics.

No external solver is executed. No external LLM is called. The metadata is
preview/design-assist only.

## Source Types

- `plane_wave`: normal or angled plane-wave-like illumination metadata.
- `gaussian_beam`: scalar paraxial Gaussian beam metadata.
- `mode_source`: eigenmode or guided-mode source/context metadata.
- `broadband_pulse`: reserved for future broadband source previews.
- `ray_bundle`: first-order ray bundle for paraxial lens previews.
- `unknown`: used when the goal is too ambiguous.

## Monitor Types

- `scattering_spectrum`: scattering or extinction spectrum preview.
- `reflectance_transmittance`: R/T/A preview for thin-film stacks.
- `near_field`: local field preview metadata.
- `far_field`: far-field preview metadata.
- `mode_overlap`: mode-overlap or V-number preview metadata.
- `focal_spot`: beam waist/focal spot preview.
- `image_plane`: paraxial image-plane estimate.
- `phase_profile`: metasurface phase/far-field preview metadata.
- `band_structure`: photonic-crystal band-structure preview metadata.
- `unknown`: used when the observable is not clear.

## Default Examples

- `nanoparticle_plasmonics`: plane-wave-like source, 400-900 nm default band,
  `linear_x` polarization, scattering/extinction spectrum monitor.
- `thin_film_ar_coating`: normal-incidence plane wave, 400-800 nm sweep,
  reflectance/transmittance monitor.
- `gaussian_beam_focus`: Gaussian beam source and focal-spot monitor.
- `slab_waveguide_single_mode`: mode-source metadata and mode/V-number monitor.
- `photonic_crystal_band_preview`: eigenmode context and band-structure monitor.
- `paraxial_lens_imaging`: ray-bundle source and image-plane monitor.
- `dielectric_metasurface_preview`: plane-wave source and phase/far-field
  preview monitor.

## Safety Boundary

Monitor definitions are metadata only. They are not external solver monitor
results. They do not claim production-grade physical validation or formal
convergence proof.

See also:

- `docs/observable_diagnostics.md` for observable taxonomy, required inputs,
  and preview-vs-real-result boundaries.
- `docs/adapter_native_source_monitor_mapping.md` for Meep, MPB, Gmsh, Elmer,
  and Optiland preview mapping semantics.
