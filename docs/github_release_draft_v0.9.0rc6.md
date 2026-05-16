# optical-spec-agent v0.9.0rc6

English summary:
- v0.9.0rc6 is the sixth release candidate for v0.9.0.
- It packages post-v0.9.0rc5 v1.0 readiness hardening.
- It records successful TestPyPI Trusted Publishing for 0.9.0rc6.dev0.
- It records clean install verification from TestPyPI.
- It records approved v1.0 public contract freeze.
- It includes PyPI publication readiness and post-publication verification plans.
- It keeps PyPI publication unapproved and unpublished.
- It keeps v1.0.0 unreleased.
- It preserves conservative validation boundaries.

中文简介：
- v0.9.0rc6 是 v0.9.0 的第六个候选版本。
- 纳入 v0.9.0rc5 之后的 v1.0 readiness 加固。
- 已完成 0.9.0rc6.dev0 的 TestPyPI Trusted Publishing 和 clean install 验证。
- 已记录并批准 v1.0 public contract freeze。
- 已补齐 PyPI publication readiness checklist 和 post-publication verification plan。
- PyPI 仍未发布，仍需单独批准。
- v1.0.0 仍未发布。
- 仍不声称生产级物理验证或形式化收敛证明。

Highlights:
- TestPyPI Trusted Publishing verified for 0.9.0rc6.dev0.
- CI and GitHub Actions workflow gates stabilized.
- v1.0 public contract freeze approved.
- PyPI publication readiness checklist added.
- PyPI post-publication verification plan added.
- Publication decision boundaries clarified.
- Adapter maturity remains:
  - Gmsh: Level 3
  - Meep: Level 3
  - MPB: Level 3
  - Optiland: Level 3
  - Elmer: Level 2 + Level-3-ready, install deferred

Verification:
- quality gates: passed
- TestPyPI no-upload preflight: passed
- normal smoke: passed
- wheel smoke: passed
- pytest: passed
- python -m build: passed
- make check: passed
- CLI examples: passed
- dist files:
  - optical_spec_agent-0.9.0rc6-py3-none-any.whl
  - optical_spec_agent-0.9.0rc6.tar.gz

Scope limitations:
- no PyPI publish
- no TestPyPI upload for 0.9.0rc6
- no production-grade physical validation
- no formal convergence proof
- external solvers not run by default
- external LLM not required by default
- proprietary solvers not required by default
- Elmer Level 3 validation deferred
- workflow remains local/synchronous preview
- RC is not final 1.0 stability

Important note:
- v0.9.0rc1 / v0.9.0rc2 / v0.9.0rc3 / v0.9.0rc4 / v0.9.0rc5 tags are unchanged.
- v0.9.0rc6 tag should be created only after maintainer approval.
- This task does not create tag/release or upload packages.
- PyPI publication remains separately gated.
