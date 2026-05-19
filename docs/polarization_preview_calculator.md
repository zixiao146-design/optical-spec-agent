# Polarization Preview Calculator

The polarization preview calculator provides deterministic Jones-calculus
helpers for local polarizer and waveplate reasoning. It is a design-assist
calculator, not a vector electromagnetic simulation.

Endpoint: `POST /api/optics/polarization-jones`

## Supported Previews

- `linear_polarization(angle_deg)`
- `jones_linear_polarizer(input_jones, angle_deg)`
- `jones_waveplate(input_jones, retardance_rad, fast_axis_deg)`
- `summarize_polarization_state(jones_vector)`

## Inputs

The API accepts either an explicit two-component Jones vector or an
`input_angle_deg` for a linear polarization state. Jones components may be
numbers, `[real, imag]`, or `{real, imag}` objects.

## Assumptions

- Jones vectors are coherent two-component polarization states.
- The polarizer is ideal.
- The waveplate is ideal, spatially uniform, and wavelength-independent in the
  preview.
- Depolarization, aperture effects, coatings, dispersion, and full vector
  field propagation are not included.

## Reference Sanity Cases

- Linear polarization at 0 degrees is approximately `[1, 0]`.
- Linear polarization at 90 degrees is approximately `[0, 1]`.
- A 45-degree input through a 0-degree ideal polarizer gives intensity
  `cos^2(45 deg) ~= 0.5`.
- A half-wave plate at 45 degrees rotates horizontal input to vertical up to a
  global phase.
- A quarter-wave plate introduces relative phase near `pi/2` for a suitable
  diagonal input.

The JSON reference cases live under `examples/optics_reference_cases/polarization/`;
the combined reference policy is documented in
[`fiber_polarization_reference_cases.md`](fiber_polarization_reference_cases.md).

## Limitations

This is preview/design-assist evidence only.

- No external solver is executed.
- No external LLM is called.
- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
- Real polarization-device behavior should be verified with validated
  Jones/Mueller measurements or full vector EM simulation when needed.
