# TestPyPI Upload Approval Record for v0.9.0rc6

- TestPyPI upload approval for 0.9.0rc6: pending
- TestPyPI already uploaded and verified for 0.9.0rc6.dev0: yes
- PyPI publication approval: not granted
- Upload command authorized for rc6: no
- Current public prerelease: v0.9.0rc5
- Current main release draft: v0.9.0rc6
- v0.9.0rc6 tag: not created
- PyPI: not published
- TestPyPI upload for rc6: not performed

## Command Template

DO NOT RUN WITHOUT APPROVAL.

```bash
python -m twine upload \
  --repository testpypi \
  dist/optical_spec_agent-0.9.0rc6-py3-none-any.whl \
  dist/optical_spec_agent-0.9.0rc6.tar.gz
```

No token should be printed, committed, logged, or pasted into chat.

This record does not authorize PyPI publication, tag creation, GitHub release
creation, or TestPyPI upload for `0.9.0rc6`.
