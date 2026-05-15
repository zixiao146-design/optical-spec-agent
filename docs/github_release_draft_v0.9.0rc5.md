# optical-spec-agent v0.9.0rc5

## English Summary

v0.9.0rc5 is the fifth release candidate for v0.9.0. It packages the
post-v0.9.0rc4 v1.0 readiness hardening on `main`, with a focus on repeatable
quality gates, operations readiness, public contract evidence, adapter maturity,
and optional open-source-solver validation boundaries.

This release draft includes optional manual validation evidence for Gmsh, Meep,
MPB, and Optiland. Elmer has a Level-3-ready path, but remains Level 2 because
ElmerSolver is not currently available in the maintained local package routes
tested for this environment. The Elmer deferred record is
`validation/elmer/elmer_install_deferred_2026-05-15.md`.

The draft also improves Python-aware solver preflight, no-upload quality gates,
release dry-run governance, secrets hygiene, offline user journey evidence,
public contract freeze evidence, and validation manifests. PyPI is not
published, and TestPyPI is not uploaded.

## 中文简介

v0.9.0rc5 是 v0.9.0 的第五个候选版本，纳入 v0.9.0rc4 之后的 v1.0
readiness 加固。

Gmsh / Meep / MPB / Optiland 已记录窄范围 optional manual validation
evidence。Elmer 已具备 Level-3-ready 路径，但由于当前缺少 ElmerSolver，
仍保持 Level 2 + deferred。

本候选版本仍不声称生产级物理验证，也不声称形式化收敛证明。PyPI/TestPyPI
仍未发布/上传。

## Highlights

- Open-source-solver-first release engineering.
- One-command local quality gates.
- CI/workflow parity and release dry-run operations docs.
- Python-aware solver availability preflight.
- Adapter maturity model for Meep, Gmsh, Elmer, MPB, and Optiland.
- Optional manual validation evidence for Gmsh, Meep, MPB, and Optiland.
- Elmer Level-3-ready documentation with an install-deferred record.
- Public contract freeze candidate and public contract manifest.
- Offline examples, examples manifest, and offline end-to-end user journey.
- Validation evidence manifest.
- Packaging and validation gates.
- Wheel install smoke.
- No proprietary solver dependency by default.
- No external solver or external LLM required by default.

## Verification

- Quality gates: passed.
- TestPyPI no-upload preflight: passed.
- Normal smoke: passed.
- Wheel smoke: passed.
- `pytest`: 475 passed, 4 warnings.
- `python -m build`: passed.
- `make check`: passed.
- CLI examples: passed.
- E2E example: passed.
- Dist files:
  - `optical_spec_agent-0.9.0rc5-py3-none-any.whl`
  - `optical_spec_agent-0.9.0rc5.tar.gz`

## Scope Limitations

- No PyPI publish.
- No TestPyPI upload.
- No production-grade physical validation.
- No formal convergence proof.
- External solvers are not run by default.
- External LLM is not required by default.
- Proprietary solvers are not required by default.
- Elmer Level 3 validation is deferred.
- Workflow remains a local/synchronous preview.
- This release candidate is not final 1.0 stability.

## Important Note

- `v0.9.0rc1`, `v0.9.0rc2`, `v0.9.0rc3`, and `v0.9.0rc4` tags are unchanged.
- `v0.9.0rc5` tag should be created only after maintainer approval.
- This task does not create a tag, create a GitHub release, or upload packages.
