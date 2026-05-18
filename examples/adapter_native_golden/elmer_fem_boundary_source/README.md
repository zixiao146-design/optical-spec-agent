# Elmer FEM boundary/source

Design intent: FEM boundary/source placeholders and output-section preview metadata.

## Source Model

- Source type: `mode_source`
- Defaulted fields: `wavelength_nm, mode_index, polarization`
- Preview only: `true`

## Monitor Model

- Monitor type: `mode_overlap`
- Observable intent: `V-number and single-mode likelihood preview`
- Region: `slab core/cladding cross-section`
- Preview only: `true`

## Adapter-Native Mapping

- Adapter: `elmer`
- Source mapping: mode_source maps to FEM source/boundary placeholders.
- Monitor mapping: mode_overlap maps to FEM solver/output section placeholders.
- Native source terms: `Boundary Condition placeholders, Body Force/source section metadata`
- Native monitor terms: `ResultOutputSolver placeholder, field/output variable plan`
- Supported observables: `mode_overlap, mode_frequency`
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
