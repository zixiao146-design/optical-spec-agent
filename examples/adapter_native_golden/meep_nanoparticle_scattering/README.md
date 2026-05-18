# Meep nanoparticle scattering

Design intent: Broadband nanoparticle scattering preview with plane-wave-like illumination.

## Source Model

- Source type: `plane_wave`
- Defaulted fields: `wavelength_range_nm, polarization, incidence_direction`
- Preview only: `true`

## Monitor Model

- Monitor type: `scattering_spectrum`
- Observable intent: `scattering/extinction spectrum preview`
- Region: `closed flux box or equivalent far-field proxy around nanoparticle`
- Preview only: `true`

## Adapter-Native Mapping

- Adapter: `meep`
- Source mapping: plane_wave maps to Meep source metadata; broadband bands map to GaussianSource/broadband pulse preview terms.
- Monitor mapping: scattering_spectrum maps to Meep flux/DFT monitor metadata only.
- Native source terms: `mp.Source, GaussianSource/broadband pulse metadata, planewave-like current source placeholder`
- Native monitor terms: `flux monitor metadata, DFT field monitor metadata, closed flux box / incident-flux normalization plan`
- Supported observables: `scattering_spectrum, extinction_spectrum`
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
