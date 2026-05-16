# PyPI Post-publication Verification Plan

This plan defines the checks to run only after a separately approved PyPI
publication. It is not approval to publish PyPI.

For v1.0.0 planning, this plan is paired with
`docs/v1_0_pypi_decision_gate.md` and `docs/v1_0_release_criteria.md`.

## Clean install

- Create a clean virtual environment.
- Install from PyPI with `python -m pip install optical-spec-agent==<version>`.
- Confirm the installed distribution is resolved from PyPI.

## Runtime checks

- Import version check:
  `import optical_spec_agent; optical_spec_agent.__version__ == "<version>"`.
- Run `optical-spec --help`.
- Run `optical-spec adapter-list --json`.
- Run `optical-spec validate examples/specs/minimal_nanoparticle.json`.
- Run `optical-spec parse examples/specs/minimal_nanoparticle.json --json`.
- Run `optical-spec workflow-plan examples/workflows/local_preview_request.json --json`.

## Post-publication status record

- Add a post-publication status doc with the package version, PyPI URL,
  artifact names, install command, verification results, and known limitations.
- Record that TestPyPI evidence, if present, does not by itself authorize PyPI.
- Record whether any release notes or README wording need a follow-up patch.

## Rollback and yank note

- PyPI artifacts are immutable for a given version.
- If metadata or runtime behavior is wrong, publish a new fixed version rather
  than attempting to overwrite files.
- Yanking may reduce accidental installs but does not remove artifacts from all
  clients, indexes, or caches.

## Validation scope

PyPI publication does not imply production-grade physical validation, a formal
convergence proof, optical design correctness, default external solver
execution, default external LLM execution, or proprietary solver support.
