# MPB photonic crystal band

Design intent: Photonic-crystal band preview with eigenmode/k-point semantics.

## Source Model

- Source type: `mode_source`
- Defaulted fields: `mode_index`
- Preview only: `true`

## Monitor Model

- Monitor type: `band_structure`
- Observable intent: `band diagram preview`
- Region: `reciprocal-space k-path`
- Preview only: `true`

## Adapter-Native Mapping

- Adapter: `mpb`
- Source mapping: Time-domain source metadata is interpreted as eigenmode/band context; MPB does not use a driven FDTD source in this preview.
- Monitor mapping: band_structure maps to k-point, band-frequency, or mode metadata.
- Native source terms: `lattice/eigenmode context, mode parity / mode index metadata`
- Native monitor terms: `k-points, num_bands, band frequencies, mode field output plan`
- Supported observables: `band_structure, mode_frequency`
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
