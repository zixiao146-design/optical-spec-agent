# Create v0.9.0rc1 Pre-release Workflow

The `Create v0.9.0rc1 Pre-release` workflow is a manual GitHub Actions entry
point for creating the `v0.9.0rc1` GitHub pre-release.

It is intentionally conservative:

- It only runs through `workflow_dispatch`.
- It only creates a GitHub pre-release.
- It does not publish to PyPI.
- It does not upload `dist/` artifacts.
- It does not create, move, or overwrite the git tag.
- It requires the `v0.9.0rc1` tag to already exist.
- It requires `docs/github_release_draft_v0.9.0rc1.md` to exist.
- If the release already exists, it prints the existing release state and exits
  successfully without creating a duplicate release.

## How To Run

1. Open the GitHub repository.
2. Go to **Actions**.
3. Select **Create v0.9.0rc1 Pre-release**.
4. Click **Run workflow**.
5. Use the default inputs:
   - `tag = v0.9.0rc1`
   - `title = optical-spec-agent v0.9.0rc1`
6. After the workflow completes, check the GitHub **Releases** page.

## What It Verifies

Before creating the pre-release, the workflow checks:

- The requested tag exists.
- `pyproject.toml` contains `0.9.0rc1`.
- `src/optical_spec_agent/__init__.py` contains `0.9.0rc1`.
- `README.md` links to `README.zh-CN.md`.
- `README.zh-CN.md` exists.
- `docs/github_release_draft_v0.9.0rc1.md` exists.

## Release Notes Source

The release notes are read from:

```text
docs/github_release_draft_v0.9.0rc1.md
```

The workflow marks the GitHub release as a pre-release. It must not be treated
as final stable `1.0`.

## Not Included

- No PyPI publication.
- No wheel or sdist upload.
- No external solver execution.
- No external LLM provider.
- No production-grade physical validation claim.
- No formal convergence proof claim.
