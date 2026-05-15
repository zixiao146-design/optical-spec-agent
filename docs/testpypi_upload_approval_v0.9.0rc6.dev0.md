# TestPyPI Upload Approval Record for 0.9.0rc6.dev0

Status:
- TestPyPI upload approval: granted for 0.9.0rc6.dev0 only
- PyPI publication approval: not granted
- Upload command authorized: TestPyPI only

Current release context:
- Current public prerelease: v0.9.0rc5
- Current main development version: 0.9.0rc6.dev0
- v0.9.0rc6 tag: not created
- PyPI/TestPyPI: PyPI not published / TestPyPI upload approved for 0.9.0rc6.dev0 only

Expected package version for this development state:
- `0.9.0rc6.dev0`

Expected local dist filenames after build:
- `optical_spec_agent-0.9.0rc6.dev0-py3-none-any.whl`
- `optical_spec_agent-0.9.0rc6.dev0.tar.gz`

Command template:

```bash
# AUTHORIZED FOR TESTPYPI ONLY FOR 0.9.0rc6.dev0.
# DO NOT USE FOR PYPI.
read -s TESTPYPI_TOKEN
export TESTPYPI_TOKEN
python -m twine upload \
  --repository testpypi \
  -u __token__ \
  -p "$TESTPYPI_TOKEN" \
  dist/optical_spec_agent-0.9.0rc6.dev0-py3-none-any.whl \
  dist/optical_spec_agent-0.9.0rc6.dev0.tar.gz
unset TESTPYPI_TOKEN
```

Safety notes:
- TestPyPI upload is authorized only for `0.9.0rc6.dev0`.
- Do not publish PyPI in this task.
- Do not create `v0.9.0rc6` tag.
- Do not create a GitHub release.
- No token is printed, committed, logged, or pasted into chat.
- TestPyPI token must be entered securely and not logged.
- PyPI publication requires separate explicit maintainer approval.
- GitHub release/tag creation remains prohibited.
