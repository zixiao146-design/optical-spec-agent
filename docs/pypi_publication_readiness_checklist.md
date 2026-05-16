# PyPI Publication Readiness Checklist

## Current status

- TestPyPI uploaded: yes
- TestPyPI version: 0.9.0rc6.dev0
- Clean install from TestPyPI: passed
- PyPI published: no
- PyPI publication approval: not granted
- Upload command authorized for PyPI: no
- GitHub tag/release for v0.9.0rc6: not created

## Required before PyPI publication

- Explicit maintainer approval is recorded for the exact version.
- Final version is chosen and matches `pyproject.toml` and `__version__`.
- Version has not previously been uploaded to PyPI.
- Quality gates passed.
- GitHub Actions CI passed.
- `python -m build` passed.
- `python -m twine check dist/*` passed.
- TestPyPI verified or an explicit skip is recorded.
- README and package metadata reviewed.
- Release notes reviewed.
- Validation claims reviewed and kept conservative.
- Yanking policy reviewed.
- Post-publication verification plan prepared.

## PyPI publication risks

- Package name claim is permanent once published.
- File/version uploads cannot be freely overwritten.
- Bad metadata may require a new version.
- PyPI yanking is possible but not the same as deletion.
- Production claims must remain conservative.
- Dependency resolution differs from TestPyPI.

## Recommended path

- Do not publish PyPI yet.
- Continue v1.0 readiness engineering.
- Prepare PyPI only after the public contract freeze is confirmed.

This checklist does not authorize PyPI publication, tag creation, GitHub release
creation, TestPyPI re-upload, production-grade physical validation claims, or
formal convergence proof claims.
