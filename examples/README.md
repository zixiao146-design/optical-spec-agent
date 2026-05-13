# Offline Examples

These examples are local fixtures for README, CLI, adapter, workflow, and v1.0
readiness evidence. They are offline by default: no external solver, external
LLM provider, network access, PyPI upload, or TestPyPI upload is required.

Current public prerelease: `v0.9.0rc3`.
Current main development version: `0.9.0rc4.dev0`.

## Minimal spec

```bash
optical-spec validate examples/specs/minimal_nanoparticle.json
optical-spec parse examples/specs/minimal_nanoparticle.json --json
```

`examples/specs/minimal_nanoparticle.json` is a valid local `OpticalSpec`
fixture and also contains a `text` request field for the parse example.

## Adapter preview

```bash
optical-spec adapter-generate examples/specs/missing_wavelength_meep_preview.json \
  --tool meep \
  --json
```

This fixture intentionally omits an explicit wavelength range so the Meep
adapter records its preview default. It does not run Meep.

## Workflow preview

```bash
optical-spec workflow-plan examples/workflows/local_preview_request.json --json
```

The workflow example uses deterministic local settings. It plans a workflow but
does not execute external solvers or call external LLM providers.
