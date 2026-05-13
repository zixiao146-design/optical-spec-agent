# optical-spec-agent v0.9.0rc4

## English summary

`v0.9.0rc4` is the fourth release candidate for the `v0.9.0` line. It packages
the v1.0 readiness hardening accumulated after `v0.9.0rc3`.

Highlights include:

- Open-source-solver-first product strategy.
- Broader adapter family evidence for Meep, Gmsh, Elmer, MPB, and Optiland.
- Offline examples and `examples/examples_manifest.json`.
- Offline end-to-end user journey.
- Error model and pre-v1 migration notes.
- Public contract freeze candidate.
- Public contract manifest.
- Validation evidence manifest.
- TestPyPI no-upload preflight.
- Packaging and validation gates.
- Wheel install smoke.
- No proprietary solver dependency by default.
- No external solver or external LLM required by default.

## 中文简介

`v0.9.0rc4` 是 `v0.9.0` 的第四个候选版本，纳入了 `v0.9.0rc3`
之后的 v1.0 readiness 加固。

本候选版本明确 open-source-solver-first 定位，扩展了 Meep、Gmsh、Elmer、
MPB、Optiland 的 adapter family evidence，增加了离线端到端用户旅程、
public contract freeze candidate、public contract manifest、TestPyPI
no-upload preflight，以及 packaging / validation gates。

PyPI 仍未发布，TestPyPI 仍未上传。

## Verification

- `scripts/testpypi_preflight.sh`: passed
- `scripts/smoke_release.sh`: passed
- Wheel install smoke: passed
- `pytest`: 429 passed, 4 warnings
- `python -m build`: passed
- `make check`: passed
- CLI examples passed:
  - `optical-spec --help`
  - `optical-spec adapter-list --json`
  - `optical-spec validate examples/specs/minimal_nanoparticle.json`
  - `optical-spec parse examples/specs/minimal_nanoparticle.json --json`
  - `optical-spec workflow-plan examples/workflows/local_preview_request.json --json`
  - `optical-spec workflow-plan examples/e2e/local_optical_workflow.json --json`
- Dist files:
  - `optical_spec_agent-0.9.0rc4-py3-none-any.whl`
  - `optical_spec_agent-0.9.0rc4.tar.gz`
- PyPI: not published
- TestPyPI: not uploaded

## Scope limitations

- No PyPI publish.
- No TestPyPI upload.
- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLM is not required by default.
- Proprietary solvers are not required by default.
- Adapter outputs may still be MVP/scaffold unless explicitly validated.
- Workflow is local/synchronous preview.
- This RC is not final 1.0 stability.

## Important note

- `v0.9.0rc1`, `v0.9.0rc2`, and `v0.9.0rc3` tags are unchanged.
- `v0.9.0rc4` should be created as a new annotated tag only after final
  readiness checks pass.
- This draft does not create or move any tag.
- This draft does not create a GitHub release.
- This draft does not upload TestPyPI.
- This draft does not publish PyPI.
