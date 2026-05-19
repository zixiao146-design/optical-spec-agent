# Fiber Coupling and Polarization Reference Cases

The fiber coupling and polarization preview calculators now have local
reference sanity cases, matching the evidence level used for the thin-film,
paraxial, Gaussian beam, and waveguide helpers.

These cases are preview/design-assist checks only. They do not execute an
external solver, do not call an external LLM, do not claim production-grade
physical validation, and do not claim a formal convergence proof.

## Fiber Coupling

The scalar Gaussian mode-overlap preview uses independent factors for mode
size mismatch, lateral offset, and angular tilt:

- `eta_w = (2 w_in w_f / (w_in^2 + w_f^2))^2`
- `offset_factor = exp(-2 dx^2 / (w_in^2 + w_f^2))`
- `tilt_factor ~= exp(-(pi w_eff theta / lambda)^2)`
- `eta = eta_w * offset_factor * tilt_factor`, bounded to `[0, 1]`

Reference cases:

- `fiber_gaussian_perfect_overlap`: equal waists, zero offset, zero tilt,
  expected coupling efficiency near `1.0`.
- `fiber_gaussian_waist_mismatch`: unequal waists lower the estimate.
- `fiber_gaussian_offset_loss`: non-zero lateral offset lowers the estimate.
- `fiber_gaussian_tilt_loss`: non-zero angular tilt lowers the estimate.

Failure modes reject non-finite or non-positive waists, non-positive
wavelength, and negative lateral offset.

## Polarization

The polarization preview uses ideal two-component Jones calculus:

- linear polarization: `[cos(theta), sin(theta)]`
- ideal polarizer: `P = |a><a|`
- ideal waveplate: rotate into local axes, apply retardance, rotate back

Reference cases:

- `jones_linear_0deg`: horizontal linear polarization is approximately
  `[1, 0]`.
- `jones_linear_90deg`: vertical linear polarization is approximately
  `[0, 1]`.
- `jones_linear_polarizer_malus`: 45-degree input through a 0-degree polarizer
  gives intensity near `cos^2(45 deg) = 0.5`.
- `jones_half_waveplate_preview`: a half-wave plate at 45 degrees rotates
  horizontal input to vertical up to global phase.
- `jones_quarter_waveplate_phase_preview`: a quarter-wave plate introduces
  relative phase near `pi/2` for a suitable diagonal input.

Failure modes reject malformed Jones vectors, zero-intensity Jones vectors,
non-finite angles, and non-finite retardance.

## Files

Reference JSON cases live under:

- `examples/optics_reference_cases/fiber_coupling/`
- `examples/optics_reference_cases/polarization/`

API fixtures for representative reference cases live under `examples/api/`.

## Safety Boundary

- Calculator quality level is `sanity_checked_preview`.
- Outputs are local preview/design-assist evidence.
- No external solver execution is performed.
- No external LLM is called.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
