# Fiber Coupling Reference Cases

These local JSON files document deterministic sanity checks for the scalar
Gaussian fiber-coupling preview calculator. They are preview/design-assist
cases only.

They do not execute an external solver, do not call an external LLM, do not
claim production-grade physical validation, and do not claim a formal
convergence proof.

## Cases

- `perfect_gaussian_match.json`: equal input and fiber waists, zero offset,
  zero tilt, expected coupling efficiency near `1.0`.
- `gaussian_waist_mismatch.json`: unequal waists, expected efficiency below
  the perfect-match reference.
- `gaussian_offset_loss.json`: lateral offset loss, expected offset factor and
  efficiency below `1.0`.
- `gaussian_tilt_loss.json`: angular tilt loss, expected tilt factor and
  efficiency below `1.0`.

The formulas are local documented approximations, not external validation
certificates.
