# Fiber Coupling Preview Calculator

The fiber-coupling preview calculator estimates scalar Gaussian mode overlap
for local design orientation. It is deterministic Python and does not execute
an external solver.

Endpoint: `POST /api/optics/fiber-coupling`

## Inputs

- `wavelength_nm`
- `waist_input_um`
- `waist_fiber_um`
- `lateral_offset_um`
- `angular_tilt_mrad`

## Approximation

The preview separates coupling into three bounded factors:

- mode-size mismatch:
  `eta_w = (2 w_in w_f / (w_in^2 + w_f^2))^2`
- lateral offset penalty:
  `eta_d = exp(-2 d^2 / (w_in^2 + w_f^2))`
- angular tilt penalty using a scalar Gaussian phase-overlap estimate

The final `coupling_efficiency_estimate` is clipped to `[0, 1]`.

## Assumptions

- Input beam and fiber mode are circular scalar Gaussian modes.
- Polarization overlap, Fresnel loss, NA clipping, aberrations, and
  mode-solver effects are not included.
- Perfect waist match with zero offset and zero tilt is the local sanity case.

## Reference Sanity Cases

- Perfect Gaussian match: equal waists, zero lateral offset, zero angular tilt,
  expected `coupling_efficiency_estimate ~= 1.0`.
- Waist mismatch: unequal waists lower the estimate.
- Lateral offset: non-zero offset lowers the estimate.
- Angular tilt: non-zero tilt lowers the estimate.

The JSON reference cases live under
`examples/optics_reference_cases/fiber_coupling/`; the combined reference
policy is documented in
[`fiber_polarization_reference_cases.md`](fiber_polarization_reference_cases.md).

## Limitations

This is preview/design-assist evidence only.

- No external solver is executed.
- No external LLM is called.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
- Real coupling efficiency should be verified with validated mode-overlap,
  beam-propagation, measurement, or solver workflows.
