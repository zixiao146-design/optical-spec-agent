# Optical Calculator Reference Cases

The backend optical calculators now include local numeric sanity checks. These
checks make the preview/design-assist calculators more useful, but they are not
production-grade physical validation and are not formal convergence proofs.

## Quality Fields

Calculator responses expose:

- `quality.quality_level`: currently `sanity_checked_preview`
- `quality.reference_case`: formula sanity case when applicable
- `quality.assumptions`
- `quality.limitations`
- `quality.warnings`
- `quality.valid_input_range`
- `production_grade_validation_claimed=false`
- `formal_convergence_proof_claimed=false`

The same response also includes top-level `assumptions`, `limitations`, and
`warnings` for API/frontend rendering.

## Reference Cases

### Thin-film Single Interface

For a normal-incidence air to glass interface:

`R = |(n0 - ns) / (n0 + ns)|^2`

With `n0=1.0` and `ns=1.5`, the expected reflectance is approximately `0.04`.
For a lossless interface, `R + T ~= 1`.

### Quarter-wave AR Coating

For an ideal single-layer anti-reflection starting point:

- `n_coating = sqrt(n0 * ns)`
- `d = lambda / (4 * n_coating)`

At `lambda=550 nm`, `n0=1.0`, and `ns=1.5`, the preview target reflectance is
near zero under the simplified normal-incidence model.

### Gaussian Beam

The Gaussian beam sanity checks use:

- `z_R = pi * w0^2 / lambda`
- `w(z) = w0 * sqrt(1 + (z / z_R)^2)`
- `w(0) = w0`
- `w(z_R) = w0 * sqrt(2)`

The implementation assumes an ideal fundamental Gaussian beam and paraxial
propagation in a medium with refractive index 1.0.

### Paraxial Lens

The thin-lens sanity case uses:

`1/f = 1/s + 1/s'`

For `f=50 mm` and `s=100 mm`, the expected image distance is `s'=100 mm` and
the magnification is `-1`.

ABCD reference matrices:

- Free space: `[[1, d], [0, 1]]`
- Thin lens: `[[1, 0], [-1/f, 1]]`

The two-lens relay sanity check covers the simplified `4f` convention where
`f1=f2`, `separation=f1+f2`, and the object is at the front focal plane.

### Waveguide V-number

The scalar slab-waveguide sanity check uses:

`V = (2*pi / lambda) * thickness * sqrt(n_core^2 - n_clad^2)`

The single-mode orientation is preview-only and uses `V < pi`. If
`n_core <= n_clad`, the calculator returns a stable invalid-input diagnostic or
raises `ValueError` in pure Python helpers.

## Failure Modes

The calculators reject invalid local inputs such as negative wavelength, zero
physical layer thickness, invalid refractive index, invalid sweep point count,
and unguided waveguide index combinations. API endpoints return stable error
responses with safety flags preserved.

## Artifacts

Reference JSON cases live under `examples/optics_reference_cases/`.

## Safety

- No external solver is executed.
- No external LLM is called.
- No network material database is queried.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
