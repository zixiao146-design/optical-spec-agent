# Nanoparticle Plasmonics Preview

Design goal: preview a local workflow for nanoparticle scattering using open-source-first tooling.

- Suggested materials: Au, Ag, SiO2, water, air from the local preview material catalog.
- Suggested adapter: Meep, with Gmsh geometry preview if geometry scaffolding is needed.
- Workflow steps: parse, validate, material suggestion, workflow plan, adapter preview, human review.
- Expected next action: verify wavelength-dependent optical constants and generate a local adapter preview.

Safety boundaries:
- No solver is executed by default.
- No external LLM is called by default.
- No production-grade physical validation is claimed.
- Formal convergence proof is not claimed.
