# Agent Studio Frontend Safety Policy

- No default solver execution.
- No default external LLM.
- No PyPI/TestPyPI upload controls in MVP.
- No tag/release controls in MVP.
- No proprietary solver default integration.
- No production-grade physical validation claim.
- No formal convergence proof claim.
- Optional solver execution, if ever added, must require explicit approval gates.
- Frontend must display preview and validation boundaries clearly.
- Frontend must remain local-first unless a future maintainer decision changes
  the product scope.
- The implemented MVP must not include buttons or API calls for package upload,
  PyPI/TestPyPI publication, tag creation, or GitHub release creation.
- API disconnected/demo fixture mode must be labeled as not live validation.
- Loading, empty, error, and API disconnected states must preserve the same
  no-solver/no-LLM/no-publication boundary copy.
- Fixture loading buttons may populate local forms, but they must not trigger
  solver execution, external LLM calls, upload, tag, or release actions.
- API mode indicators must make live API versus demo fixture mode clear.
- Diagnostics and recommended next actions must not imply production-grade
  validation or a formal convergence proof.
- Optional Playwright visual smoke may verify rendering and safety copy, but it
  must remain local/manual and outside the default release gate.
- Playwright visual smoke must not upload packages, create tags, create
  releases, execute solvers, or call external LLMs.
- Playwright reports, screenshots, `node_modules`, and frontend build outputs
  must not be committed by default.
- The Agent Studio demo package is local-only. It must not upload packages,
  publish PyPI/TestPyPI, create tags, create GitHub releases, execute solvers,
  or call external LLMs.
- Quickstart scripts and guided demo mode are local-only. They must not upload
  packages, publish PyPI/TestPyPI, create tags, create GitHub releases, execute
  solvers, or call external LLMs.
- Chinese localization must preserve the same safety boundaries:
  默认不执行外部求解器、默认不调用外部 LLM、预览产物不代表生产级物理验证、
  不声明形式化收敛证明、本界面不控制 PyPI/TestPyPI 上传，也不控制 GitHub
  tag/release。
- Localization must not translate API JSON field names, adapter tool names,
  package metadata, version strings, or `api_contract_version`.
- Demo screenshots or recordings must not be committed unless explicitly
  approved by the maintainer.
