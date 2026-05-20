# TestPyPI Upload Approval Record for 0.9.0rc8

- TestPyPI upload approval for 0.9.0rc8: pending
- TestPyPI already uploaded and verified only for 0.9.0rc6.dev0: yes
- PyPI publication approval: not granted
- Upload command authorized for rc8: no
- Current public prerelease: v0.9.0rc7
- Current main release draft: v0.9.0rc8
- v0.9.0rc8 tag: not created
- v1.0.0 tag: not created
- PyPI: not published
- TestPyPI upload for rc8: not performed

## Command Template

DO NOT RUN WITHOUT APPROVAL.

```bash
python -m twine upload --repository testpypi \
  dist/optical_spec_agent-0.9.0rc8-py3-none-any.whl \
  dist/optical_spec_agent-0.9.0rc8.tar.gz
```

## Token Safety

- No token should be printed, committed, logged, or pasted into chat.
- Do not read, print, save, or commit `TESTPYPI_TOKEN`, `PYPI_TOKEN`,
  `GH_TOKEN`, or `GITHUB_TOKEN`.
- This record does not authorize TestPyPI upload, PyPI publication, tag
  creation, GitHub release creation, or v1.0.0 release.
