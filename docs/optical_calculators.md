# Optical Calculators

The backend includes lightweight local optical design calculators for
design-assist previews. They are deterministic Python helpers and do not run
external solvers, call external LLMs, or access network material databases.

## Calculators

| Calculator | Endpoint | Purpose |
| --- | --- | --- |
| Thin-film stack preview | `POST /api/optics/thin-film` | Normal-incidence transfer-matrix estimate for simple layer stacks. |
| Thin-film spectrum preview | `POST /api/optics/thin-film-spectrum` | Wavelength sweep of reflectance/transmittance/absorptance estimates. |
| Quarter-wave AR helper | `POST /api/optics/quarter-wave-ar` | Single-layer anti-reflection starting point from `sqrt(n0 * ns)`. |
| Paraxial lens preview | `POST /api/optics/paraxial-lens` | Thin-lens image distance and magnification estimate. |
| Paraxial system preview | `POST /api/optics/paraxial-system` | Compose free-space and thin-lens ABCD elements. |
| Two-lens relay preview | `POST /api/optics/two-lens-relay` | Sequential ideal thin-lens relay estimate. |
| Gaussian beam preview | `POST /api/optics/gaussian-beam` | Rayleigh range, beam radius, curvature, and Gouy phase estimate. |
| Gaussian beam series | `POST /api/optics/gaussian-beam-series` | Propagation samples over a z range. |
| Gaussian beam focus | `POST /api/optics/gaussian-beam-focus` | Thin-lens diffraction-limited focus estimate. |
| Waveguide V-number preview | `POST /api/optics/waveguide-estimate` | Scalar slab waveguide V-number and single-mode orientation. |
| Waveguide sweep | `POST /api/optics/waveguide-sweep` | V-number samples over core thickness. |
| Waveguide single-mode range | `POST /api/optics/waveguide-single-mode-range` | Scalar slab thickness range for likely `V < pi` behavior. |

## Assumptions

- Thin-film estimates use caller-provided preview n/k values.
- Thin-film calculation currently uses normal-incidence transfer matrix for
  the numerical estimate.
- Thin-film spectrum sweeps do not include material dispersion unless the
  caller supplies wavelength-specific n/k in separate calls.
- Quarter-wave AR is a single-layer, normal-incidence starting point.
- Paraxial lens estimates assume small angles, no aberrations, and no aperture
  effects.
- Paraxial system and two-lens relay helpers use ideal thin lenses and
  homogeneous free-space sections.
- Gaussian beam estimates assume ideal fundamental Gaussian beams in a medium
  with refractive index 1.0.
- Gaussian focus assumes a collimated Gaussian at an ideal thin lens; M^2,
  aperture clipping, and aberrations are not included.
- Waveguide estimates use scalar symmetric slab-waveguide orientation only.
- Waveguide sweeps and single-mode ranges are scalar orientation helpers, not
  vector eigenmode solves.

## Result summaries

Calculator responses include `status`, `result`, `assumptions`, `diagnostics`,
`warnings`, `limitations`, `quality`, and conservative safety flags. The
`quality.quality_level` is `sanity_checked_preview`, and
`quality.reference_case` is populated for local formula sanity checks such as
single-interface Fresnel reflection, quarter-wave AR, Gaussian Rayleigh range,
thin-lens 1:1 imaging, and slab-waveguide V-number. Sweep responses include
sample counts and compact summary fields so an agent session can show what was
actually computed without claiming physical validation.

## Reference formulas

- Thin-film single interface: `R = |(n0 - ns) / (n0 + ns)|^2`.
- Quarter-wave AR: `n_coating = sqrt(n0 * ns)` and
  `d = lambda / (4 * n_coating)`.
- Gaussian beam: `z_R = pi * w0^2 / lambda` and
  `w(z_R) = w0 * sqrt(2)`.
- Thin lens: `1/f = 1/s + 1/s'`.
- ABCD free space: `[[1, d], [0, 1]]`; thin lens:
  `[[1, 0], [-1/f, 1]]`.
- Waveguide V-number:
  `V = (2*pi/lambda) * thickness * sqrt(n_core^2 - n_clad^2)`.

Reference case details live in
[`optical_calculator_reference_cases.md`](optical_calculator_reference_cases.md).

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
