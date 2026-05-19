# TestPyPI Upload Approval Record for v0.9.0rc7

## Current status

- TestPyPI upload approval for 0.9.0rc7: pending
- TestPyPI already uploaded and verified only for 0.9.0rc6.dev0: yes
- PyPI publication approval: not granted
- Upload command authorized for rc7: no
- Current public prerelease: v0.9.0rc6
- Current main release draft: v0.9.0rc7
- v0.9.0rc7 tag: not created
- PyPI: not published
- TestPyPI upload for rc7: not performed

## Command template

DO NOT RUN WITHOUT APPROVAL:

```bash
python -m twine upload \
  --repository testpypi \
  dist/optical_spec_agent-0.9.0rc7-py3-none-any.whl \
  dist/optical_spec_agent-0.9.0rc7.tar.gz
```

## Token handling

- No token should be printed.
- No token should be committed.
- No token should be logged.
- No token should be pasted into chat.

## Safety boundaries

- This record does not authorize TestPyPI upload.
- This record does not authorize PyPI publication.
- This record does not authorize tag creation.
- This record does not authorize GitHub release creation.
- This record does not authorize `v1.0.0`.
