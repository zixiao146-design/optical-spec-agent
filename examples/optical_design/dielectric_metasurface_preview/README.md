# Dielectric Metasurface Preview

Design goal: preview a local metasurface workflow without running solvers.

- Suggested materials: TiO2, Si3N4, Si, SiO2.
- Suggested adapter: Meep with Gmsh geometry preview.
- Workflow steps: parse, validate, material suggestion, workflow plan, adapter preview, human review.
- Expected next action: confirm meta-atom geometry and wavelength band before deeper validation.

Safety boundaries:
- No solver is executed by default.
- No external LLM is called by default.
- No production-grade physical validation is claimed.
- Formal convergence proof is not claimed.
