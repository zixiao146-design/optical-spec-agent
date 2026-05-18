# Gmsh mesh region

Design intent: Geometry-only source/monitor annotations as mesh regions and physical groups.

## Source Model

- Source type: `plane_wave`
- Defaulted fields: `wavelength_nm, polarization`
- Preview only: `true`

## Monitor Model

- Monitor type: `unknown`
- Observable intent: `mesh region / physical group preview`
- Region: `source and monitor physical groups`
- Preview only: `true`

## Adapter-Native Mapping

- Adapter: `gmsh`
- Source mapping: Gmsh does not execute optical sources; source intent is attached as geometry/mesh annotation metadata.
- Monitor mapping: Monitor intent maps to physical group / mesh region annotations, not optical fields.
- Native source terms: `geometry comments, mesh-size hints, source-region annotation`
- Native monitor terms: `Physical Surface/Volume groups, monitor-region annotation`
- Supported observables: `mesh_region`
- Unsupported observables: `none`

## Preview Artifact Expectations

The expected fragments file records source, monitor, observable, and adapter-native
terms that must appear in generated mapping metadata. These fragments are checked
by `scripts/check_adapter_native_golden.py`.

## Safety Boundary

- No solver execution is performed.
- No external LLM is called.
- The mapping is preview/design-assist metadata only.
- It is not a real solver monitor result.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
