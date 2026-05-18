# Source/Monitor Missing-Input Diagnostics

This document defines how the backend reports missing source, monitor, and
observable inputs for local optical design previews.

## Required Inputs

The required inputs vary by requirement template, but common fields are:

- source type
- wavelength or wavelength range
- polarization
- incidence direction
- beam waist or mode index when relevant
- monitor observable
- monitor region
- wavelength/frequency sampling

## Default Assumptions

The backend records default assumptions explicitly. Examples:

- nanoparticle scattering defaults to a normal-incidence plane-wave-like source.
- nanoparticle scattering defaults to a 400-900 nm preview band.
- nanoparticle scattering defaults to `linear_x` polarization.
- thin-film coating defaults to normal incidence and an R/T monitor.
- Gaussian beam focus defaults to paraxial scalar formulas.

Defaults make a case safe to preview, not safe to run an external solver.

## Diagnostics

`OpticalLanguageDiagnostics` reports:

- `missing_required_inputs`
- `default_assumptions_applied`
- `ambiguity_notes`
- `blocking_questions`
- `safe_to_preview`
- `safe_to_run_solver`

`safe_to_preview` can be true while `safe_to_run_solver` remains false.

## API

- `POST /api/optical-language/infer`
- `POST /api/optical-language/diagnose`
- `POST /api/agent-session`

Agent sessions also include tool-call ledger entries:

- `optical_language.infer_source_monitor`
- `optical_language.diagnose_missing_inputs`

## Safety Boundary

No external solver is executed. No external LLM is called. No network material
lookup is performed. Diagnostics are preview/design-assist and do not claim
production-grade physical validation or formal convergence proof.
