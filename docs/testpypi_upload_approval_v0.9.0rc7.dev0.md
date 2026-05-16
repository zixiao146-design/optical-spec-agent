# TestPyPI Upload Approval Record for 0.9.0rc7.dev0

- TestPyPI upload approval: pending
- PyPI publication approval: not granted
- Upload command authorized: no
- Current public prerelease: v0.9.0rc6
- Current main development version: 0.9.0rc7.dev0
- v0.9.0rc7 tag: not created
- v1.0.0 tag: not created
- PyPI: not published
- TestPyPI upload for 0.9.0rc7.dev0: not performed

## Command Template

DO NOT RUN WITHOUT APPROVAL.

```bash
python -m twine upload \
  --repository testpypi \
  dist/optical_spec_agent-0.9.0rc7.dev0-py3-none-any.whl \
  dist/optical_spec_agent-0.9.0rc7.dev0.tar.gz
```

No token should be printed, committed, logged, or pasted into chat.

This record does not authorize TestPyPI upload, PyPI publication, tag creation,
GitHub release creation, or v1.0.0 release.
