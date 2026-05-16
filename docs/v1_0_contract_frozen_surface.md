# v1.0 Contract Frozen Surface Candidate

This document lists the public surface proposed for v1.0 freeze. It is a
candidate package for maintainer review, not an approved freeze.

| Area | Frozen candidate item | Evidence/tests | Notes |
|---|---|---|---|
| CLI | CLI command names | `docs/cli_contract.md`, `tests/test_cli_contract.py`, `tests/test_documented_cli_examples.py` | The documented command names are candidate-stable. |
| CLI | CLI examples | `docs/offline_user_journey.md`, `examples/`, `tests/test_documented_cli_examples.py` | Examples remain no-network and no-default-solver. |
| Schema | Schema fields | `docs/schema_contract.md`, `tests/test_schema_contract.py`, `tests/test_public_contract_manifest.py` | Public schema fields are candidate-stable; internals may still evolve before final approval. |
| Adapters | Adapter registry names | `docs/adapter_support_matrix.md`, `tests/test_adapter_registry.py`, `tests/test_adapter_cli_contract.py` | `meep`, `mpb`, `gmsh`, `elmer`, and `optiland` are candidate-stable registry names. |
| Adapter JSON | `adapter-list --json` shape | `docs/cli_contract.md`, `tests/test_cli_contract.py`, `tests/test_adapter_cli_contract.py` | Top-level JSON shape is candidate-stable. |
| Workflow | `workflow-plan --json` keys | `docs/workflow_preview_contract.md`, `tests/test_workflow_preview_contract.py` | Public top-level keys are candidate-stable; implementation internals remain preview. |
| Examples | Examples manifest | `examples/examples_manifest.json`, `tests/test_examples_manifest.py` | Manifest paths and no-network/no-solver/no-LLM/no-proprietary guarantees are candidate-stable. |
| Package metadata | Project name, version semantics, console script | `pyproject.toml`, `docs/packaging_gate.md`, `tests/test_packaging_gate.py` | Package metadata is candidate-stable for RC flow; PyPI is not published. |
| Default execution guarantees | No-default solver/LLM/proprietary guarantees | `docs/validation_boundary.md`, `docs/external_solver_policy.md`, `docs/external_llm_policy.md`, `docs/proprietary_solver_policy.md` | External solvers, external LLMs, and proprietary solvers are not default dependencies. |

The freeze candidate does not include generated adapter internals, workflow
implementation internals, optional solver validation internals, production-grade
physical validation, formal convergence proof, or Elmer Level 3 validation.

