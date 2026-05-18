# Optiland lens image plane

Design intent: Ray-bundle source and image-plane/focal-spot preview metadata.

## Source Model

- Source type: `ray_bundle`
- Defaulted fields: `wavelength_nm, incidence_direction`
- Preview only: `true`

## Monitor Model

- Monitor type: `image_plane`
- Observable intent: `image distance and magnification preview`
- Region: `paraxial image plane`
- Preview only: `true`

## Adapter-Native Mapping

- Adapter: `optiland`
- Source mapping: ray_bundle maps to object/ray-bundle metadata for ray optics previews.
- Monitor mapping: image_plane maps to image-plane, spot, or ray-fan preview metadata.
- Native source terms: `object point/field metadata, ray bundle, Gaussian beam note`
- Native monitor terms: `image plane, focal spot, spot diagram plan, ray fan plan`
- Supported observables: `image_plane, ray_fan`
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
