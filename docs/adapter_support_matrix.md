# Adapter Support Matrix

Version scope: current public prerelease `v0.9.0rc3`; current `main`
development version `0.9.0rc4`. `v0.9.0rc4` is not a release, the
`v0.9.0rc4` tag has not been created, and PyPI/TestPyPI remain unpublished.
Continue v1.0 readiness engineering and prepare a `v0.9.0rc4` release draft
only when accumulated changes should be published as another RC.
Compatibility evidence is tracked in `docs/v1_0_compatibility_policy.md`,
`docs/validation_evidence_manifest.md`, and `examples/examples_manifest.json`.

optical-spec-agent is open-source-solver-first. Adapter outputs are local
generated artifacts. They do not run external solvers by default and do not
claim production-grade physical validation. Adapter listing and evidence tests
do not require external LLM providers, proprietary licenses, or network access.

Registry `current_status` values are `preview` for Meep and `mvp` for MPB,
Gmsh, Elmer, and Optiland. No production-grade physical validation is claimed.

| Adapter | Backend category | Openness / dependency class | Registry/CLI visible | Default support level | Local artifact preview | External solver required to execute? | External solver run by default? | Evidence fixture/test | Proprietary dependency required? | Known limitations | v1.0 readiness |
|---|---|---|---:|---|---|---|---|---|---|---|---|
| `meep` | Open-source simulation backend | Optional external open-source solver | Yes | `preview` / research-preview | Python script | Yes, only for explicit `meep-run` execution | No | Yes: `tests/fixtures/adapter_golden/meep_missing_wavelength_expected_fragments.txt`, `tests/test_adapter_evidence_fixtures.py` | No | Specialized nanoparticle-on-film adapter; scripts are preview/research-preview and not production-grade validation | Needs solver-backed validation standard before stable claims |
| `mpb` | Open-source simulation backend | Optional external open-source solver | Yes | MVP scaffold | Python scaffold | Yes, to execute MPB externally | No | Yes: `examples/specs/mpb_preview.json`, `tests/fixtures/adapter_golden/mpb/`, `tests/test_adapter_family_evidence.py` | No | Uses default lattice, k-points, resolution, and num_bands when missing; geometry is schematic | Needs richer periodic geometry schema and optional solver validation |
| `gmsh` | Open-source geometry / mesh backend | Optional external open-source mesh tool | Yes | MVP scaffold | `.geo` scaffold | Yes, to mesh externally | No | Yes: `examples/specs/gmsh_preview.json`, `tests/fixtures/adapter_golden/gmsh/`, `tests/test_adapter_family_evidence.py` | No | Geometry is schematic unless OpticalSpec carries explicit dimensions; physical groups are placeholders | Needs richer CAD/mesh schema and optional gmsh validation |
| `elmer` | Open-source multiphysics backend | Optional external open-source solver | Yes | MVP scaffold | `.sif` scaffold | Yes, to execute `ElmerSolver` externally | No | Yes: `examples/specs/elmer_preview.json`, `tests/fixtures/adapter_golden/elmer/`, `tests/test_adapter_family_evidence.py` | No | Requires a real mesh prepared outside this adapter; equation and boundary sections are placeholders | Needs explicit mesh/FEM boundary contract and optional solver validation |
| `optiland` | Open-source simulation backend | Optional external open-source solver | Yes | MVP scaffold | Python scaffold | Yes, to execute Optiland externally | No | Yes: `examples/specs/optiland_preview.json`, `tests/fixtures/adapter_golden/optiland/`, `tests/test_adapter_family_evidence.py` | No | OpticalSpec lacks full lens surface sequence and glass catalog mapping | Needs lens prescription schema extension before stable claims |

## Registry contract

The adapter registry currently exposes:

- `meep`
- `mpb`
- `gmsh`
- `elmer`
- `optiland`

`adapter-list --json` must include the same adapter names and metadata fields:
`tool_name`, `display_name`, `solver_family`, `output_language`,
`output_extension`, `supported_solver_methods`, `supported_physical_systems`,
`current_status`, `limitations`, and `consumed_fields`.

## Support boundary

- External solvers are not run by default.
- External solver installation is not required for default tests.
- External LLM providers are not required for adapter evidence tests.
- Proprietary licenses are not required for default tests, examples, smoke, or
  release validation.
- MPB/Gmsh/Elmer/Optiland outputs are scaffold/MVP unless separately validated.
- Meep execution remains optional/local and must be explicitly requested.
- Adapter warnings and defaults are part of the auditable output contract.
- Physical correctness is not claimed as production-grade.
- Workflow-to-adapter planning is preview/no-execute by default.

## Proprietary tools

The following are non-default proprietary targets, not registered adapters unless
source code explicitly registers them:

| Tool | Classification | Default dependency? | Default tests? | Release validation? | Notes |
|---|---|---:|---:|---:|---|
| Zemax | Proprietary/export-only future target | No | No | No | Future support, if any, must be manually scoped and export-only by default. |
| Lumerical | Proprietary/export-only future target | No | No | No | Compatibility examples do not imply default solver automation. |
| COMSOL | Proprietary/export-only future target | No | No | No | Schema coverage examples do not imply solver-backed validation. |
| proprietary Ansys optics tools | Proprietary/export-only future target | No | No | No | No proprietary Ansys license is required for tests, smoke, examples, or release validation. |

Export-only future support means generating scripts, templates, or configs that a
user may inspect and run manually. It does not imply solver-backed correctness or
production-grade physical validation.

## Offline journey linkage

The offline end-to-end journey in `examples/e2e/` uses adapter registry
visibility and workflow planning as local compatibility evidence. It does not
execute adapter solvers, does not require external LLM providers, and does not
require proprietary optical software. Pre-v1 migration boundaries are tracked in
`docs/migration_notes_pre_v1.md`.
