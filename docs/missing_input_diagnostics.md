# Missing-input Diagnostics

Missing-input diagnostics separate critical inputs from optional inputs so the
backend can proceed with a safe local preview while still blocking solver
execution by default.

## Critical vs Optional

Critical inputs define the physics family or first-order calculation. Examples:

- nanoparticle radius/material/wavelength band
- thin-film target wavelength and substrate
- waveguide core/cladding/thickness/wavelength
- lens focal length and object distance

Optional inputs improve preview quality. Examples include polarization,
incidence angle, aperture, field of view, background medium, or mode family.

## Defaults and Questions

Diagnostics report:

- `missing_critical_inputs`
- `missing_optional_inputs`
- `default_assumptions_applied`
- `ambiguity_notes`
- `blocking_questions`
- `safe_to_preview=true`
- `safe_to_run_solver=false`

The backend may produce a design-assist preview with visible defaults, but it
does not treat those defaults as approval to run a solver.

## Boundaries

- No external solver execution is performed.
- No external LLM is called.
- Defaults are explicit and reviewable.
- No production-grade physical validation or formal convergence proof is claimed.
