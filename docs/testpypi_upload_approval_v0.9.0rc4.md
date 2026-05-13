# TestPyPI Upload Approval Record for 0.9.0rc4

Approval status:
- TestPyPI upload approval: pending
- PyPI publication approval: not granted
- Upload command authorized: no

Current state:
- Current public prerelease: v0.9.0rc3
- Current main release draft: 0.9.0rc4
- v0.9.0rc4 tag: not created
- PyPI: not published
- TestPyPI: not uploaded

Preflight evidence:
- `scripts/testpypi_preflight.sh`: passed
- `twine check`: passed
- Wheel install: passed
- `optical_spec_agent.__version__`: 0.9.0rc4
- `optical-spec --help`: passed
- `pytest`: 429 passed, 4 warnings
- `python -m build`: passed
- `make check`: passed

Expected local artifacts:
- `optical_spec_agent-0.9.0rc4-py3-none-any.whl`
- `optical_spec_agent-0.9.0rc4.tar.gz`

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
- Do not create `v0.9.0rc4` tag.
- Do not create GitHub release.
- Do not claim production-grade physical validation.
- Do not claim formal convergence proof.
- Do not require external solver or external LLM by default.
