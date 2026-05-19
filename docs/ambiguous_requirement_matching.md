# Ambiguous Requirement Matching

Requirement matching is deterministic keyword logic. It maps natural-language
goals to local optical design templates without calling an external LLM.

## Confidence Levels

- `high`: one design family is clearly dominant.
- `medium`: one safe default template is available, but important inputs are missing.
- `low`: multiple design families are plausible or the goal is under-specified.
- `none`: no supported local template matched.

## Response Fields

`POST /api/design-requirements/match` returns:

- `candidate_templates`
- `ambiguity_notes`
- `missing_disambiguation_inputs`
- `recommended_questions`
- `safe_default_template`
- `no_external_llm_used=true`

Ambiguous goals produce questions rather than unsafe solver actions. For
example, a waveguide/coating mixed goal reports both candidate families and
asks which path should take priority.

## Safe Behavior

- No external LLM is called by default.
- No external solver is executed by default.
- Unknown goals do not silently select a solver path.
- Results remain preview/design-assist and do not claim production-grade validation.
