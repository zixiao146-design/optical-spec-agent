# Optical Calculators

The backend includes lightweight local optical design calculators for
design-assist previews. They are deterministic Python helpers and do not run
external solvers, call external LLMs, or access network material databases.

## Calculators

| Calculator | Endpoint | Purpose |
| --- | --- | --- |
| Thin-film stack preview | `POST /api/optics/thin-film` | Normal-incidence transfer-matrix estimate for simple layer stacks. |
| Paraxial lens preview | `POST /api/optics/paraxial-lens` | Thin-lens image distance and magnification estimate. |
| Gaussian beam preview | `POST /api/optics/gaussian-beam` | Rayleigh range, beam radius, curvature, and Gouy phase estimate. |
| Waveguide V-number preview | `POST /api/optics/waveguide-estimate` | Scalar slab waveguide V-number and single-mode orientation. |

## Assumptions

- Thin-film estimates use caller-provided preview n/k values.
- Thin-film calculation currently uses normal-incidence transfer matrix for
  the numerical estimate.
- Paraxial lens estimates assume small angles, no aberrations, and no aperture
  effects.
- Gaussian beam estimates assume ideal fundamental Gaussian beams in a medium
  with refractive index 1.0.
- Waveguide estimates use scalar symmetric slab-waveguide orientation only.

## Limitations

These calculators are preview/design-assist tools. They are useful for local
orientation, UI demos, and backend task sessions, but they are not validated
production simulation workflows.

- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
- No external solver is executed.
- No external LLM is called.
- Users must verify material data, boundary conditions, and numerical methods
  before making physical conclusions.

## Examples

Example requests live under `examples/optics_calculators/`.

