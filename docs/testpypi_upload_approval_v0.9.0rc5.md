# TestPyPI Upload Approval Record for 0.9.0rc5

Approval status:

- TestPyPI upload approval: pending
- PyPI publication approval: not granted
- Upload command authorized: no

Current state:

- Current public prerelease: v0.9.0rc4
- Current main release draft: 0.9.0rc5
- v0.9.0rc5 tag: not created
- PyPI/TestPyPI: not published / not uploaded

Preflight evidence:

- `scripts/testpypi_preflight.sh`: available
- `scripts/run_quality_gates.sh`: available
- TestPyPI no-upload preflight is required before any future upload decision
- Expected package version: 0.9.0rc5

Expected local artifacts:

- `optical_spec_agent-0.9.0rc5-py3-none-any.whl`
- `optical_spec_agent-0.9.0rc5.tar.gz`

Approval requirements before upload:

- Maintainer explicitly approves TestPyPI upload.
- TestPyPI account/token is available.
- Token is entered only through a secure terminal prompt.
- No token is printed, committed, logged, or pasted into chat.
- Upload command is run manually or by an explicitly approved release task.
- PyPI publication remains separately gated and not approved by this document.

Command template, DO NOT RUN WITHOUT APPROVAL:

```bash
python -m twine upload --repository testpypi dist/*
```

Post-upload verification plan, only after approval and upload:

- Confirm project appears on TestPyPI.
- Create clean venv.
- Install from TestPyPI.
- Run import version check.
- Run `optical-spec --help`.
- Record result in a post-TestPyPI status document.

Non-goals:

- Do not upload TestPyPI in this task.
- Do not publish PyPI in this task.
- Do not create `v0.9.0rc5` tag.
- Do not create GitHub release.
- Do not claim production-grade physical validation.
- Do not claim formal convergence proof.
- Do not require external solver or external LLM by default.
- Do not require proprietary solver by default.
