# TestPyPI Upload Approval Record for 0.9.0rc9.dev0

- TestPyPI upload approval: pending
- PyPI publication approval: not granted
- Upload command authorized: no
- Current public prerelease: v0.9.0rc8
- Current main development version: 0.9.0rc9.dev0
- v0.9.0rc9 tag: not created
- v1.0.0 tag: not created
- PyPI: not published
- TestPyPI uploaded and verified only for 0.9.0rc6.dev0
- TestPyPI upload for 0.9.0rc9.dev0: not performed

## Command Template

DO NOT RUN WITHOUT APPROVAL.

```bash
python -m twine upload \
  --repository-url https://test.pypi.org/legacy/ \
  dist/optical_spec_agent-0.9.0rc9.dev0-py3-none-any.whl \
  dist/optical_spec_agent-0.9.0rc9.dev0.tar.gz
```

## Safety Notes

- No token should be printed, committed, logged, or pasted into chat.
- This record does not authorize PyPI publication.
- This record does not authorize tag creation.
- This record does not authorize GitHub release creation.
- This record does not authorize v1.0.0 release work.
- `scripts/testpypi_preflight.sh` remains a no-upload local preflight and must
  print `NO UPLOAD PERFORMED`.
