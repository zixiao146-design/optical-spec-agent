# Preview Boundary Policy

This policy defines the boundary for optical-spec-agent backend evidence in
`0.9.0rc8.dev0`. The backend is useful as a deterministic optical design
assistant, but its current evidence must remain preview/design-assist.

## What Preview/Design-Assist Means

Users can rely on the backend to:

- route supported optical design goals to deterministic templates and domains;
- report missing critical and optional inputs;
- run local analytic calculators for sanity-checked previews;
- generate adapter-native source/monitor metadata previews;
- keep external solver, external LLM, upload, tag, and release actions disabled by default;
- expose evidence through local scripts and API responses.

Users must verify:

- material constants and wavelength-dependent data;
- solver-specific source, monitor, mesh, and boundary settings;
- physical accuracy, convergence, and tolerances;
- production workflow suitability.

## Component Boundaries

| Component | Boundary |
| --- | --- |
| Materials | Local curated preview catalog; not a production-grade optical constants database. |
| Calculators | Sanity-checked analytic previews; not production-grade physical validation. |
| Application domains | Benchmarks check deterministic routing and diagnostics, not physical correctness. |
| Source/monitor models | Preview metadata only; no real solver monitor result is claimed. |
| Adapter mappings | Adapter-native semantic previews; real results require explicit solver execution. |
| Optional solver micro-benchmarks | Manual, explicit opt-in only; default tests, smoke, quality gates, and release gates do not run solvers. |
| Optional solver readiness | Profile-aware availability detection and approval matrix only; no solver execution, PyPI/TestPyPI upload, tag, or release authorization. |
| Sub-agents | Deterministic backend roles; not independent autonomous services. |
| Frontend | UI/demo surface; not validation evidence. |

## Publication Boundary

PyPI publication, if later approved, would not imply production-grade physical
validation. Release or packaging status is separate from physical validation,
solver convergence, and material-data verification.

## Not Claimed

- No production-grade physical validation is claimed.
- No formal convergence proof is claimed.
- No guaranteed accuracy is claimed.
- No external solver execution is performed by default.
- Optional solver-backed validation is manual and explicit opt-in only.
- Optional solver readiness checks do not execute solver binaries and do not
  authorize publication or release actions.
- `OSA_SOLVER_PYTHON` can calibrate import-only probes for a dedicated solver
  Python environment; CLI tools such as Gmsh are still detected through the
  current `PATH`.
- No external LLM is called by default.
- Elmer Level 3 remains deferred.
