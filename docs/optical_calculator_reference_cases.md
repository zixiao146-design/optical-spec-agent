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

### Fiber Coupling Gaussian Overlap

The fiber-coupling preview uses scalar circular Gaussian mode overlap:

- `eta_w = (2 w_in w_f / (w_in^2 + w_f^2))^2`
- lateral offset and angular tilt are independent Gaussian penalty factors
- total efficiency is bounded to `[0, 1]`

Reference cases cover perfect waist match, waist mismatch, lateral offset loss,
and angular tilt loss. Perfect match gives coupling efficiency near `1.0`; the
other three reduce the estimate.

### Jones Polarization

The polarization preview uses ideal Jones vectors and ideal passive elements:

- linear polarization: `[cos(theta), sin(theta)]`
- ideal polarizer projection: `P = |a><a|`
- ideal waveplate retardance in rotated local axes

Reference cases cover horizontal/vertical linear states, Malus-like polarizer
projection, half-wave plate rotation, and quarter-wave plate phase retardance.

## Failure Modes

The calculators reject invalid local inputs such as negative wavelength, zero
physical layer thickness, invalid refractive index, invalid sweep point count,
unguided waveguide index combinations, non-finite fiber-coupling inputs,
malformed Jones vectors, and non-finite Jones angles or retardance. API
endpoints return stable error responses with safety flags preserved.

## Artifacts

Reference JSON cases live under `examples/optics_reference_cases/`.
Backend capability reporting in `docs/backend_capability_report.md` lists these
reference cases alongside calculator endpoints and failure modes.
The maintainer backend evidence review pack also includes calculator reference
case coverage; generate it with `scripts/generate_backend_evidence_pack.py` or
smoke it with `./scripts/smoke_backend_evidence_pack.sh`.

## Safety

- No external solver is executed.
- No external LLM is called.
- No network material database is queried.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.

All calculator reference cases feed the backend validation maturity summary as
`sanity_checked_preview` evidence. The summary is exposed by
`GET /api/backend-validation-maturity` and documented in
[`backend_validation_maturity_matrix.md`](backend_validation_maturity_matrix.md).
