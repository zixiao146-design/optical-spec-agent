# TestPyPI Upload Approval Record for 0.9.0rc6.dev0

Status:
- TestPyPI upload approval: pending
- PyPI publication approval: not granted
- Upload command authorized: no

Current release context:
- Current public prerelease: v0.9.0rc5
- Current main development version: 0.9.0rc6.dev0
- v0.9.0rc6 tag: not created
- PyPI/TestPyPI: not published / not uploaded

Expected package version for this development state:
- `0.9.0rc6.dev0`

Expected local dist filenames after build:
- `optical_spec_agent-0.9.0rc6.dev0-py3-none-any.whl`
- `optical_spec_agent-0.9.0rc6.dev0.tar.gz`

Command template:

```bash
# DO NOT RUN WITHOUT APPROVAL.
# This command is intentionally not authorized by this record.
python -m twine upload --repository testpypi dist/*
```

Safety notes:
- Do not upload TestPyPI in this task.
- Do not publish PyPI in this task.
- Do not create `v0.9.0rc6` tag.
- Do not create a GitHub release.
- No token is printed, committed, logged, or pasted into chat.
- TestPyPI upload requires explicit maintainer approval.
- PyPI publication requires separate explicit maintainer approval.
