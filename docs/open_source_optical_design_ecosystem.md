# Open-source Optical Design Ecosystem

optical-spec-agent follows an open-source-solver-first strategy. Commercial
and proprietary tools are non-default, export-only or future-evaluation paths
unless explicitly approved and implemented.

Current adapter direction:
- Meep: FDTD preview and scaffold generation.
- MPB: photonic band / eigenmode preview and scaffold generation.
- Gmsh: geometry and mesh preview scaffolds.
- Elmer: Level 2 + Level-3-ready, install deferred; not marked Level 3.
- Optiland: lens/ray optics scaffold direction.

Current frontend/API domain expansion:
- Local preview material catalog.
- Optical design examples for nanoparticle plasmonics, thin films, waveguides,
  photonic crystals, dielectric metasurfaces, and lens/ray optics.
- Deterministic sub-agent collaboration trace.

Candidate future integrations to evaluate:
- TorchOptics for differentiable optical modeling experiments.
- AOtools for adaptive optics utilities.
- Simphony for photonic circuit modeling.
- PyFocus for focused-field and microscopy-style calculations.
- Lightweight ray optics / lens design candidates that remain maintainable.

Non-default / non-goals:
- Zemax, Lumerical, COMSOL, and commercial Ansys workflows are not default
  dependencies.
- Proprietary solvers must not become required by default.
- No external solver is executed by default.
- No external LLM is called by default.
- No production-grade physical validation is claimed.
- Formal convergence proof is not claimed.
