# Release Decision Matrix

This document frames the final maintainer choice after the release-engineering
quality gates landed in commit `76d1646`.

## Recommendation

If all quality gates continue to pass and the README/docs keep the
preview/scaffold/evaluation boundaries clear, the recommended path is **Option C:
prepare a `0.9.0rc1` release candidate**. That option has now been selected for
the package metadata bump; manual tag/release creation remains separate.

Do not claim `1.0`, production automation, production-grade physical validation,
or production-ready solver input. v0.9 is an orchestration and engineering
readiness milestone, not a scientific validation claim.

## Option A: Keep `0.5.0` Packaged Baseline

### Meaning

Keep `pyproject.toml` at `0.5.0` and describe v0.6-v0.9 work as unreleased
main-branch preview capability.

### Pros

- Most conservative versioning choice.
- Avoids implying that broad v0.6-v0.9 surfaces are formally released.
- Lets maintainers continue collecting feedback before a release candidate.
- Keeps PyPI/package consumers on the last packaged baseline.

### Cons

- Users reading `main` see many capabilities that installed package metadata
  still labels `0.5.0`.
- Release-check remains in warning state by design.
- Harder for external testers to reference a single candidate version.

### README Impact

README must keep stating that `pyproject.toml` is `0.5.0` and v0.6-v0.9 are
main-branch preview/scaffold/evaluation capabilities.

### GitHub Release Impact

No new GitHub release or tag is created.

### User Install Impact

Editable/main-branch installs expose v0.6-v0.9 preview capability, while formal
package metadata remains `0.5.0`.

### Main Branch Preview Impact

Main branch remains the proving ground for release-candidate feedback.

## Option B: Bump To `0.9.0`

### Meaning

Update package metadata and docs to make v0.9 the next formal release target.

### Pros

- Aligns package version with current main-branch capability.
- Removes the version mismatch warning.
- Gives users a clear version for diagnostics, adapters, LLM parser foundation,
  and workflow orchestration.

### Cons

- Large jump from `0.5.0` to `0.9.0`.
- Broad CLI/API/docs surface may still need external user feedback.
- Could be mistaken as final stability if docs are not careful.

### Files To Modify

- `pyproject.toml`
- `src/optical_spec_agent/__init__.py`
- `README.md`
- `CHANGELOG.md`
- `docs/release_readiness_current.md`
- `docs/release_notes_current.md`
- `docs/release_notes_v0.9.0.md`
- `docs/versioning_policy.md`, if wording needs clarification

### Quality Gates To Re-run

- `pip install -e ".[dev]"`
- `pytest -q`
- `python benchmarks/run_benchmark.py --mode key_fields`
- `python benchmarks/run_semantic_benchmark.py`
- `python benchmarks/run_semantic_benchmark.py --report outputs/semantic_benchmark_report.json`
- `python benchmarks/run_llm_benchmark.py --cases benchmarks/llm_cases.json --parser hybrid --llm-provider mock --report outputs/llm_eval_report.json`
- `python benchmarks/run_workflow_benchmark.py --cases benchmarks/workflow_cases.json --output-dir outputs/workflow_benchmark --report outputs/workflow_benchmark_report.json`
- `make check`
- `python scripts/check_release_readiness.py --report outputs/release_readiness_report.json`
- `python -m build`
- `twine check dist/*`

### Release Notes Requirements

Release notes must explicitly state that adapters are scaffold/MVP, workflow is
local/synchronous, external solvers are not run by default, and no physical
validation claim is made.

### Risks

- Users may over-read v0.9 as production automation.
- Maintainers may need to support a broad surface sooner.

## Option C: Prepare `0.9.0rc1`

### Meaning

Prepare a release-candidate version plan for `0.9.0rc1` without creating a tag,
GitHub release, or PyPI publication in this task.

### Pros

- Aligns the version story with the broad main-branch surface while preserving
  candidate status.
- Invites users to test the CLI/API/workflow surface before final `0.9.0`.
- Keeps claims honest: release candidate, not production-complete.
- Best fit for a project that just added release-engineering quality gates.

### Cons

- Requires a later explicit version bump patch.
- Requires maintainers to decide release timing manually.
- Still needs careful docs to avoid production-validation overclaims.

### Why This Fits Now

- All reported gates passed after commit `76d1646`.
- The CLI surface is broad and worth candidate testing.
- v0.6-v0.9 features are engineering previews with clear limits.
- Formal releases have lagged behind main branch.

### RC Should Declare

- v0.6 diagnostics are post-hoc local diagnostics.
- v0.7 adapters generate solver-native scaffolds only.
- v0.8 LLM parser foundation uses deterministic mock provider by default.
- v0.9 workflow orchestration is synchronous/local and auditable.
- Quality gates and artifact contracts are available.

### RC Must Not Declare

- Production-grade physical validation.
- Formal convergence proof.
- Full solver automation.
- Automatic external solver execution.
- Real external LLM model quality.
- Production-ready MPB/Gmsh/Elmer/Optiland inputs.
