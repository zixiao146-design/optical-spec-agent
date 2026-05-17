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
