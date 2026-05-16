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
