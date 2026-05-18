# Observable Diagnostics

Current public prerelease: v0.9.0rc6. Current main development version:
`0.9.0rc7.dev0`.

Observable diagnostics translate inferred monitor intent into explicit
preview-supported observable metadata. They list required inputs, default
assumptions, adapter compatibility, and whether a real result would require
external solver execution. No external solver is executed by these diagnostics.
No external LLM is called.

## Observable Taxonomy

- `scattering_spectrum`: scattering spectrum preview for FDTD-style workflows.
- `extinction_spectrum`: extinction spectrum preview for nanoparticle cases.
- `reflectance`: reflection observable for thin-film or FDTD monitor previews.
- `transmittance`: transmission observable for thin-film or FDTD monitor previews.
- `absorptance`: loss estimate derived from R/T/A preview semantics.
- `near_field`: local field metadata, usually DFT field style in Meep contexts.
- `far_field`: far-field projection metadata.
- `dft_field`: DFT field monitor metadata.
- `band_structure`: MPB-style band / k-point metadata.
- `mode_frequency`: eigenmode frequency metadata.
- `mode_overlap`: waveguide or mode-source overlap metadata.
- `focal_spot`: Gaussian beam or raytrace spot metadata.
- `image_plane`: paraxial or raytrace image-plane metadata.
- `ray_fan`: raytrace fan metadata.
- `phase_profile`: metasurface phase or wavefront metadata.
- `mesh_region`: Gmsh physical-group / mesh-region metadata.
- `unknown`: stable fallback when the goal is ambiguous.

## Required Inputs

Each diagnostic carries required inputs such as wavelength range, polarization,
monitor region, k-point path, image plane, mode index, or geometry region. When
the goal omits a value, default assumptions are reported rather than silently
claiming a real result.

## Preview vs Real Result

Preview-supported means the backend can describe the observable, attach it to
an adapter preview, and record it in the tool-call ledger. A real field,
spectrum, raytrace, or band result usually requires explicit external solver
execution and is not produced by default.

The adapter-native golden cases in `examples/adapter_native_golden/` check that
observable diagnostics survive adapter mapping for Meep nanoparticle
scattering, MPB photonic-crystal bands, Gmsh mesh regions, Elmer FEM
placeholders, and Optiland image-plane previews.

## Safety Boundary

No production-grade physical validation is claimed. No formal convergence proof
is claimed. Observable diagnostics are local design-assist metadata and should
be checked before any optional solver setup.
