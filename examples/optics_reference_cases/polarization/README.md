# Polarization Reference Cases

These local JSON files document deterministic sanity checks for the
Jones-calculus polarization preview calculator. They are preview/design-assist
cases only.

They do not execute an external solver, do not call an external LLM, do not
claim production-grade physical validation, and do not claim a formal
convergence proof.

## Cases

- `linear_polarizer_malus.json`: 45-degree linear polarization through a
  0-degree ideal polarizer, expected intensity `cos^2(45 deg) ~= 0.5`.
- `half_wave_plate_rotation.json`: horizontal input through a half-wave plate
  at 45 degrees, expected output orientation equivalent to vertical up to
  global phase.
- `quarter_wave_plate_phase.json`: 45-degree input through a quarter-wave
  plate, expected relative phase near `pi/2`.

The formulas are local documented approximations, not external validation
certificates.
