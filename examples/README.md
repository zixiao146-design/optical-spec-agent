# Offline Examples

These examples are local fixtures for README, CLI, adapter, workflow, and v1.0
readiness evidence. They are offline by default: no external solver, external
LLM provider, network access, PyPI upload, or TestPyPI upload is required.

Current public prerelease: `v0.9.0rc6`.
Current main release draft: `0.9.0rc7`.

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

Additional adapter preview fixtures are local artifact previews, not
solver-backed validation:

```bash
optical-spec adapter-generate examples/specs/gmsh_preview.json --tool gmsh --json
optical-spec adapter-generate examples/specs/elmer_preview.json --tool elmer --mesh examples/meshes/waveguide.msh --json
optical-spec adapter-generate examples/specs/mpb_preview.json --tool mpb --json
optical-spec adapter-generate examples/specs/optiland_preview.json --tool optiland --json
```

These commands generate `.geo`, `.sif`, or Python scaffold text. They do not
run Gmsh, ElmerSolver, MPB, or Optiland.

## Workflow preview

```bash
optical-spec workflow-plan examples/workflows/local_preview_request.json --json
```

The workflow example uses deterministic local settings. It plans a workflow but
does not execute external solvers or call external LLM providers.

## End-to-end offline journey

`examples/e2e/README.md` documents the local user journey that connects CLI
inspection, validation, parsing, adapter listing, and workflow planning:

```bash
optical-spec workflow-plan examples/e2e/local_optical_workflow.json --json
```

The e2e fixture is preview/diagnostics evidence only. It does not require
network access, external solvers, external LLM providers, or proprietary optical
software.

## Design requirement templates

`examples/design_requirements/` contains seven realistic first-run requirement
templates. Each folder includes `requirement.json`, English and Chinese natural
language goals, expected tool calls, and a README. These fixtures demonstrate
the backend path from natural language -> optical language -> design case ->
tool-call ledger. They are preview/design-assist examples only and do not run
solvers, call external LLMs, upload packages, create tags, or create releases.
