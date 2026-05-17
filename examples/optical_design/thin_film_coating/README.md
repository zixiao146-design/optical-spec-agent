# Thin Film Coating Preview

Design goal: preview an optical coating workflow without adding a solver dependency.

- Suggested materials: SiO2, TiO2, Al2O3.
- Suggested adapter: preview-only; future TMM adapter candidate.
- Workflow steps: parse, validate, material suggestion, workflow plan, artifact preview, human review.
- Expected next action: decide whether a lightweight open-source TMM path should be evaluated later.

Safety boundaries:
- No solver is executed by default.
- No external LLM is called by default.
- No production-grade physical validation is claimed.
- Formal convergence proof is not claimed.
