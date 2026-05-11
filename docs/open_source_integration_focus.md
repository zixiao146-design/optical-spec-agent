# Open-Source Integration Focus

> Status: Current integration direction. Meep is implemented; v0.7 adds MVP
> input-generation adapters for MPB, Gmsh, Elmer, and Optiland. These adapters
> do not run external solvers.

## Why Open-Source-First

The adapter roadmap targets open-source, scriptable tools because they are:

- reproducible without license servers;
- usable from Python or CLI workflows;
- easier to test in CI without proprietary installations;
- composable as future multi-agent or multi-step workflows.

## Current Adapter Status

| Tool | Method / role | Status | Notes |
|------|---------------|--------|-------|
| Meep | FDTD | Implemented | Specialized nanoparticle-on-film script generation plus optional local `meep-run` harness |
| MPB | Eigenmode / band structure | MVP preview | Generates Python scaffold only |
| Gmsh | Geometry / mesh | MVP preview | Generates annotated `.geo` scaffold only |
| Elmer | FEM | MVP preview | Generates `.sif` scaffold only; mesh is external |
| Optiland | Sequential ray tracing | MVP preview | Generates Python scaffold only; current schema lacks full lens surface sequence |
| FreeCAD | CAD | Future | Not implemented |

## Why Meep Came First

Meep provided the first end-to-end proof point:

```text
natural language -> OpticalSpec -> validation -> Meep script -> optional local artifacts
```

Its Python API maps well to the current `OpticalSpec` fields for one trusted
nanoparticle-on-film workflow. That path remains the strongest hero workflow.

## Why Adapter Work Still Comes Before LLM Parser

The project intentionally ships adapter and diagnostics work before real LLM
integration:

1. Solver-facing code exposes missing or ambiguous schema fields.
2. Rule-based parser outputs and benchmarks provide stable evaluation data.
3. A better parser is only useful if downstream adapters can give concrete,
   reviewable feedback about readiness and missing fields.

LLM parser integration remains v0.8+ work.

## Commercial Software Examples

Examples mentioning COMSOL or Lumerical remain schema-coverage examples. They
are not current adapter targets. The main roadmap stays open-source-native:
Meep, MPB, Gmsh, Elmer, and Optiland.

See also:

- [`open_source_stack.md`](open_source_stack.md)
- [`adapter_architecture.md`](adapter_architecture.md)
- [`adapter_mvp_v0.7.md`](adapter_mvp_v0.7.md)
