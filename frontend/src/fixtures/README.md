# Agent Studio Frontend Fixtures

The frontend MVP uses the canonical API fixtures in `../../examples/api` during
development. Keeping fixture ownership outside the frontend avoids duplicating
API contract examples.

- API contract version: 0.1
- No network access beyond the configured local API base URL.
- No solver execution by default.
- No external LLM call by default.
- No PyPI/TestPyPI upload controls.
- No tag or release controls.
